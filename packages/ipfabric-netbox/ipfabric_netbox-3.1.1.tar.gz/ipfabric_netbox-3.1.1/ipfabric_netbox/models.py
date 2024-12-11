import ast
import json
import logging
import traceback
from copy import deepcopy

import httpx
from core.choices import DataSourceStatusChoices
from core.exceptions import SyncError
from core.models import Job
from core.signals import handle_deleted_object
from core.signals import pre_sync
from dcim.models import VirtualChassis
from dcim.signals import assign_virtualchassis_master
from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core.validators import MinValueValidator
from django.db import models
from django.db import transaction
from django.db.models import Q
from django.db.models import signals
from django.urls import reverse
from django.utils import timezone
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _
from extras.models import Branch
from extras.models import StagedChange
from netbox.models import ChangeLoggedModel
from netbox.models import NetBoxModel
from netbox.models import PrimaryModel
from netbox.models.features import JobsMixin
from netbox.models.features import TagsMixin
from netbox.registry import registry
from netbox.staging import checkout
from utilities.data import shallow_compare_dict
from utilities.querysets import RestrictedQuerySet
from utilities.serialization import serialize_object

from .choices import IPFabricRawDataTypeChoices
from .choices import IPFabricSnapshotStatusModelChoices
from .choices import IPFabricSourceTypeChoices
from .choices import IPFabricSyncTypeChoices
from .choices import IPFabricTransformMapSourceModelChoices
from .utilities.ipfutils import IPFabric
from .utilities.ipfutils import IPFabricSyncRunner
from .utilities.ipfutils import render_jinja2
from .utilities.logging import SyncLogging


logger = logging.getLogger("ipfabric_netbox.models")


def apply_tags(object, tags):
    def _apply(object):
        for tag in tags:
            if hasattr(object, "tags"):
                object.tags.add(tag)
        object.save()

    _apply(object)


IPFabricSupportedSyncModels = Q(
    Q(app_label="dcim", model="site")
    | Q(app_label="dcim", model="manufacturer")
    | Q(app_label="dcim", model="platform")
    | Q(app_label="dcim", model="devicerole")
    | Q(app_label="dcim", model="devicetype")
    | Q(app_label="dcim", model="device")
    | Q(app_label="dcim", model="virtualchassis")
    | Q(app_label="dcim", model="interface")
    | Q(app_label="ipam", model="vlan")
    | Q(app_label="ipam", model="vrf")
    | Q(app_label="ipam", model="prefix")
    | Q(app_label="ipam", model="ipaddress")
    | Q(app_label="contenttypes", model="contenttype")
    | Q(app_label="tenancy", model="tenant")
    | Q(app_label="dcim", model="inventoryitem")
)


IPFabricRelationshipFieldSourceModels = Q(
    Q(app_label="dcim")
    | Q(app_label="ipam")
    | Q(app_label="tenancy")
    | Q(app_label="contenttypes", model="contenttype")
)


