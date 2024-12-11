import copy
import json
import uuid

from dcim.models import Device
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.test import TestCase
from django.utils import timezone

from ipfabric_netbox.models import IPFabricSnapshot
from ipfabric_netbox.models import IPFabricSource
from ipfabric_netbox.models import IPFabricSync
from ipfabric_netbox.models import IPFabricTransformField
from ipfabric_netbox.models import IPFabricTransformMap
from ipfabric_netbox.utilities.ipfutils import IPFabricSyncRunner

transform_maps = [
    {
        "model": "ipfabric_netbox.ipfabrictransformmap",
        "pk": 4,
        "fields": {
            "created": "2023-06-22T09:12:03.018Z",
            "last_updated": "2023-06-22T09:12:03.018Z",
            "custom_field_data": {},
            "name": "Platform Transform Map",
            "source_model": "device",
            "target_model": 43,
            "status": "",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformmap",
        "pk": 1,
        "fields": {
            "created": "2023-06-22T09:12:02.886Z",
            "last_updated": "2023-06-22T09:53:32.100Z",
            "custom_field_data": {},
            "name": "Site Transform Map",
            "source_model": "site",
            "target_model": 56,
            "status": "active",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformmap",
        "pk": 2,
        "fields": {
            "created": "2023-06-22T09:12:02.924Z",
            "last_updated": "2023-06-22T15:02:20.038Z",
            "custom_field_data": {},
            "name": "Manufacturer Transform Map",
            "source_model": "device",
            "target_model": 42,
            "status": "",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformmap",
        "pk": 5,
        "fields": {
            "created": "2023-06-22T09:12:03.087Z",
            "last_updated": "2023-06-22T15:51:28.987Z",
            "custom_field_data": {},
            "name": "Device Transform Map",
            "source_model": "device",
            "target_model": 31,
            "status": "active",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformmap",
        "pk": 6,
        "fields": {
            "created": "2023-06-22T09:12:03.134Z",
            "last_updated": "2023-06-22T16:24:22.879Z",
            "custom_field_data": {},
            "name": "Device Role Transform Map",
            "source_model": "device",
            "target_model": 34,
            "status": "",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformmap",
        "pk": 3,
        "fields": {
            "created": "2023-06-22T09:12:02.971Z",
            "last_updated": "2023-06-23T13:23:50.445Z",
            "custom_field_data": {},
            "name": "Device Type Transform Map",
            "source_model": "device",
            "target_model": 35,
            "status": "",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformmap",
        "pk": 10,
        "fields": {
            "created": "2023-06-23T14:42:40.118Z",
            "last_updated": "2023-06-23T14:42:40.118Z",
            "custom_field_data": {},
            "name": "Interface Transform Map",
            "source_model": "interface",
            "target_model": 38,
            "status": "",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformmap",
        "pk": 11,
        "fields": {
            "created": "2023-06-28T15:13:56.033Z",
            "last_updated": "2023-06-28T15:18:37.423Z",
            "custom_field_data": {},
            "name": "Inventory Transform Map",
            "source_model": "part_number",
            "target_model": 40,
            "status": "",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformmap",
        "pk": 12,
        "fields": {
            "created": "2023-07-14T15:37:25.428Z",
            "last_updated": "2023-07-14T15:37:25.428Z",
            "custom_field_data": {},
            "name": "VLAN Transform Map",
            "source_model": "vlan",
            "target_model": 75,
            "status": "active",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformmap",
        "pk": 13,
        "fields": {
            "created": "2023-07-14T16:39:14.674Z",
            "last_updated": "2023-07-14T16:39:14.675Z",
            "custom_field_data": {},
            "name": "VRF Transform Map",
            "source_model": "vrf",
            "target_model": 73,
            "status": "",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformmap",
        "pk": 14,
        "fields": {
            "created": "2023-07-18T09:36:57.588Z",
            "last_updated": "2023-07-18T09:36:57.588Z",
            "custom_field_data": {},
            "name": "Prefix Transform Map",
            "source_model": "prefix",
            "target_model": 69,
            "status": "active",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformmap",
        "pk": 15,
        "fields": {
            "created": "2023-07-31T10:54:29.792Z",
            "last_updated": "2023-07-31T10:54:29.792Z",
            "custom_field_data": {},
            "name": "Virtual Chassis Transform Map",
            "source_model": "virtualchassis",
            "target_model": 58,
            "status": "",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformmap",
        "pk": 16,
        "fields": {
            "created": "2023-08-15T14:34:00.334Z",
            "last_updated": "2023-08-15T14:34:00.334Z",
            "custom_field_data": {},
            "name": "IP Address Transform Map",
            "source_model": "ipaddress",
            "target_model": 68,
            "status": "active",
        },
    },
]

transform_fields = [
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 19,
        "fields": {
            "created": "2023-06-23T15:01:13.459Z",
            "last_updated": "2023-06-23T15:01:13.459Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 10,
            "source_field": "dscr",
            "target_field": "description",
            "coalesce": False,
            "template": '{{ object.dscr or ""}}',
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 20,
        "fields": {
            "created": "2023-06-28T10:39:24.588Z",
            "last_updated": "2023-06-28T10:39:24.588Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 10,
            "source_field": "media",
            "target_field": "type",
            "coalesce": False,
            "template": "1000base-t",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 2,
        "fields": {
            "created": "2023-06-22T09:12:02.900Z",
            "last_updated": "2023-06-22T09:12:02.900Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 1,
            "source_field": "siteName",
            "target_field": "slug",
            "coalesce": True,
            "template": "{{ object.siteName | slugify }}",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 3,
        "fields": {
            "created": "2023-06-22T09:12:02.933Z",
            "last_updated": "2023-06-22T09:12:02.933Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 2,
            "source_field": "vendor",
            "target_field": "name",
            "coalesce": False,
            "template": None,
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 25,
        "fields": {
            "created": "2023-06-28T10:46:04.153Z",
            "last_updated": "2023-06-28T10:46:04.153Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 10,
            "source_field": "l1",
            "target_field": "enabled",
            "coalesce": False,
            "template": '{% if object.l1 == "up" %}True{% else %}False{% endif %}',
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 34,
        "fields": {
            "created": "2023-07-14T15:38:30.728Z",
            "last_updated": "2023-07-31T10:37:21.182Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 12,
            "source_field": "vlanName",
            "target_field": "name",
            "coalesce": False,
            "template": '{{ object.vlanName or ""}}',
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 40,
        "fields": {
            "created": "2023-07-31T15:07:09.911Z",
            "last_updated": "2023-07-31T15:07:09.911Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 15,
            "source_field": "master",
            "target_field": "name",
            "coalesce": True,
            "template": "",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 22,
        "fields": {
            "created": "2023-06-28T10:41:47.345Z",
            "last_updated": "2023-06-28T12:08:47.704Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 10,
            "source_field": "mac",
            "target_field": "mac_address",
            "coalesce": False,
            "template": '{% if object.mac %}{{ object.mac | mac_to_format(frmt="MAC_COLON_TWO") | upper }}{% else %}{{ "00:00:00:00:00:01" | mac_to_format(frmt="MAC_COLON_TWO") | upper }}{% endif %}',
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 4,
        "fields": {
            "created": "2023-06-22T09:12:02.948Z",
            "last_updated": "2023-06-22T09:12:02.948Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 2,
            "source_field": "vendor",
            "target_field": "slug",
            "coalesce": True,
            "template": "{{ object.vendor | slugify }}",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 8,
        "fields": {
            "created": "2023-06-22T09:12:03.043Z",
            "last_updated": "2023-07-14T10:54:57.940Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 4,
            "source_field": "vendor",
            "target_field": "slug",
            "coalesce": True,
            "template": "{{ object.vendor | slugify }}{%if object.family %}_{{ object.family | slugify }}{% endif %}",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 6,
        "fields": {
            "created": "2023-06-22T09:12:02.995Z",
            "last_updated": "2023-06-22T09:12:02.995Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 3,
            "source_field": "vendor",
            "target_field": "slug",
            "coalesce": True,
            "template": "{{ object.vendor | slugify }}",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 26,
        "fields": {
            "created": "2023-06-28T10:49:23.845Z",
            "last_updated": "2023-06-28T14:50:04.953Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 10,
            "source_field": "intName",
            "target_field": "name",
            "coalesce": True,
            "template": "",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 28,
        "fields": {
            "created": "2023-06-28T15:20:02.726Z",
            "last_updated": "2023-06-28T15:20:08.343Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 11,
            "source_field": "sn",
            "target_field": "serial",
            "coalesce": True,
            "template": "",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 29,
        "fields": {
            "created": "2023-06-28T15:20:22.262Z",
            "last_updated": "2023-06-28T15:20:22.262Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 11,
            "source_field": "pid",
            "target_field": "part_id",
            "coalesce": False,
            "template": "",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 7,
        "fields": {
            "created": "2023-06-22T09:12:03.027Z",
            "last_updated": "2023-07-14T10:56:34.746Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 4,
            "source_field": "family",
            "target_field": "name",
            "coalesce": False,
            "template": "{%if object.family %}{{ object.family | slugify }}{% else %}{{ object.vendor }}{% endif %}",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 35,
        "fields": {
            "created": "2023-07-14T15:38:43.642Z",
            "last_updated": "2023-07-14T15:39:37.833Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 12,
            "source_field": "vlanId",
            "target_field": "vid",
            "coalesce": True,
            "template": "",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 36,
        "fields": {
            "created": "2023-07-14T15:39:00.515Z",
            "last_updated": "2023-07-14T15:57:48.819Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 12,
            "source_field": "dscr",
            "target_field": "description",
            "coalesce": False,
            "template": '{{ object.dscr or ""}}',
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 11,
        "fields": {
            "created": "2023-06-22T09:12:03.112Z",
            "last_updated": "2023-06-22T09:12:03.112Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 5,
            "source_field": "sn",
            "target_field": "serial",
            "coalesce": True,
            "template": "{{ object | serial }}",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 37,
        "fields": {
            "created": "2023-07-14T16:39:34.015Z",
            "last_updated": "2023-07-14T16:39:34.015Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 13,
            "source_field": "vrf",
            "target_field": "name",
            "coalesce": True,
            "template": "",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 21,
        "fields": {
            "created": "2023-06-28T10:41:03.607Z",
            "last_updated": "2023-08-08T14:44:52.118Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 10,
            "source_field": "mtu",
            "target_field": "mtu",
            "coalesce": False,
            "template": "{{ object.mtu or 1500 }}",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 38,
        "fields": {
            "created": "2023-07-14T16:39:57.563Z",
            "last_updated": "2023-07-14T16:44:39.864Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 13,
            "source_field": "rd",
            "target_field": "rd",
            "coalesce": True,
            "template": "",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 42,
        "fields": {
            "created": "2023-08-09T12:31:17.235Z",
            "last_updated": "2023-08-09T12:31:17.235Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 5,
            "source_field": "hostname",
            "target_field": "vc_position",
            "coalesce": False,
            "template": "{% if object.virtual_chassis is defined %}{{ object.virtual_chassis.member }}{% else %}None{% endif %}",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 10,
        "fields": {
            "created": "2023-06-22T09:12:03.095Z",
            "last_updated": "2023-08-14T09:56:03.044Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 5,
            "source_field": "hostname",
            "target_field": "name",
            "coalesce": False,
            "template": "",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 1,
        "fields": {
            "created": "2023-06-22T09:12:02.889Z",
            "last_updated": "2023-07-17T10:08:24.194Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 1,
            "source_field": "siteName",
            "target_field": "name",
            "coalesce": False,
            "template": "",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 27,
        "fields": {
            "created": "2023-06-28T15:19:45.005Z",
            "last_updated": "2023-06-28T16:18:37.860Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 11,
            "source_field": "name",
            "target_field": "name",
            "coalesce": False,
            "template": "{% if object.name is not none %}{{ object.name }}{% elif object.dscr is not none %}{{ object.dscr}}{% else %}Default Name{% endif %}",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 12,
        "fields": {
            "created": "2023-06-22T09:12:03.144Z",
            "last_updated": "2023-06-22T16:24:30.681Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 6,
            "source_field": "devType",
            "target_field": "name",
            "coalesce": False,
            "template": "",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 13,
        "fields": {
            "created": "2023-06-22T09:12:03.161Z",
            "last_updated": "2023-06-22T16:24:34.880Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 6,
            "source_field": "devType",
            "target_field": "slug",
            "coalesce": True,
            "template": "{{ object.devType | slugify }}",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 39,
        "fields": {
            "created": "2023-07-18T09:40:37.112Z",
            "last_updated": "2023-07-18T09:41:09.238Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 14,
            "source_field": "net",
            "target_field": "prefix",
            "coalesce": True,
            "template": "",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 43,
        "fields": {
            "created": "2023-08-15T14:25:31.706Z",
            "last_updated": "2023-08-15T14:25:31.706Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 10,
            "source_field": "primaryIp",
            "target_field": "mgmt_only",
            "coalesce": False,
            "template": "{% if object.primaryIp == object.loginIp %}True{% else %}False{% endif %}",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 5,
        "fields": {
            "created": "2023-06-22T09:12:02.979Z",
            "last_updated": "2023-07-14T13:51:37.370Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 3,
            "source_field": "model",
            "target_field": "model",
            "coalesce": False,
            "template": '{% if object.model|string != ""%}{{ object.model | string }}{% else %}{{ object.vendor }} - {{ object.family }} - {{ object.platform }}{% endif %}',
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 14,
        "fields": {
            "created": "2023-06-22T09:12:03.177Z",
            "last_updated": "2023-06-22T16:24:48.259Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 6,
            "source_field": "devType",
            "target_field": "vm_role",
            "coalesce": True,
            "template": "False",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 44,
        "fields": {
            "created": "2023-08-15T14:38:13.622Z",
            "last_updated": "2023-08-15T20:12:45.341Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 16,
            "source_field": "sn",
            "target_field": "assigned_object_id",
            "coalesce": False,
            "template": "{{ dcim.Interface.objects.filter(device__serial=object.sn, name=object.intName).first().pk }}",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabrictransformfield",
        "pk": 45,
        "fields": {
            "created": "2023-08-15T14:59:24.131Z",
            "last_updated": "2023-08-15T20:26:08.071Z",
            "custom_field_data": {},
            "description": "",
            "comments": "",
            "transform_map": 16,
            "source_field": "net",
            "target_field": "address",
            "coalesce": True,
            "template": "{% if object.net %}{% set MASK = object.net.split('/')[1] %}{% else %}{% set MASK = 32 %}{% endif %}{{ object.ip }}/{{MASK}}",
        },
    },
]

transform_relationship_fields = [
    {
        "model": "ipfabric_netbox.ipfabricrelationshipfield",
        "pk": 21,
        "fields": {
            "created": "2023-07-31T19:48:34.485Z",
            "last_updated": "2023-08-09T10:41:49.273Z",
            "custom_field_data": {},
            "transform_map": 15,
            "source_model": 31,
            "target_field": "master",
            "coalesce": False,
            "template": "{{ dcim.Device.objects.filter(serial=object.sn).first().pk }}",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabricrelationshipfield",
        "pk": 3,
        "fields": {
            "created": "2023-06-23T11:01:56.160Z",
            "last_updated": "2023-06-23T11:04:55.366Z",
            "custom_field_data": {},
            "transform_map": 5,
            "source_model": 43,
            "target_field": "platform",
            "coalesce": False,
            "template": None,
        },
    },
    {
        "model": "ipfabric_netbox.ipfabricrelationshipfield",
        "pk": 4,
        "fields": {
            "created": "2023-06-23T11:05:37.165Z",
            "last_updated": "2023-06-23T11:05:37.165Z",
            "custom_field_data": {},
            "transform_map": 5,
            "source_model": 56,
            "target_field": "site",
            "coalesce": False,
            "template": None,
        },
    },
    {
        "model": "ipfabric_netbox.ipfabricrelationshipfield",
        "pk": 5,
        "fields": {
            "created": "2023-06-23T11:07:26.908Z",
            "last_updated": "2023-06-23T11:07:26.908Z",
            "custom_field_data": {},
            "transform_map": 5,
            "source_model": 35,
            "target_field": "device_type",
            "coalesce": False,
            "template": None,
        },
    },
    {
        "model": "ipfabric_netbox.ipfabricrelationshipfield",
        "pk": 6,
        "fields": {
            "created": "2023-06-23T11:11:42.914Z",
            "last_updated": "2023-06-23T11:11:42.914Z",
            "custom_field_data": {},
            "transform_map": 5,
            "source_model": 34,
            "target_field": "device_role",
            "coalesce": False,
            "template": None,
        },
    },
    {
        "model": "ipfabric_netbox.ipfabricrelationshipfield",
        "pk": 7,
        "fields": {
            "created": "2023-06-23T13:42:05.285Z",
            "last_updated": "2023-06-23T13:42:05.285Z",
            "custom_field_data": {},
            "transform_map": 3,
            "source_model": 42,
            "target_field": "manufacturer",
            "coalesce": False,
            "template": None,
        },
    },
    {
        "model": "ipfabric_netbox.ipfabricrelationshipfield",
        "pk": 9,
        "fields": {
            "created": "2023-06-23T14:17:57.664Z",
            "last_updated": "2023-06-23T14:17:57.664Z",
            "custom_field_data": {},
            "transform_map": 4,
            "source_model": 42,
            "target_field": "manufacturer",
            "coalesce": False,
            "template": None,
        },
    },
    {
        "model": "ipfabric_netbox.ipfabricrelationshipfield",
        "pk": 22,
        "fields": {
            "created": "2023-08-09T12:39:35.028Z",
            "last_updated": "2023-08-09T12:39:35.028Z",
            "custom_field_data": {},
            "transform_map": 5,
            "source_model": 58,
            "target_field": "virtual_chassis",
            "coalesce": False,
            "template": "{% if object.virtual_chassis is defined %}{{ dcim.VirtualChassis.objects.filter(name=object.virtual_chassis.master).first().pk }}{% endif %}",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabricrelationshipfield",
        "pk": 11,
        "fields": {
            "created": "2023-06-28T11:00:44.494Z",
            "last_updated": "2023-06-28T14:37:54.113Z",
            "custom_field_data": {},
            "transform_map": 10,
            "source_model": 31,
            "target_field": "device",
            "coalesce": True,
            "template": None,
        },
    },
    {
        "model": "ipfabric_netbox.ipfabricrelationshipfield",
        "pk": 12,
        "fields": {
            "created": "2023-06-28T15:19:18.237Z",
            "last_updated": "2023-06-28T15:19:18.237Z",
            "custom_field_data": {},
            "transform_map": 11,
            "source_model": 42,
            "target_field": "manufacturer",
            "coalesce": False,
            "template": None,
        },
    },
    {
        "model": "ipfabric_netbox.ipfabricrelationshipfield",
        "pk": 13,
        "fields": {
            "created": "2023-06-28T15:19:35.397Z",
            "last_updated": "2023-07-14T14:15:42.974Z",
            "custom_field_data": {},
            "transform_map": 11,
            "source_model": 31,
            "target_field": "device",
            "coalesce": False,
            "template": None,
        },
    },
    {
        "model": "ipfabric_netbox.ipfabricrelationshipfield",
        "pk": 14,
        "fields": {
            "created": "2023-07-14T15:39:27.858Z",
            "last_updated": "2023-07-14T15:39:27.858Z",
            "custom_field_data": {},
            "transform_map": 12,
            "source_model": 56,
            "target_field": "site",
            "coalesce": True,
            "template": None,
        },
    },
    {
        "model": "ipfabric_netbox.ipfabricrelationshipfield",
        "pk": 23,
        "fields": {
            "created": "2023-08-15T14:48:42.409Z",
            "last_updated": "2023-08-15T20:24:33.161Z",
            "custom_field_data": {},
            "transform_map": 16,
            "source_model": 5,
            "target_field": "assigned_object_type",
            "coalesce": False,
            "template": '{{ contenttypes.ContentType.objects.get(app_label="dcim", model="interface").pk }}',
        },
    },
    {
        "model": "ipfabric_netbox.ipfabricrelationshipfield",
        "pk": 24,
        "fields": {
            "created": "2023-08-15T21:44:41.058Z",
            "last_updated": "2023-08-15T21:47:26.684Z",
            "custom_field_data": {},
            "transform_map": 16,
            "source_model": 73,
            "target_field": "vrf",
            "coalesce": False,
            "template": "{{ ipam.VRF.objects.filter(name=object.vrf).first().pk }}",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabricrelationshipfield",
        "pk": 15,
        "fields": {
            "created": "2023-07-18T09:40:50.275Z",
            "last_updated": "2023-08-15T21:53:36.179Z",
            "custom_field_data": {},
            "transform_map": 14,
            "source_model": 56,
            "target_field": "site",
            "coalesce": True,
            "template": "{% set SLUG = object.siteName | slugify %}\r\n{{ dcim.Site.objects.filter(slug=SLUG).first().pk }}",
        },
    },
    {
        "model": "ipfabric_netbox.ipfabricrelationshipfield",
        "pk": 17,
        "fields": {
            "created": "2023-07-18T21:19:36.757Z",
            "last_updated": "2023-07-18T21:19:44.148Z",
            "custom_field_data": {},
            "transform_map": 14,
            "source_model": 73,
            "target_field": "vrf",
            "coalesce": True,
            "template": "{{ ipam.VRF.objects.filter(name=object.vrf).first().pk }}",
        },
    },
]


class IPFabricTransformMapModelTestCase(TestCase):
    def setUp(self):
        deserialized_tm = serializers.deserialize("json", json.dumps(transform_maps))
        for deserialized_object in deserialized_tm:
            deserialized_object.save()

        deserialized_tf = serializers.deserialize("json", json.dumps(transform_fields))
        for deserialized_object in deserialized_tf:
            deserialized_object.save()

        deserialized_trf = serializers.deserialize(
            "json", json.dumps(transform_relationship_fields)
        )
        for deserialized_object in deserialized_trf:
            deserialized_object.save()

        source = IPFabricSource.objects.create(
            name="test",
            url="https://localhost",
            status="new",
            parameters={"auth": "token123", "verify": True},
        )
        snapshot = IPFabricSnapshot.objects.create(
            name="S01 - Day 2 - IPF Lab - 02-Jul-21 06:29:16 - 12dd8c61-129c-431a-b98b-4c9211571f89",
            source=source,
            snapshot_id="12dd8c61-129c-431a-b98b-4c9211571f89",
            data={
                "end": "2021-07-02T06:29:16.311000Z",
                "name": "S01 - Day 2 - IPF Lab",
                "note": "Multi-Environment containing:\\nAWS, Azure, ACI, NSX-T, Viptela, Versa, SilverPeak, Meraki\\n\\nSite 48 - devices added, NTP issue\\nSite 68 &38 - NTP update\\nSite 38 - resiliency affected (no ospfx2 - no L1 link x1) + passive interfaces FIXED / NTP partial update\\n?E2E: 38 - 66 - migration HTTP to HTTPS\\n?Site 66 - FW bypass E2E\\nVRRP improvements (LAB1 / L52)",
                "sites": [
                    "35COLO",
                    "35HEADOFFICE",
                    "35PRODUCTION",
                    "35SALES",
                    "38 Pilsen DR",
                    "66 Ostrava DC",
                    "68 Pardubice Distribution",
                    "ACI",
                    "AWS_SITE",
                    "AZURE",
                    "HWLAB",
                    "L31",
                    "L33",
                    "L34",
                    "L35",
                    "L36",
                    "L37",
                    "L39",
                    "L43",
                    "L45",
                    "L46",
                    "L47",
                    "L48",
                    "L49",
                    "L51",
                    "L52",
                    "L62",
                    "L63",
                    "L64",
                    "L65",
                    "L67",
                    "L71",
                    "L72",
                    "L77",
                    "L81",
                    "LAB01",
                    "MERAKI_SITE",
                    "MPLS",
                    "NSX-T",
                    "SILVERPEAK",
                    "VERSA_SITE",
                    "VIPTELA",
                ],
                "start": "2021-07-02T06:00:00.930000Z",
                "change": "2022-03-25T14:35:48.277000Z",
                "errors": [
                    {"count": 2, "error_type": "ABMapResultError"},
                    {"count": 5, "error_type": "ABParseError"},
                    {"count": 3, "error_type": "ABTaskMapResultError"},
                    {"count": 1, "error_type": "ABAmbiguousCommand"},
                    {"count": 7, "error_type": "ABCmdAuthFail"},
                    {"count": 6, "error_type": "ABCommandTimeout"},
                    {"count": 1, "error_type": "ABNoConfig"},
                    {"count": 1, "error_type": "ABParseBadConfigError"},
                    {"count": 1, "error_type": "ABTaskMapResultBadConfigError"},
                    {"count": 1, "error_type": "ABWorkerAuthError"},
                ],
                "locked": False,
                "status": "done",
                "loading": False,
                "version": "6.3.0-13",
                "user_count": 2324,
                "loaded_size": 170856074,
                "snapshot_id": "12dd8c61-129c-431a-b98b-4c9211571f89",
                "from_archive": True,
                "finish_status": "done",
                "unloaded_size": 26914884,
                "initial_version": "4.4.3+2",
                "interface_count": 9608,
                "total_dev_count": 729,
                "creator_username": None,
                "device_added_count": 0,
                "licensed_dev_count": 720,
                "device_removed_count": 0,
                "disabled_graph_cache": False,
                "interface_edge_count": 534,
                "interface_active_count": 6379,
                "disabled_historical_data": False,
                "disabled_intent_verification": False,
            },
            last_updated=timezone.now(),
        )
        sync = IPFabricSync.objects.create(
            name="ingest",
            type="dcim",
            status="new",
            snapshot_data=snapshot,
            parameters={
                "vrf": False,
                "site": True,
                "vlan": False,
                "sites": [],
                "device": True,
                "prefix": False,
                "platform": True,
                "interface": False,
                "ipaddress": False,
                "devicerole": True,
                "devicetype": True,
                "manufacturer": True,
                "virtualchassis": False,
            },
        )

        runner = IPFabricSyncRunner(
            transform_map=IPFabricTransformMap,
            settings={
                "site": True,
                "sites": [],
                "device": True,
                "platform": True,
                "interface": False,
                "devicerole": True,
                "devicetype": True,
                "manufacturer": True,
                "virtualchassis": True,
                "snapshot_id": "12dd8c61-129c-431a-b98b-4c9211571f89",
            },
            sync=sync,
        )
        device_uuid = str(uuid.uuid4())

        site_data = {
            "siteName": "Site 1",
            "devicesCount": 1,
            "usersCount": 2,
            "stpDCount": 0,
            "switchesCount": 0,
            "vlanCount": 1,
            "rDCount": 0,
            "routersCount": 0,
            "networksCount": 6,
        }

        self.site = runner.get_model_or_update(
            "dcim", "site", site_data, uuid=device_uuid
        )

        device_data = {
            "id": "961251111",
            "configReg": "0x0",
            "devType": "router",
            "family": "ios",
            "hostname": "L21PE152",
            "hostnameOriginal": None,
            "hostnameProcessed": None,
            "domain": None,
            "fqdn": None,
            "icon": None,
            "image": "unix:/opt/unetlab/addons/iol/bin/i86bi-linux-l3-adventerprisek9-15.2",
            "objectId": None,
            "taskKey": "fb67e3b4-5e48-4e52-b000-56cb187f2852",
            "loginIp": "10.21.254.152",
            "loginType": "telnet",
            "loginPort": None,
            "mac": None,
            "memoryTotalBytes": 396008048,
            "memoryUsedBytes": 72264172,
            "memoryUtilization": 18.25,
            "model": "",
            "platform": "i86bi_linux",
            "processor": "Intel-x86",
            "rd": "3",
            "reload": "reload at 0",
            "siteName": "MPLS",
            "sn": "a15ff98",
            "snHw": "a15ff98",
            "stpDomain": None,
            "uptime": 7254180,
            "vendor": "cisco",
            "version": "15.2(4)M1",
            "slug": None,
        }

        self.mf_obj = runner.get_model_or_update(
            "dcim", "manufacturer", device_data, uuid=device_uuid
        )
        self.dt_obj = runner.get_model_or_update(
            "dcim", "devicetype", device_data, uuid=device_uuid
        )

        self.platform = runner.get_model_or_update(
            "dcim", "platform", device_data, uuid=device_uuid
        )

        self.device_role = runner.get_model_or_update(
            "dcim", "devicerole", device_data, uuid=device_uuid
        )

        self.device_object = runner.get_model_or_update(
            "dcim", "device", device_data, uuid=device_uuid
        )

    def test_transform_map(self):
        site_transform_map = IPFabricTransformMap.objects.get(name="Site Transform Map")
        self.assertEqual(site_transform_map.name, "Site Transform Map")
        self.assertEqual(site_transform_map.source_model, "site")
        self.assertEqual(site_transform_map.status, "active")
        self.assertEqual(
            site_transform_map.target_model,
            ContentType.objects.filter(app_label="dcim", model="site")[0],
        )

    def test_transform_field(self):
        site_transform_map = IPFabricTransformMap.objects.get(name="Site Transform Map")
        site_slug_field = IPFabricTransformField.objects.get(
            source_field="siteName",
            target_field="slug",
            transform_map=site_transform_map,
        )
        self.assertEqual(site_slug_field.source_field, "siteName")
        self.assertEqual(site_slug_field.target_field, "slug")
        self.assertEqual(site_slug_field.template, "{{ object.siteName | slugify }}")
        self.assertEqual(site_slug_field.transform_map, site_transform_map)
        site_name_field = IPFabricTransformField.objects.get(
            source_field="siteName",
            target_field="name",
            transform_map=site_transform_map,
        )
        self.assertEqual(site_name_field.source_field, "siteName")
        self.assertEqual(site_name_field.target_field, "name")
        self.assertEqual(site_name_field.template, "")
        self.assertEqual(site_name_field.transform_map, site_transform_map)

    def test_transform_map_serialization(self):
        site_transform_map = IPFabricTransformMap.objects.get(name="Site Transform Map")
        data = serializers.serialize("json", [site_transform_map])
        data = json.loads(data)[0]
        test_data = {
            "model": "ipfabric_netbox.ipfabrictransformmap",
            "pk": site_transform_map.pk,
            "fields": {
                "name": "Site Transform Map",
                "source_model": "site",
                "target_model": 56,
                "status": "active",
            },
        }
        new_data = copy.deepcopy(data)
        new_data.pop("fields")
        new_fields = {}
        for k in test_data["fields"]:
            new_fields[k] = data["fields"][k]
        new_data["fields"] = new_fields
        self.assertDictEqual(test_data, new_data)

    def test_transform_field_serialization(self):
        site_transform_map = IPFabricTransformMap.objects.get(name="Site Transform Map")
        site_slug_field = IPFabricTransformField.objects.get(
            source_field="siteName", target_field="slug"
        )
        data = serializers.serialize("json", [site_slug_field])
        data = json.loads(data)[0]
        test_data = {
            "model": "ipfabric_netbox.ipfabrictransformfield",
            "pk": site_slug_field.pk,
            "fields": {
                "source_field": "siteName",
                "target_field": "slug",
                "template": "{{ object.siteName | slugify }}",
                "transform_map": site_transform_map.pk,
            },
        }
        new_data = copy.deepcopy(data)
        new_data.pop("fields")
        new_data["fields"] = {k: data["fields"][k] for k in test_data["fields"]}
        self.assertDictEqual(test_data, new_data)

    def test_update_or_create_instance_site(self):
        site_transform_map = IPFabricTransformMap.objects.get(name="Site Transform Map")
        data = {
            "siteName": "Site 1",
            "devicesCount": 1,
            "usersCount": 2,
            "stpDCount": 0,
            "switchesCount": 0,
            "vlanCount": 1,
            "rDCount": 0,
            "routersCount": 0,
            "networksCount": 6,
        }
        object = site_transform_map.update_or_create_instance(data=data)
        self.assertEqual(object.name, "Site 1")
        self.assertEqual(object.slug, "site-1")

    def test_update_or_create_instance_device(self):
        device_object = Device.objects.first()

        self.assertEqual(device_object.name, "L21PE152")
        self.assertEqual(device_object.serial, "a15ff98")
        self.assertEqual(device_object.platform, self.platform)
        self.assertEqual(device_object.device_role, self.device_role)
        self.assertEqual(device_object.device_type, self.dt_obj)
        self.assertEqual(device_object.device_type.manufacturer, self.mf_obj)
        self.assertEqual(device_object.site, self.site)
        self.assertEqual(device_object.status, "active")

    def test_alter_transform_field_template(self):
        sync = IPFabricSync.objects.get(name="ingest")

        runner = IPFabricSyncRunner(
            transform_map=IPFabricTransformMap,
            settings={
                "site": True,
                "sites": [],
                "device": True,
                "platform": True,
                "interface": False,
                "devicerole": True,
                "devicetype": True,
                "manufacturer": True,
                "virtualchassis": True,
                "snapshot_id": "12dd8c61-129c-431a-b98b-4c9211571f89",
            },
            sync=sync,
        )
        device_uuid = str(uuid.uuid4())

        device_data = {
            "id": "961251111",
            "configReg": "0x0",
            "devType": "router",
            "family": "ios",
            "hostname": "L21PE152",
            "hostnameOriginal": None,
            "hostnameProcessed": None,
            "domain": None,
            "fqdn": None,
            "icon": None,
            "image": "unix:/opt/unetlab/addons/iol/bin/i86bi-linux-l3-adventerprisek9-15.2",
            "objectId": None,
            "taskKey": "fb67e3b4-5e48-4e52-b000-56cb187f2852",
            "loginIp": "10.21.254.152",
            "loginType": "telnet",
            "loginPort": None,
            "mac": None,
            "memoryTotalBytes": 396008048,
            "memoryUsedBytes": 72264172,
            "memoryUtilization": 18.25,
            "model": "",
            "platform": "i86bi_linux",
            "processor": "Intel-x86",
            "rd": "3",
            "reload": "reload at 0",
            "siteName": "MPLS",
            "sn": "a15ff98",
            "snHw": "a15ff98",
            "stpDomain": None,
            "uptime": 7254180,
            "vendor": "cisco",
            "version": "15.2(4)M1",
            "slug": None,
        }

        transform_field = IPFabricTransformField.objects.get(pk=10)
        transform_field.template = "{{ object.hostname }} - test"
        transform_field.save()
        device_object = runner.get_model_or_update(
            "dcim", "device", device_data, uuid=device_uuid
        )
        self.assertEqual(device_object.name, "L21PE152 - test")
