import json
import logging
import uuid
from importlib import metadata

from core.exceptions import SyncError
from dcim.models import Device
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django_tables2 import Column
from ipfabric import IPFClient
from jinja2.sandbox import SandboxedEnvironment
from netbox.config import get_config
from netutils.utils import jinja2_convenience_function

from ..choices import IPFabricSourceTypeChoices
from .nbutils import device_serial_max_length
from .nbutils import order_devices
from .nbutils import order_members
from .nbutils import order_pn
from .nbutils import order_vrf

logger = logging.getLogger("ipfabric_netbox.utilities.ipf_utils")


def slugify_text(value):
    return slugify(value)


def serial(value):
    sn_length = len(value.get("sn"))
    serial_number = value.get("sn") if sn_length < device_serial_max_length else ""
    if not serial_number:
        serial_number = value.get("id")
    return serial_number


IPF_JINJA_FILTERS = {"slugify": slugify_text, "serial": serial}


def render_jinja2(template_code, context):
    """
    Render a Jinja2 template with the provided context. Return the rendered content.
    """
    environment = SandboxedEnvironment()
    environment.filters.update(get_config().JINJA2_FILTERS)
    environment.filters.update(IPF_JINJA_FILTERS)
    environment.filters.update(jinja2_convenience_function())
    return environment.from_string(source=template_code).render(**context)


class IPFabric(object):
    def __init__(self, parameters=None, transform_map=None) -> None:
        if parameters:
            self.ipf = IPFClient(**parameters, unloaded=True)
        else:
            self.ipf = IPFClient(
                **settings.PLUGINS_CONFIG["ipfabric_netbox"], unloaded=True
            )
        self.ipf._client.headers[
            "user-agent"
        ] += f'; ipfabric-netbox/{metadata.version("ipfabric-netbox")}'  # noqa: E702
        self.transform_map = transform_map

    def get_snapshots(self) -> dict:
        formatted_snapshots = {}
        if self.ipf:
            for snapshot_ref, snapshot in self.ipf.snapshots.items():
                if snapshot.status != "done" and snapshot.finish_status != "done":
                    continue
                if snapshot_ref in ["$prev", "$lastLocked"]:
                    continue
                if snapshot.name:
                    description = (
                        snapshot.name
                        + " - "
                        + snapshot.end.strftime("%d-%b-%y %H:%M:%S")
                    )
                else:
                    description = snapshot.end.strftime("%d-%b-%y %H:%M:%S")

                formatted_snapshots[snapshot_ref] = (description, snapshot.snapshot_id)
        return formatted_snapshots

    def get_sites(self, snapshot=None) -> dict():
        if snapshot:
            raw_sites = self.ipf.inventory.sites.all(snapshot_id=snapshot)
        else:
            raw_sites = self.ipf.inventory.sites.all()
        sites = []
        for item in raw_sites:
            sites.append(item["siteName"])
        return sites

    def get_table_data(self, table, device):
        filter = {"sn": ["eq", device.serial]}
        split = table.split(".")

        if len(split) == 2:
            if split[1] == "serial_ports":
                table = getattr(self.ipf.technology, split[1])
            else:
                tech = getattr(self.ipf.technology, split[0])
                table = getattr(tech, split[1])
        else:
            table = getattr(self.ipf.inventory, split[0])

        columns = self.ipf.get_columns(table.endpoint)

        columns.pop(0)

        columns = [(k, Column()) for k in columns]
        data = table.all(
            filters=filter,
        )
        return data, columns