class IPFabricTransformMap(NetBoxModel):
    name = models.CharField(max_length=100, unique=True)
    source_model = models.CharField(
        max_length=50, choices=IPFabricTransformMapSourceModelChoices
    )
    target_model = models.ForeignKey(
        to=ContentType,
        related_name="+",
        verbose_name="Target Model",
        limit_choices_to=IPFabricSupportedSyncModels,
        help_text=_("The object(s) to which transform map target applies."),
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )
    status = models.CharField(
        max_length=50,
    )

    class Meta:
        verbose_name = "IP Fabric Transform Map"
        verbose_name_plural = "IP Fabric Transform Maps"

    def __str__(self):
        if self.source_model and self.target_model:
            return f"{self.source_model} - {self.target_model}"
        else:
            return "Transform Map"

    def get_absolute_url(self):
        return reverse("plugins:ipfabric_netbox:ipfabrictransformmap", args=[self.pk])

    @property
    def docs_url(self):
        # TODO: Add docs url
        return ""

    def get_models(self):
        _context = dict()

        for app, model_names in registry["model_features"]["custom_fields"].items():
            _context.setdefault(app, {})
            for model_name in model_names:
                model = apps.get_registered_model(app, model_name)
                _context[app][model.__name__] = model
        _context["contenttypes"] = {}
        _context["contenttypes"]["ContentType"] = ContentType
        return _context

    def build_relationships(self, uuid, source_data):
        relationship_maps = self.relationship_maps.all()
        rel_dict = {}
        rel_dict_coalesce = {}

        for field in relationship_maps:
            if field.template:
                context = {
                    "object": source_data,
                }
                context.update(self.get_models())
                text = render_jinja2(field.template, context).strip()
                if text:
                    try:
                        pk = int(text)
                    except ValueError:
                        pk = text

                    if isinstance(pk, int):
                        related_object = field.source_model.model_class().objects.get(
                            pk=pk
                        )
                    else:
                        related_object = ast.literal_eval(pk)

                    if not field.coalesce:
                        rel_dict[field.target_field] = related_object
                    else:
                        rel_dict_coalesce[field.target_field] = related_object
            elif uuid and self.relationship_store.get(uuid):
                object = self.relationship_store[uuid].get(
                    field.source_model.model_class()
                )
                if object:
                    if not field.coalesce:
                        rel_dict[field.target_field] = object
                    else:
                        rel_dict_coalesce[field.target_field] = object

        return rel_dict, rel_dict_coalesce

    def update_or_create_instance(
        self, data, tags=[], uuid=None, relationship_store={}, logger=None
    ):
        self.relationship_store = relationship_store
        new_data = deepcopy(data)
        relationship, coalesce_relationship = self.build_relationships(
            uuid=uuid, source_data=data
        )
        if relationship:
            new_data["relationship"] = relationship
        if coalesce_relationship:
            new_data["relationship_coalesce"] = coalesce_relationship
        context = self.render(new_data)
        try:
            instance, _ = self.target_model.model_class().objects.update_or_create(
                **context
            )
            if instance:
                apply_tags(instance, tags)
        except Exception as e:
            error_message = f"""Failed to create instance:<br/>
            message: `{e}`<br/>
            raw data: `{data}`<br/>
            context: `{context}`<br/>
            """
            logger.log_failure(error_message, obj=self)
            logger.log_failure(
                "Ensure that all transform map fields are present.", obj=self
            )
            raise SyncError("Unable to update_or_create_instance.")

        return instance

    def get_coalesce_fields(self, source_data):
        data = self.render(source_data)
        del data["defaults"]
        return data

    def render(self, source_data):
        data = {"defaults": {}}
        for field in self.field_maps.all():
            if field.template:
                context = {
                    "object": source_data,
                    field.source_field: source_data[field.source_field],
                }
                context.update(self.get_models())
                text = render_jinja2(field.template, context).strip()
            else:
                text = source_data[field.source_field]

            if text is not None:
                if isinstance(text, str):
                    if text.lower() in ["true"]:
                        text = True
                    elif text.lower() in ["false"]:
                        text = False
                    elif text.lower() in ["none"]:
                        text = None

                    if text:
                        target_field = getattr(
                            self.target_model.model_class(), field.target_field
                        )
                        target_field_type = target_field.field.get_internal_type()
                        if "integer" in target_field_type.lower():
                            text = int(text)

            if not field.coalesce:
                data["defaults"][field.target_field] = text
            else:
                data[field.target_field] = text

        if relationship := source_data.get("relationship"):
            data["defaults"].update(relationship)

        if relationship_coalesce := source_data.get("relationship_coalesce"):
            data.update(relationship_coalesce)

        if self.status:
            data["defaults"]["status"] = self.status

        return data


class IPFabricRelationshipField(models.Model):
    transform_map = models.ForeignKey(
        to=IPFabricTransformMap,
        on_delete=models.CASCADE,
        related_name="relationship_maps",
        editable=True,
    )
    source_model = models.ForeignKey(
        ContentType,
        related_name="ipfabric_transform_fields",
        limit_choices_to=IPFabricRelationshipFieldSourceModels,
        verbose_name="Source Model",
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )
    target_field = models.CharField(max_length=100)
    coalesce = models.BooleanField(default=False)
    template = models.TextField(
        help_text=_(
            "Jinja2 template code, return an integer to create a relationship between the source and target model. True, False and None are also supported."
        ),
        blank=True,
        null=True,
    )

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        ordering = ("transform_map",)
        verbose_name = "IP Fabric Relationship Field"
        verbose_name_plural = "IP Fabric Relationship Fields"

    @property
    def docs_url(self):
        # TODO: Add docs url
        return ""


class IPFabricTransformField(models.Model):
    transform_map = models.ForeignKey(
        to=IPFabricTransformMap,
        on_delete=models.CASCADE,
        related_name="field_maps",
        editable=True,
    )
    source_field = models.CharField(max_length=100)
    target_field = models.CharField(max_length=100)
    coalesce = models.BooleanField(default=False)

    objects = RestrictedQuerySet.as_manager()

    template = models.TextField(
        help_text=_("Jinja2 template code to be rendered into the target field."),
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("transform_map",)
        verbose_name = "IP Fabric Transform Field"
        verbose_name_plural = "IP Fabric Transform Fields"

    @property
    def docs_url(self):
        # TODO: Add docs url
        return ""


class IPFabricClient:
    def get_client(self, parameters, transform_map=None):
        try:
            if transform_map:
                ipf = IPFabric(parameters=parameters, transform_map=transform_map)
            else:
                ipf = IPFabric(parameters=parameters)
            return ipf.ipf
        except httpx.ConnectError as e:
            if "CERTIFICATE_VERIFY_FAILED" in str(e):
                error_message = (
                    "SSL certificate verification failed, self-signed cert? "
                    "<a href='https://docs.ipfabric.io/main/integrations/netbox-plugin/user_guide/10_FAQ/' target='_blank'>Check out our FAQ documentation.</a>"
                )
            else:
                error_message = str(e)
            self.handle_sync_failure("ConnectError", e, error_message)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                error_message = "Authentication failed, check API key."
            else:
                error_message = str(e)
            self.handle_sync_failure("HTTPStatusError", e, error_message)
        except Exception as e:
            self.handle_sync_failure("Error", e)

    def handle_sync_failure(self, failure_type, exception, message=None):
        self.status = DataSourceStatusChoices.FAILED

        if message:
            self.logger.log_failure(
                f"{message} ({failure_type}): `{exception}`", obj=self
            )
        else:
            self.logger.log_failure(f"Syncing Snapshot Failed: `{exception}`", obj=self)


class IPFabricSource(IPFabricClient, JobsMixin, PrimaryModel):
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(
        verbose_name=_("type"),
        max_length=50,
        choices=IPFabricSourceTypeChoices,
        default=IPFabricSourceTypeChoices.LOCAL,
    )
    url = models.CharField(max_length=200, verbose_name=_("URL"))
    status = models.CharField(
        max_length=50,
        choices=DataSourceStatusChoices,
        default=DataSourceStatusChoices.NEW,
        editable=False,
    )
    parameters = models.JSONField(blank=True, null=True)
    last_synced = models.DateTimeField(blank=True, null=True, editable=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "IP Fabric Source"
        verbose_name_plural = "IP Fabric Sources"

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("plugins:ipfabric_netbox:ipfabricsource", args=[self.pk])

    @property
    def ready_for_sync(self):
        return self.status not in (
            DataSourceStatusChoices.QUEUED,
            DataSourceStatusChoices.SYNCING,
        )

    @property
    def docs_url(self):
        # TODO: Add docs url
        return ""

    def clean(self):
        super().clean()

        self.url = self.url.rstrip("/")

    def enqueue_sync_job(self, request):
        # Set the status to "syncing"
        self.status = DataSourceStatusChoices.QUEUED
        IPFabricSource.objects.filter(pk=self.pk).update(status=self.status)

        # Enqueue a sync job
        return Job.enqueue(
            import_string("ipfabric_netbox.jobs.sync_ipfabricsource"),
            name=f"{self.name} Snapshot Sync",
            instance=self,
            user=request.user,
        )

    def sync(self, job):
        self.logger = SyncLogging(job=job.pk)
        if self.status == DataSourceStatusChoices.SYNCING:
            self.logger.log_failure(
                "Cannot initiate sync; syncing already in progress.", obj=self
            )
            raise SyncError("Cannot initiate sync; syncing already in progress.")

        pre_sync.send(sender=self.__class__, instance=self)

        self.status = DataSourceStatusChoices.SYNCING
        IPFabricSource.objects.filter(pk=self.pk).update(status=self.status)

        # Begin Sync
        try:
            self.logger.log_info(f"Syncing snapshots from {self.name}", obj=self)
            logger.debug(f"Syncing snapshots from {self.url}")

            self.parameters["base_url"] = self.url
            ipf = self.get_client(parameters=self.parameters)

            if not ipf:
                raise SyncError("Unable to connect to IP Fabric.")

            for snapshot_id, value in ipf.snapshots.items():
                if snapshot_id not in ["$prev", "$lastLocked"]:
                    if value.name:
                        name = (
                            value.name
                            + " - "
                            + value.start.strftime("%d-%b-%y %H:%M:%S")
                        )
                    else:
                        name = value.start.strftime("%d-%b-%y %H:%M:%S")

                    if value.status == "done":
                        status = "loaded"
                    else:
                        status = value.status

                    data = {
                        "name": name,
                        "data": json.loads(value.model_dump_json(exclude={"client"})),
                        "date": value.start,
                        "created": timezone.now(),
                        "last_updated": timezone.now(),
                        "status": status,
                    }
                    snapshot, _ = IPFabricSnapshot.objects.update_or_create(
                        source=self, snapshot_id=snapshot_id, defaults=data
                    )
                    self.logger.log_info(
                        f"Created/Updated Snapshot {snapshot.name} ({snapshot.snapshot_id})",
                        obj=snapshot,
                    )
            self.status = DataSourceStatusChoices.COMPLETED
            self.logger.log_success(f"Completed syncing snapshots from {self.name}")
            logger.debug(f"Completed syncing snapshots from {self.url}")
        except Exception as e:
            self.handle_sync_failure(type(e).__name__, e)
        finally:
            self.last_synced = timezone.now()
            IPFabricSource.objects.filter(pk=self.pk).update(
                status=self.status, last_synced=self.last_synced
            )
            self.logger.log_info("Sync job completed.", obj=self)
            if job:
                job.data = self.logger.log_data
        # Emit the post_sync signal
        # post_sync.send(sender=self.__class__, instance=self)


class IPFabricSnapshot(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(editable=False)
    source = models.ForeignKey(
        to=IPFabricSource,
        on_delete=models.CASCADE,
        related_name="snapshots",
        editable=False,
    )
    name = models.CharField(max_length=200)
    snapshot_id = models.CharField(max_length=100)
    data = models.JSONField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True, editable=False)
    status = models.CharField(
        max_length=50,
        choices=IPFabricSnapshotStatusModelChoices,
        default=IPFabricSnapshotStatusModelChoices.STATUS_UNLOADED,
    )

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        ordering = ("source", "-date")
        verbose_name = "IP Fabric Snapshot"
        verbose_name_plural = "IP Fabric Snapshots"

    def __str__(self):
        return f"{self.name} - {self.snapshot_id}"

    def get_absolute_url(self):
        return reverse("plugins:ipfabric_netbox:ipfabricsnapshot", args=[self.pk])

    def get_status_color(self):
        return IPFabricSnapshotStatusModelChoices.colors.get(self.status)

    @property
    def sites(self):
        if self.data:
            sites = self.data.get("sites", None)
            if sites:
                return sites
            else:
                return []
        else:
            return []


class IPFabricSync(IPFabricClient, JobsMixin, TagsMixin, ChangeLoggedModel):
    objects = RestrictedQuerySet.as_manager()
    name = models.CharField(max_length=100, unique=True)
    snapshot_data = models.ForeignKey(
        to=IPFabricSnapshot,
        on_delete=models.CASCADE,
        related_name="snapshots",
    )
    type = models.CharField(
        max_length=50,
        choices=IPFabricSyncTypeChoices,
        default=IPFabricSyncTypeChoices.DCIM,
    )
    status = models.CharField(
        max_length=50,
        choices=DataSourceStatusChoices,
        default=DataSourceStatusChoices.NEW,
        editable=False,
    )
    parameters = models.JSONField(blank=True, null=True)
    auto_merge = models.BooleanField(default=False)
    last_synced = models.DateTimeField(blank=True, null=True, editable=False)
    scheduled = models.DateTimeField(null=True, blank=True)
    interval = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=(MinValueValidator(1),),
        help_text=_("Recurrence interval (in minutes)"),
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["pk"]
        verbose_name = "IP Fabric Sync"

    def __str__(self):
        return f"{self.name}"

    @property
    def docs_url(self):
        # TODO: Add docs url
        return ""

    def get_absolute_url(self):
        return reverse("plugins:ipfabric_netbox:ipfabricsync", args=[self.pk])

    def get_status_color(self):
        return DataSourceStatusChoices.colors.get(self.status)

    @property
    def ready_for_sync(self):
        if self.status not in (DataSourceStatusChoices.SYNCING,):
            if self.snapshot_data.source.type == "remote":
                if self.snapshot_data.ipf_data.count() > 0:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    def enqueue_sync_job(self, adhoc=False, user=None):
        # Set the status to "syncing"
        self.status = DataSourceStatusChoices.QUEUED
        IPFabricSync.objects.filter(pk=self.pk).update(status=self.status)

        Job.enqueue(
            import_string("ipfabric_netbox.jobs.sync_ipfabricsource"),
            name=f"{self.name} Snapshot Sync (Pre Ingestion)",
            instance=self.snapshot_data.source,
            user=self.user,
        )

        # Enqueue a sync job
        if not user:
            user = self.user

        if not adhoc and self.scheduled:
            job = Job.enqueue(
                import_string("ipfabric_netbox.jobs.sync_ipfabric"),
                name=f"{self.name} - (scheduled)",
                instance=self,
                user=self.user,
                schedule_at=self.scheduled,
                interval=self.interval,
            )
        elif adhoc:
            job = Job.enqueue(
                import_string("ipfabric_netbox.jobs.sync_ipfabric"),
                instance=self,
                user=user,
                name=f"{self.name} - (adhoc)",
                adhoc=adhoc,
            )
        return job

    def sync(self, job=None):
        if job:
            self.logger = SyncLogging(job=job.pk)
            user = job.user
        else:
            self.logger = SyncLogging(job=self.pk)
            user = None

        if self.status == DataSourceStatusChoices.SYNCING:
            raise SyncError("Cannot initiate sync; ingestion already in progress.")

        pre_sync.send(sender=self.__class__, instance=self)

        self.status = DataSourceStatusChoices.SYNCING
        IPFabricSync.objects.filter(pk=self.pk).update(status=self.status)

        # Begin Sync
        self.logger.log_info(
            f"Ingesting data from {self.snapshot_data.source.name}", obj=self
        )
        logger.info(f"Ingesting data from {self.snapshot_data.source.name}")

        self.snapshot_data.source.parameters["base_url"] = self.snapshot_data.source.url
        self.parameters["snapshot_id"] = self.snapshot_data.snapshot_id
        self.logger.log_info(
            f"Syncing with the following data {json.dumps(self.parameters)}", obj=self
        )
        logger.info(f"Syncing with the following data {json.dumps(self.parameters)}")

        current_time = str(timezone.now())

        branch = IPFabricBranch.objects.create(
            name=f"{current_time}", sync=self, job=job, user=user
        )
        self.logger.log_info(f"New branch Created {branch.name}", obj=branch)
        logger.info(f"New branch Created {branch.name}")

        try:
            self.logger.log_info("Fetching IP Fabric Client", obj=branch)
            logger.info("Fetching IP Fabric Client")

            if self.snapshot_data.source.type == IPFabricSourceTypeChoices.LOCAL:
                ipf = self.get_client(
                    parameters=self.snapshot_data.source.parameters,
                    transform_map=IPFabricTransformMap,
                )
                if not ipf:
                    logger.debug("Unable to connect to IP Fabric.")
                    raise SyncError("Unable to connect to IP Fabric.")
            else:
                ipf = None

            runner = IPFabricSyncRunner(
                client=ipf,
                settings=self.parameters,
                transform_map=IPFabricTransformMap,
                sync=self,
            )

            with checkout(branch):
                runner.sync_devices(branch=branch)

            self.status = DataSourceStatusChoices.COMPLETED
        except Exception as e:
            self.status = DataSourceStatusChoices.FAILED
            self.logger.log_failure(f"Branch Failed: `{e}`", obj=branch)
            self.logger.log_failure(
                f"Stack Trace: `{traceback.format_exc()}`", obj=branch
            )
            logger.debug(f"Branch Failed: `{e}`")

        logger.debug(f"Completed ingesting data from {self.snapshot_data.source.name}")
        self.logger.log_info(
            f"Completed ingesting data from {self.snapshot_data.source.name}", obj=self
        )

        for change in branch.staged_changes.all():
            if hasattr(change.object, "pk"):
                prechange_data = prechange_data = serialize_object(
                    change.object, resolve_tags=False
                )
                prechange_data = dict(sorted(prechange_data.items()))
            else:
                prechange_data = None
            if hasattr(change, "data"):
                postchange_data = dict(sorted(change.data.items()))

            diff_added = shallow_compare_dict(
                prechange_data or dict(),
                postchange_data or dict(),
                exclude=["last_updated"],
            )

            if not diff_added:
                change.delete()

        self.last_synced = timezone.now()

        if self.auto_merge and self.status == DataSourceStatusChoices.COMPLETED:
            self.logger.log_info("Auto Merging Branch", obj=branch)
            logger.info("Auto Merging Branch")
            branch.enqueue_merge_job(user=user)
            self.logger.log_info("Auto Merge Job Enqueued", obj=branch)
            logger.info("Auto Merge Job Enqueued")

        IPFabricSync.objects.filter(pk=self.pk).update(
            status=self.status, last_synced=self.last_synced
        )
        if job:
            job.data = self.logger.log_data


class IPFabricBranch(JobsMixin, Branch):
    """
    A collection of related StagedChanges.
    """

    sync = models.ForeignKey(IPFabricSync, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "IP Fabric Branch"
        verbose_name_plural = "IP Fabric Branches"

    def __str__(self):
        return f"{self.name} ({self.pk})"

    def get_absolute_url(self):
        return reverse("plugins:ipfabric_netbox:ipfabricbranch", args=[self.pk])

    def enqueue_merge_job(self, user):
        # Set the status to "syncing"
        self.status = DataSourceStatusChoices.QUEUED
        IPFabricSync.objects.filter(ipfabricbranch=self.pk).update(status=self.status)

        # Enqueue a sync job
        return Job.enqueue(
            import_string("ipfabric_netbox.jobs.merge_ipfabric_branch"),
            name=f"{self.name} Merge",
            instance=self,
            user=user,
        )

    def get_logs(self):
        if self.job.data:
            job_results = self.job.data
        else:
            job_results = cache.get(f"ipfabric_sync_{self.job.pk}")
            if not job_results:
                job_results = cache.get(f"ipfabric_sync_{self.sync.pk}")
        return job_results

    def get_statistics(self):
        job_results = self.get_logs()
        statistics = {}
        if job_results:
            for model, stats in job_results["statistics"].items():
                if stats["total"] > 0:
                    statistics[model] = stats["current"] / stats["total"] * 100
                else:
                    statistics[model] = stats["current"] / 1 * 100
        return {"job_results": job_results, "statistics": statistics}

    def merge(self):
        logger.info(f"Merging changes in branch {self}")
        with transaction.atomic():
            for change in self.staged_changes.all():
                logger.debug("Applying change: %s", change)
                change.apply()
        signals.pre_delete.disconnect(handle_deleted_object)
        self.staged_changes.all().delete()
        signals.pre_delete.connect(handle_deleted_object, sender=StagedChange)

    def sync_merge(self):
        ipfabricsync = self.sync
        if ipfabricsync.status == DataSourceStatusChoices.SYNCING:
            raise SyncError("Cannot initiate merge; merge already in progress.")

        pre_sync.send(sender=self.__class__, instance=self)

        ipfabricsync.status = DataSourceStatusChoices.SYNCING
        IPFabricSync.objects.filter(ipfabricbranch=self.pk).update(
            status=self.sync.status
        )

        # Begin Sync
        logger.debug(f"Merging {self.name}")
        try:
            signals.post_save.disconnect(
                assign_virtualchassis_master, sender=VirtualChassis
            )
            self.merge()
            signals.post_save.connect(
                assign_virtualchassis_master, sender=VirtualChassis
            )
            ipfabricsync.status = DataSourceStatusChoices.COMPLETED
        except Exception as e:
            ipfabricsync.status = DataSourceStatusChoices.FAILED
            logger.debug(f"Merging {self.name} Failed: `{e}`")

        logger.debug(f"Completed merge {self.name}")

        ipfabricsync.last_synced = timezone.now()
        IPFabricSync.objects.filter(ipfabricbranch=self.pk).update(
            status=ipfabricsync.status, last_synced=ipfabricsync.last_synced
        )


class IPFabricData(models.Model):
    snapshot_data = models.ForeignKey(
        to=IPFabricSnapshot,
        on_delete=models.CASCADE,
        related_name="ipf_data",
    )
    data = models.JSONField(blank=True, null=True)
    type = models.CharField(
        max_length=50,
        choices=IPFabricRawDataTypeChoices,
    )
    objects = RestrictedQuerySet.as_manager()