class IPFabricSyncRunner(object):
    def __init__(
        self, transform_map, sync=None, client: IPFabric = None, settings: dict = None
    ) -> None:
        self.client = client
        self.settings = settings
        self.transform_map = transform_map
        self.sync = sync
        self.relationship_store = {}
        self.siteUUID = {}
        if hasattr(self.sync, "logger"):
            self.logger = self.sync.logger
        self.interface_count_total = 0
        self.interface_count = 1
        self.inventoryitem_count = 1
        self.inventoryitem_count_total = 0

        if self.sync.snapshot_data.status != "loaded":
            raise SyncError("Snapshot not loaded in IP Fabric.")

    def get_model_or_update(self, app, model, data, uuid=None):
        transform_map = self.transform_map.objects.filter(
            target_model__app_label=app, target_model__model=model
        ).first()

        if not transform_map:
            raise SystemError(f"No transform map available for {app}: {model}")

        model_settings = self.settings.get(model, False)
        object = None

        if model_settings:
            logger.info(f"Creating {model}")
            object = transform_map.update_or_create_instance(
                data=data,
                uuid=uuid,
                relationship_store=self.relationship_store,
                tags=self.sync.tags.all(),
                logger=self.logger,
            )
        else:
            logger.info(f"Getting {model}")
            coalesce_fields = transform_map.get_coalesce_fields(data)
            object = get_object_or_404(
                transform_map.target_model.model_class().objects.all(),
                **coalesce_fields,
            )

        store = self.relationship_store.get(uuid)

        if store:
            store[object._meta.model] = object
        else:
            self.relationship_store[uuid] = {object._meta.model: object}

        return object

    def create_interface(
        self, device_interface, device_uuid, managed_ips, device_object, device
    ):
        device_interface["loginIp"] = device.get("loginIp")
        interface_object = self.get_model_or_update(
            "dcim", "interface", device_interface, uuid=device_uuid
        )

        self.logger.increment_statistics(
            model="interface",
            current=self.interface_count,
            total=self.interface_count_total,
        )
        self.interface_count += 1

        if self.settings.get("ipaddress"):
            managed_ip = managed_ips.get(device_object.serial, {}).get(
                interface_object.name
            )
            if managed_ip:
                ip_address_obj = self.get_model_or_update(
                    "ipam",
                    "ipaddress",
                    managed_ip,
                )
                try:
                    other_device = Device.objects.get(primary_ip4=ip_address_obj)
                    if other_device and device_object != other_device:
                        other_device.primary_ip4 = None
                        other_device.save()
                except ObjectDoesNotExist:
                    pass

                if device.get("loginIp") == device_interface.get("primaryIp"):
                    device_object.primary_ip4 = ip_address_obj
                    device_object.save()

        return True

    def collect_data(self):
        try:
            self.logger.log_info(
                "Collecting information from IP Fabric",
                obj=self.sync.snapshot_data.source,
            )
            data = {}
            if self.sync.snapshot_data.source.type == IPFabricSourceTypeChoices.REMOTE:
                self.logger.log_info(
                    "Remote collector checking for snapshot data.", obj=self.sync
                )
                if not self.sync.snapshot_data.ipf_data.count() > 0:
                    raise SyncError(
                        "No snapshot data available. This is a remote sync. Push data to NetBox first."
                    )
                data["site"] = list(
                    self.sync.snapshot_data.ipf_data.filter(type="site").values_list(
                        "data", flat=True
                    )
                )
                data["device"] = list(
                    self.sync.snapshot_data.ipf_data.filter(type="device").values_list(
                        "data", flat=True
                    )
                )
                data["virtualchassis"] = list(
                    self.sync.snapshot_data.ipf_data.filter(
                        type="virtualchassis"
                    ).values_list("data", flat=True)
                )
                data["interface"] = list(
                    self.sync.snapshot_data.ipf_data.filter(
                        type="interface"
                    ).values_list("data", flat=True)
                )
                data["inventoryitem"] = list(
                    self.sync.snapshot_data.ipf_data.filter(
                        type="inventoryitem"
                    ).values_list("data", flat=True)
                )
                data["vlan"] = list(
                    self.sync.snapshot_data.ipf_data.filter(type="vlan").values_list(
                        "data", flat=True
                    )
                )
                data["vrf"] = list(
                    self.sync.snapshot_data.ipf_data.filter(type="vrf").values_list(
                        "data", flat=True
                    )
                )
                data["prefix"] = list(
                    self.sync.snapshot_data.ipf_data.filter(type="prefix").values_list(
                        "data", flat=True
                    )
                )
                data["ipaddress"] = list(
                    self.sync.snapshot_data.ipf_data.filter(
                        type="ipaddress"
                    ).values_list("data", flat=True)
                )
            else:
                self.logger.log_info(
                    "Local collector being used for snapshot data.", obj=self.sync
                )
                excluded_vendors = ["aws", "azure"]

                query_filter = {
                    "and": [{"vendor": ["neq", vendor]} for vendor in excluded_vendors]
                }
                # filter = {"and": [{"vendor": ["neq", "aws"]}, {"vendor": ["neq", "azure"]}]}

                if ingestion_sites := self.settings.get("sites"):
                    site_filter = {
                        "or": [{"siteName": ["eq", site]} for site in ingestion_sites]
                    }
                    query_filter["and"].append(site_filter)

                    self.logger.log_info(
                        f"Creating site filter {json.dumps(site_filter)}", obj=self.sync
                    )
                else:
                    site_filter = {}

                data["site"] = self.client.inventory.sites.all(
                    snapshot_id=self.settings["snapshot_id"]
                )

                data["device"] = self.client.inventory.devices.all(
                    snapshot_id=self.settings["snapshot_id"], filters=query_filter
                )

                data[
                    "virtualchassis"
                ] = self.client.technology.platforms.stacks_members.all(
                    snapshot_id=self.settings["snapshot_id"], filters=site_filter
                )

                data["interface"] = self.client.inventory.interfaces.all(
                    snapshot_id=self.settings["snapshot_id"]
                )

                data["inventoryitem"] = self.client.inventory.pn.all(
                    snapshot_id=self.settings["snapshot_id"],
                    filters={
                        "and": [{"sn": ["empty", False]}, {"name": ["empty", False]}]
                    },
                )

                data["vlan"] = self.client.technology.vlans.site_summary.all(
                    snapshot_id=self.settings["snapshot_id"], filters=site_filter
                )

                data["vrf"] = self.client.technology.routing.vrf_detail.all(
                    snapshot_id=self.settings["snapshot_id"], filters=site_filter
                )

                if site_filter:
                    networks_filter = {
                        "and": [site_filter, {"and": [{"net": ["empty", False]}]}]
                    }
                else:
                    networks_filter = {"and": [{"net": ["empty", False]}]}
                self.logger.log_info(f"Creating network filter: `{networks_filter}`")
                data["prefix"] = self.client.technology.managed_networks.networks.all(
                    snapshot_id=self.settings["snapshot_id"], filters=networks_filter
                )

                data[
                    "ipaddress"
                ] = self.client.technology.addressing.managed_ip_ipv4.all(
                    snapshot_id=self.settings["snapshot_id"]
                )
        except Exception as e:
            self.logger.log_failure(
                f"Error collecting data from IP Fabric: {e}", obj=self.sync
            )
            raise SyncError(f"Error collecting data from IP Fabric: {e}")

        self.logger.log_info(
            f"{len(data['site'])} sites collected", obj=self.sync.snapshot_data.source
        )
        self.logger.log_info(
            f"{len(data['device'])} devices collected",
            obj=self.sync.snapshot_data.source,
        )
        self.logger.log_info(
            f"{len(data['virtualchassis'])} stack members collected",
            obj=self.sync.snapshot_data.source,
        )

        self.logger.log_info(
            f"{len(data['interface'])} interfaces collected",
            obj=self.sync.snapshot_data.source,
        )

        self.logger.log_info(
            f"{len(data.get('inventoryitem', []))} part numbers collected",
            obj=self.sync.snapshot_data.source,
        )

        self.logger.log_info(
            f"{len(data.get('vlan', []))} VLANs collected",
            obj=self.sync.snapshot_data.source,
        )

        self.logger.log_info(
            f"{len(data.get('vrf', []))} VRFs collected",
            obj=self.sync.snapshot_data.source,
        )

        self.logger.log_info(
            f"{len(data.get('prefix', []))} networks collected",
            obj=self.sync.snapshot_data.source,
        )

        self.logger.log_info(
            f"{len(data.get('ipaddress', []))} management IP's collected",
            obj=self.sync.snapshot_data.source,
        )

        self.logger.log_info("Ordering devices", obj=self.sync)

        members = order_members(data.get("virtualchassis", []))
        devices = order_devices(data.get("device", []), members)

        self.logger.log_info("Ordering Part Numbers", obj=self.sync)

        part_numbers = order_pn(data.get("inventoryitem", []))

        self.logger.log_info("Ordering VRF's", obj=self.sync)

        vrfs = order_vrf(data["vrf"])

        managed_ips = {}
        site_dict = {}
        interface_dict = {}
        for site in data["site"]:
            site_dict[site["siteName"]] = site

        for interface in data["interface"]:
            if int_sn := interface.get("sn"):
                if interface_dict.get(int_sn):
                    interface_dict[int_sn].append(interface)
                else:
                    interface_dict[int_sn] = [interface]

        interface_key = "nameOriginal"
        try:
            int_transform_map = self.transform_map.objects.filter(
                target_model__app_label="dcim", target_model__model="interface"
            ).first()
            int_name_field_map = int_transform_map.field_maps.filter(
                target_field="name"
            ).first()
            interface_key = int_name_field_map.source_field
        except Exception as e:
            self.logger.log_failure(
                f"Error collecting information about transform map for interface name: {e}",
                obj=self.sync,
            )
            raise SyncError(f"Error collecting source column name for interface: {e}")

        for ip in data["ipaddress"]:
            # Find corresponding interface list by serial number (sn)
            device_interfaces = interface_dict.get(ip["sn"], [])

            # Use filter to find the interface with the matching intName
            filtered_interface = list(
                filter(lambda d: d["intName"] == ip["intName"], device_interfaces)
            )

            if filtered_interface:
                ip["nameOriginal"] = filtered_interface[0]["nameOriginal"]
                if ip[interface_key]:
                    int_name = ip[interface_key]
                else:
                    int_name = ip["intName"]

                if managed_ips.get(ip["sn"]):
                    managed_ips[ip["sn"]][int_name] = ip
                else:
                    managed_ips[ip["sn"]] = {int_name: ip}

        return (
            site_dict,
            devices,
            interface_dict,
            part_numbers,
            vrfs,
            data["vlan"],
            data["prefix"],
            managed_ips,
        )

    def sync_devices(self, branch=None):
        self.logger.log_info("Starting device sync", obj=self.sync)

        (
            site_dict,
            devices,
            interface_dict,
            part_numbers,
            vrfs,
            vlans,
            networks,
            managed_ips,
        ) = self.collect_data()
        vlan_count = 1
        vrf_count = 1
        network_count = 1
        device_vrfs_total = 0

        for device_count, device in enumerate(devices, start=1):
            logger.info(f"Device {device_count} out of {len(devices)}")
            self.logger.increment_statistics(
                model="device", current=device_count, total=len(devices)
            )

            device_uuid = str(uuid.uuid4())

            site_object = self.get_model_or_update(
                "dcim", "site", site_dict[device["siteName"]], uuid=device_uuid
            )

            self.get_model_or_update("dcim", "manufacturer", device, uuid=device_uuid)
            self.get_model_or_update("dcim", "devicetype", device, uuid=device_uuid)

            self.get_model_or_update("dcim", "platform", device, uuid=device_uuid)

            self.get_model_or_update("dcim", "devicerole", device, uuid=device_uuid)

            device_object = self.get_model_or_update(
                "dcim", "device", device, uuid=device_uuid
            )

            site_object.custom_field_data[
                "ipfabric_source"
            ] = self.sync.snapshot_data.source.pk

            device_object.custom_field_data[
                "ipfabric_source"
            ] = self.sync.snapshot_data.source.pk
            if branch:
                site_object.custom_field_data["ipfabric_branch"] = branch.pk
                device_object.custom_field_data["ipfabric_branch"] = branch.pk

            site_object.save()
            device_object.save()

            if self.settings.get("virtualchassis"):
                if member := device.get("virtual_chassis"):
                    self.get_model_or_update("dcim", "virtualchassis", member)
                    device_object = self.get_model_or_update(
                        "dcim", "device", device, uuid=device_uuid
                    )

            if device_object and self.settings.get("interface"):
                device_interfaces = interface_dict.get(device.get("sn"), [])
                self.interface_count_total += len(device_interfaces)
                for device_interface in device_interfaces:
                    self.create_interface(
                        device_interface,
                        device_uuid,
                        managed_ips,
                        device_object,
                        device,
                    )
                    # x = threading.Thread(target=self.create_interface, args=((device_interface, device_uuid, managed_ips, device_object, device)))
                    # threads.append(x)
                    # x.start()

            if self.settings.get("vrf"):
                device_vrfs = vrfs.get(device_object.serial, [])
                device_vrfs_total += len(device_vrfs)
                for vrf in device_vrfs:
                    self.get_model_or_update("ipam", "vrf", vrf, uuid=device_uuid)
                    self.logger.increment_statistics(
                        model="vrf", current=vrf_count, total=device_vrfs_total
                    )
                    vrf_count += 1

            device_count += 1

        if self.settings.get("inventoryitem"):
            devices = Device.objects.all()
            for device in devices:
                device_parts = part_numbers.get(device.serial, [])
                self.inventoryitem_count_total += len(device_parts)
                for part in device_parts:
                    self.get_model_or_update("dcim", "inventoryitem", part)
                    self.logger.increment_statistics(
                        model="inventory_item",
                        current=self.inventoryitem_count,
                        total=self.inventoryitem_count_total,
                    )
                    self.inventoryitem_count += 1

        if self.settings.get("vlan"):
            for vlan in vlans:
                self.get_model_or_update("ipam", "vlan", vlan)
                self.logger.increment_statistics(
                    model="vlan", current=vlan_count, total=len(vlans)
                )
                vlan_count += 1

        if self.settings.get("prefix"):
            for network in networks:
                self.get_model_or_update("ipam", "prefix", network)
                self.logger.increment_statistics(
                    model="prefix", current=network_count, total=len(networks)
                )
                network_count += 1

    def sync(self):
        self.sync_devices()
