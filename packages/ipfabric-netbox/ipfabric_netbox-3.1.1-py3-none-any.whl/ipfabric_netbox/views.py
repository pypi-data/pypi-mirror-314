import requests
from dcim.models import Device
from dcim.models import Site
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db import models
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import View
from django_tables2 import RequestConfig
from extras.choices import ChangeActionChoices
from ipfabric.diagrams import Network
from ipfabric.diagrams import NetworkSettings
from netbox.staging import StagedChange
from netbox.views import generic
from netbox.views.generic.base import BaseObjectView
from utilities.data import shallow_compare_dict
from utilities.forms import ConfirmationForm
from utilities.paginator import EnhancedPaginator
from utilities.paginator import get_paginate_count
from utilities.query import count_related
from utilities.serialization import serialize_object
from utilities.views import get_viewname
from utilities.views import register_model_view
from utilities.views import ViewTab

from .filtersets import IPFabricBranchFilterSet
from .filtersets import IPFabricDataFilterSet
from .filtersets import IPFabricSnapshotFilterSet
from .filtersets import IPFabricSourceFilterSet
from .filtersets import IPFabricStagedChangeFilterSet
from .forms import IPFabricBranchFilterForm
from .forms import IPFabricRelationshipFieldForm
from .forms import IPFabricSnapshotFilterForm
from .forms import IPFabricSourceFilterForm
from .forms import IPFabricSourceForm
from .forms import IPFabricSyncForm
from .forms import IPFabricTableForm
from .forms import IPFabricTransformFieldForm
from .forms import IPFabricTransformMapForm
from .models import IPFabricBranch
from .models import IPFabricData
from .models import IPFabricRelationshipField
from .models import IPFabricSnapshot
from .models import IPFabricSource
from .models import IPFabricSync
from .models import IPFabricTransformField
from .models import IPFabricTransformMap
from .tables import BranchTable
from .tables import DeviceIPFTable
from .tables import IPFabricDataTable
from .tables import IPFabricRelationshipFieldTable
from .tables import IPFabricSnapshotTable
from .tables import IPFabricSourceTable
from .tables import IPFabricTransformFieldTable
from .tables import IPFabricTransformMapTable
from .tables import StagedChangesTable
from .utilities.ipfutils import IPFabric
from .utilities.transform_map import BuildTransformMaps


# Transform Map Relationship Field


@register_model_view(IPFabricRelationshipField, "edit")
class IPFabricRelationshipFieldEditView(generic.ObjectEditView):
    queryset = IPFabricRelationshipField.objects.all()
    form = IPFabricRelationshipFieldForm
    default_return_url = "plugins:ipfabric_netbox:ipfabricrelationshipfield_list"


class IPFabricRelationshipFieldDeleteView(generic.ObjectDeleteView):
    queryset = IPFabricRelationshipField.objects.all()
    default_return_url = "plugins:ipfabric_netbox:ipfabricrelationshipfield_list"


@register_model_view(IPFabricTransformMap, "relationships")
class IPFabricTransformRelationshipView(generic.ObjectChildrenView):
    queryset = IPFabricTransformMap.objects.all()
    child_model = IPFabricRelationshipField
    table = IPFabricRelationshipFieldTable
    template_name = "ipfabric_netbox/inc/transform_map_relationship_map.html"
    tab = ViewTab(
        label="Relationship Maps",
        badge=lambda obj: IPFabricRelationshipField.objects.filter(
            transform_map=obj
        ).count(),
        permission="ipfabric_netbox.view_ipfabricrelationshipfield",
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(transform_map=parent)


class IPFabricRelationshipFieldListView(generic.ObjectListView):
    queryset = IPFabricRelationshipField.objects.all()
    table = IPFabricRelationshipFieldTable


# Transform Map


class IPFabricTransformMapListView(generic.ObjectListView):
    queryset = IPFabricTransformMap.objects.all()
    table = IPFabricTransformMapTable
    template_name = "ipfabric_netbox/ipfabrictransformmap_list.html"


class IPFabricTransformMapRestoreView(generic.ObjectListView):
    queryset = IPFabricTransformMap.objects.all()
    table = IPFabricTransformMapTable

    def get_required_permission(self):
        return "ipfabric_netbox.tm_restore"

    def get(self, request):
        if request.htmx:
            viewname = get_viewname(self.queryset.model, action="restore")
            form_url = reverse(viewname)
            form = ConfirmationForm(initial=request.GET)
            dependent_objects = {
                IPFabricTransformMap: IPFabricTransformMap.objects.all(),
                IPFabricTransformField: IPFabricTransformField.objects.all(),
                IPFabricRelationshipField: IPFabricRelationshipField.objects.all(),
            }
            print(dependent_objects)
            return render(
                request,
                "ipfabric_netbox/ipfabrictransformmap_restore.html",
                {
                    "form": form,
                    "form_url": form_url,
                    "dependent_objects": dependent_objects,
                },
            )

    def post(self, request):
        IPFabricTransformMap.objects.all().delete()
        try:
            data = requests.get(
                "https://gitlab.com/ip-fabric/integrations/ipfabric-netbox/-/raw/main/scripts/transform_map.json"
            ).json()
        except Exception as e:
            messages.error(request, e)
        BuildTransformMaps(data=data)
        return redirect("plugins:ipfabric_netbox:ipfabrictransformmap_list")


@register_model_view(IPFabricTransformMap, "edit")
class IPFabricTransformMapEditView(generic.ObjectEditView):
    queryset = IPFabricTransformMap.objects.all()
    form = IPFabricTransformMapForm
    default_return_url = "plugins:ipfabric_netbox:ipfabrictransformmap_list"


class IPFabricTransformMapDeleteView(generic.ObjectDeleteView):
    queryset = IPFabricTransformMap.objects.all()
    default_return_url = "plugins:ipfabric_netbox:ipfabrictransformmap_list"


class IPFabricTransformMapBulkDeleteView(generic.BulkDeleteView):
    queryset = IPFabricTransformMap.objects.all()
    table = IPFabricTransformMapTable


@register_model_view(IPFabricTransformMap)
class IPFabricTransformMapView(generic.ObjectView):
    queryset = IPFabricTransformMap.objects.all()


# Transform Map Field


class IPFabricTransformFieldListView(generic.ObjectListView):
    queryset = IPFabricTransformField.objects.all()
    table = IPFabricTransformFieldTable


@register_model_view(IPFabricTransformField, "edit")
class IPFabricTransformFieldEditView(generic.ObjectEditView):
    queryset = IPFabricTransformField.objects.all()
    form = IPFabricTransformFieldForm


class IPFabricTransformFieldDeleteView(generic.ObjectDeleteView):
    queryset = IPFabricTransformField.objects.all()


@register_model_view(IPFabricTransformMap, "fields")
class IPFabricTransformFieldView(generic.ObjectChildrenView):
    queryset = IPFabricTransformMap.objects.all()
    child_model = IPFabricTransformField
    table = IPFabricTransformFieldTable
    template_name = "ipfabric_netbox/inc/transform_map_field_map.html"
    tab = ViewTab(
        label="Field Maps",
        badge=lambda obj: IPFabricTransformField.objects.filter(
            transform_map=obj
        ).count(),
        permission="ipfabric_netbox.view_ipfabrictransformfield",
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(transform_map=parent)


# Snapshot


class IPFabricSnapshotListView(generic.ObjectListView):
    queryset = IPFabricSnapshot.objects.all()
    table = IPFabricSnapshotTable
    filterset = IPFabricSnapshotFilterSet
    filterset_form = IPFabricSnapshotFilterForm


@register_model_view(IPFabricSnapshot)
class IPFabricSnapshotView(generic.ObjectView):
    queryset = IPFabricSnapshot.objects.all()


class IPFabricSnapshotDeleteView(generic.ObjectDeleteView):
    queryset = IPFabricSnapshot.objects.all()


class IPFabricSnapshotBulkDeleteView(generic.BulkDeleteView):
    queryset = IPFabricSnapshot.objects.all()
    filterset = IPFabricSnapshotFilterSet
    table = IPFabricSnapshotTable


@register_model_view(IPFabricSnapshot, "data")
class IPFabricSnapshotRawView(generic.ObjectChildrenView):
    queryset = IPFabricSnapshot.objects.all()
    child_model = IPFabricData
    table = IPFabricDataTable
    template_name = "ipfabric_netbox/inc/snapshotdata.html"
    tab = ViewTab(
        label="Raw Data",
        badge=lambda obj: IPFabricData.objects.filter(snapshot_data=obj).count(),
        permission="ipfabric_netbox.view_ipfabricsnapshot",
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(snapshot_data=parent)


class IPFabricSnapshotDataDeleteView(generic.ObjectDeleteView):
    queryset = IPFabricData.objects.all()


class IPFabricSnapshotDataBulkDeleteView(generic.BulkDeleteView):
    queryset = IPFabricData.objects.all()
    filterset = IPFabricDataFilterSet
    table = IPFabricDataTable


@register_model_view(
    IPFabricData,
    name="data",
    path="json",
    kwargs={},
)
class IPFabricSnapshotDataJSONView(LoginRequiredMixin, View):
    template_name = "ipfabric_netbox/inc/json.html"

    def get(self, request, **kwargs):
        print(kwargs)
        # change_id = kwargs.get("change_pk", None)

        if request.htmx:
            data = get_object_or_404(IPFabricData, pk=kwargs.get("pk"))
            return render(
                request,
                self.template_name,
                {
                    "object": data,
                },
            )

        #         return render(
        #             request,
        #             self.template_name,
        #             {
        #                 "change": change,
        #                 "prechange_data": prechange_data,
        #                 "postchange_data": postchange_data,
        #                 "diff_added": diff_added,
        #                 "diff_removed": diff_removed,
        #                 "size": "lg",
        #             },
        #         )


# Source


class IPFabricSourceListView(generic.ObjectListView):
    queryset = IPFabricSource.objects.annotate(
        snapshot_count=count_related(IPFabricSnapshot, "source")
    )
    filterset = IPFabricSourceFilterSet
    filterset_form = IPFabricSourceFilterForm
    table = IPFabricSourceTable


@register_model_view(IPFabricSource, "edit")
class IPFabricSourceEditView(generic.ObjectEditView):
    queryset = IPFabricSource.objects.all()
    form = IPFabricSourceForm


@register_model_view(IPFabricSource)
class IPFabricSourceView(generic.ObjectView):
    queryset = IPFabricSource.objects.all()

    def get_extra_context(self, request, instance):
        related_models = (
            (
                IPFabricSnapshot.objects.restrict(request.user, "view").filter(
                    source=instance
                ),
                "source_id",
            ),
        )

        job = instance.jobs.order_by("id").last()
        data = {"related_models": related_models, "job": job}
        if job:
            data["job_results"] = job.data
        return data


@register_model_view(IPFabricSource, "sync")
class IPFabricSourceSyncView(BaseObjectView):
    queryset = IPFabricSource.objects.all()

    def get_required_permission(self):
        return "ipfabric_netbox.sync_source"

    def get(self, request, pk):
        ipfabricsource = get_object_or_404(self.queryset, pk=pk)
        return redirect(ipfabricsource.get_absolute_url())

    def post(self, request, pk):
        ipfabricsource = get_object_or_404(self.queryset, pk=pk)
        job = ipfabricsource.enqueue_sync_job(request=request)

        messages.success(request, f"Queued job #{job.pk} to sync {ipfabricsource}")
        return redirect(ipfabricsource.get_absolute_url())


@register_model_view(IPFabricSource, "delete")
class IPFabricSourceDeleteView(generic.ObjectDeleteView):
    queryset = IPFabricSource.objects.all()


class IPFabricSourceBulkDeleteView(generic.BulkDeleteView):
    queryset = IPFabricSource.objects.all()
    filterset = IPFabricSourceFilterSet
    table = IPFabricSourceTable


# Sync


class IPFabricSyncListView(View):
    def get(self, request):
        syncs = IPFabricSync.objects.prefetch_related("snapshot_data")
        return render(
            request,
            "ipfabric_netbox/sync_list.html",
            {"model": IPFabricSync, "syncs": syncs},
        )


@register_model_view(IPFabricSync, "edit")
class IPFabricSyncEditView(generic.ObjectEditView):
    queryset = IPFabricSync.objects.all()
    form = IPFabricSyncForm

    def alter_object(self, obj, request, url_args, url_kwargs):
        obj.user = request.user
        return obj


@register_model_view(IPFabricSync)
class IPFabricSyncView(generic.ObjectView):
    queryset = IPFabricSync.objects.all()
    actions = ("edit",)

    def get(self, request, **kwargs):
        instance = self.get_object(**kwargs)
        last_branch = instance.ipfabricbranch_set.last()

        if request.htmx:
            response = render(
                request,
                "ipfabric_netbox/partials/sync_last_branch.html",
                {"last_branch": last_branch},
            )

            if instance.status not in ["queued", "syncing"]:
                messages.success(
                    request,
                    f"Ingestion ({instance.name}) {instance.status}. Branch {last_branch.name} {last_branch.job.status}.",
                )
                response["HX-Refresh"] = "true"
            return response

        return render(
            request,
            self.get_template_name(),
            {
                "object": instance,
                "tab": self.tab,
                **self.get_extra_context(request, instance),
            },
        )

    def get_extra_context(self, request, instance):
        last_branch = instance.ipfabricbranch_set.last()

        if request.GET.get("format") in ["json", "yaml"]:
            format = request.GET.get("format")
            if request.user.is_authenticated:
                request.user.config.set("data_format", format, commit=True)
        elif request.user.is_authenticated:
            format = request.user.config.get("data_format", "json")
        else:
            format = "json"

        last_branch = instance.ipfabricbranch_set.last()

        return {"format": format, "last_branch": last_branch}


@register_model_view(IPFabricSync, "delete")
class IPFabricSyncDeleteView(generic.ObjectDeleteView):
    queryset = IPFabricSync.objects.all()
    default_return_url = "plugins:ipfabric_netbox:ipfabricsync_list"

    def get(self, request, pk):
        obj = get_object_or_404(self.queryset, pk=pk)

        if request.htmx:
            viewname = get_viewname(self.queryset.model, action="delete")
            form_url = reverse(viewname, kwargs={"pk": obj.pk})
            form = ConfirmationForm(initial=request.GET)
            return render(
                request,
                "ipfabric_netbox/inc/sync_delete.html",
                {
                    "object": obj,
                    "object_type": self.queryset.model._meta.verbose_name,
                    "form": form,
                    "form_url": form_url,
                    **self.get_extra_context(request, obj),
                },
            )


class IPFabricSyncBulkDeleteView(generic.BulkDeleteView):
    queryset = IPFabricSync.objects.all()
    filterset = IPFabricSnapshotFilterSet
    table = IPFabricSnapshotTable


# Ingestion


@register_model_view(IPFabricSync, "sync")
class IPFabricIngestSyncView(BaseObjectView):
    queryset = IPFabricSync.objects.all()

    def get_required_permission(self):
        return "ipfabric_netbox.sync_ingest"

    def get(self, request, pk):
        ipfabric = get_object_or_404(self.queryset, pk=pk)
        return redirect(ipfabric.get_absolute_url())

    def post(self, request, pk):
        ipfabric = get_object_or_404(self.queryset, pk=pk)
        job = ipfabric.enqueue_sync_job(user=request.user, adhoc=True)

        messages.success(request, f"Queued job #{job.pk} to sync {ipfabric}")
        return redirect(ipfabric.get_absolute_url())


# Branch


class IPFabricBranchListView(generic.ObjectListView):
    queryset = IPFabricBranch.objects.all()
    filterset = IPFabricBranchFilterSet
    filterset_form = IPFabricBranchFilterForm
    table = BranchTable


@register_model_view(
    IPFabricBranch,
    name="logs",
    path="logs",
)
class IPFabricBranchLogView(LoginRequiredMixin, View):
    template_name = "ipfabric_netbox/partials/branch_all.html"

    def get(self, request, **kwargs):
        branch_id = kwargs.get("pk")
        if request.htmx:
            branch = IPFabricBranch.objects.get(pk=branch_id)
            data = branch.get_statistics()
            data["object"] = branch
            data["job"] = branch.job
            response = render(
                request,
                self.template_name,
                data,
            )
            if branch.job.completed:
                response["HX-Refresh"] = "true"
                return response
            else:
                return response


@register_model_view(IPFabricBranch)
class IPFabricBranchView(generic.ObjectView):
    queryset = IPFabricBranch.objects.annotate(
        num_created=models.Count(
            "staged_changes",
            filter=models.Q(staged_changes__action=ChangeActionChoices.ACTION_CREATE)
            & ~models.Q(staged_changes__object_type__model="objectchange"),
        ),
        num_updated=models.Count(
            "staged_changes",
            filter=models.Q(staged_changes__action=ChangeActionChoices.ACTION_UPDATE)
            & ~models.Q(staged_changes__object_type__model="objectchange"),
        ),
        num_deleted=models.Count(
            "staged_changes",
            filter=models.Q(staged_changes__action=ChangeActionChoices.ACTION_DELETE)
            & ~models.Q(staged_changes__object_type__model="objectchange"),
        ),
    )

    def get_extra_context(self, request, instance):
        data = instance.get_statistics()
        return data


@register_model_view(IPFabricBranch, "merge")
class IPFabricBranchMergeView(BaseObjectView):
    queryset = IPFabricBranch.objects.all()
    template_name = "ipfabric_netbox/inc/merge_form.html"

    def get_required_permission(self):
        return "ipfabric_netbox.merge_branch"

    def get(self, request, pk):
        obj = get_object_or_404(self.queryset, pk=pk)

        if request.htmx:
            viewname = get_viewname(self.queryset.model, action="merge")
            form_url = reverse(viewname, kwargs={"pk": obj.pk})
            form = ConfirmationForm(initial=request.GET)
            return render(
                request,
                "ipfabric_netbox/inc/merge_form.html",
                {
                    "object": obj,
                    "object_type": self.queryset.model._meta.verbose_name,
                    "form": form,
                    "form_url": form_url,
                    **self.get_extra_context(request, obj),
                },
            )

        return redirect(obj.get_absolute_url())

    def post(self, request, pk):
        ipfabric = get_object_or_404(self.queryset, pk=pk)
        job = ipfabric.enqueue_merge_job(user=request.user)

        messages.success(request, f"Queued job #{job.pk} to sync {ipfabric}")
        return redirect(ipfabric.get_absolute_url())


@register_model_view(
    IPFabricBranch,
    name="change_diff",
    path="change/<int:change_pk>",
    kwargs={"model": IPFabricBranch},
)
class IPFabricBranchChangesDiffView(LoginRequiredMixin, View):
    template_name = "ipfabric_netbox/inc/diff.html"

    def get(self, request, model, **kwargs):
        change_id = kwargs.get("change_pk", None)

        if request.htmx:
            if change_id:
                change = StagedChange.objects.get(pk=change_id)
                if hasattr(change.object, "pk"):
                    prechange_data = serialize_object(change.object, resolve_tags=False)
                    prechange_data = dict(sorted(prechange_data.items()))
                else:
                    prechange_data = None

                if hasattr(change, "data"):
                    postchange_data = dict(sorted(change.data.items()))

                if prechange_data and postchange_data:
                    diff_added = shallow_compare_dict(
                        prechange_data or dict(),
                        postchange_data or dict(),
                        exclude=["last_updated"],
                    )
                    diff_removed = (
                        {x: prechange_data.get(x) for x in diff_added}
                        if prechange_data
                        else {}
                    )
                else:
                    diff_added = None
                    diff_removed = None

                return render(
                    request,
                    self.template_name,
                    {
                        "change": change,
                        "prechange_data": prechange_data,
                        "postchange_data": postchange_data,
                        "diff_added": diff_added,
                        "diff_removed": diff_removed,
                        "size": "lg",
                    },
                )


@register_model_view(IPFabricBranch, "change")
class IPFabricBranchChangesView(generic.ObjectChildrenView):
    queryset = IPFabricBranch.objects.all()
    child_model = StagedChange
    table = StagedChangesTable
    filterset = IPFabricStagedChangeFilterSet
    template_name = "generic/object_children.html"
    tab = ViewTab(
        label="Changes",
        badge=lambda obj: StagedChange.objects.filter(branch=obj).count(),
        permission="ipfabric_netbox.view_ipfabricbranch",
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(branch=parent)


@register_model_view(IPFabricBranch, "delete")
class IPFabricBranchDeleteView(generic.ObjectDeleteView):
    queryset = IPFabricBranch.objects.all()


@register_model_view(IPFabricSync, "branch")
class IPFabricBranchTabView(generic.ObjectChildrenView):
    queryset = IPFabricSync.objects.all()
    child_model = IPFabricBranch
    table = BranchTable
    filterset = IPFabricBranchFilterSet
    template_name = "generic/object_children.html"
    tab = ViewTab(
        label="Branches",
        badge=lambda obj: IPFabricBranch.objects.filter(sync=obj).count(),
        permission="ipfabric_netbox.view_ipfabricbranch",
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(sync=parent)


@register_model_view(Device, "ipfabric")
class IPFabricTable(View):
    template_name = "ipfabric_netbox/ipfabric_table.html"
    tab = ViewTab("IP Fabric", permission="ipfabric_netbox.view_devicetable")

    def get(self, request, pk):
        device = get_object_or_404(Device, pk=pk)
        form = (
            IPFabricTableForm(request.GET)
            if "table" in request.GET
            else IPFabricTableForm()
        )
        data = None

        if form.is_valid():
            table = form.cleaned_data["table"]
            test = {
                "True": True,
                "False": False,
            }
            cache_enable = test.get(form.cleaned_data["cache_enable"])
            snapshot_id = ""

            if not form.cleaned_data["snapshot_data"]:
                snapshot_id = "$last"
                source = IPFabricSource.objects.get(
                    pk=device.custom_field_data["ipfabric_source"]
                )

            else:
                snapshot_id = form.cleaned_data["snapshot_data"].snapshot_id
                source = form.cleaned_data["snapshot_data"].source

            source.parameters["snapshot_id"] = snapshot_id
            source.parameters["base_url"] = source.url

            cache_key = (
                f"ipfabric_{table}_{device.serial}_{source.parameters['snapshot_id']}"
            )
            if cache_enable:
                data = cache.get(cache_key)

            if not data:
                try:
                    ipf = IPFabric(parameters=source.parameters)
                    raw_data, columns = ipf.get_table_data(table=table, device=device)
                    data = {"data": raw_data, "columns": columns}
                    cache.set(cache_key, data, 60 * 60 * 24)
                except Exception as e:
                    messages.error(request, e)

        if not data:
            data = {"data": [], "columns": []}

        table = DeviceIPFTable(data["data"], extra_columns=data["columns"])

        RequestConfig(
            request,
            {
                "paginator_class": EnhancedPaginator,
                "per_page": get_paginate_count(request),
            },
        ).configure(table)

        if request.htmx:
            return render(
                request,
                "htmx/table.html",
                {
                    "table": table,
                },
            )

        source = None

        if source_id := device.custom_field_data["ipfabric_source"]:
            source = IPFabricSource.objects.get(pk=source_id)

        return render(
            request,
            self.template_name,
            {
                "object": device,
                "source": source,
                "tab": self.tab,
                "form": form,
                "table": table,
            },
        )


@register_model_view(
    IPFabricSource,
    name="topology",
    path="topology/<int:site>",
    kwargs={"snapshot": ""},
)
class IPFabricSourceTopology(LoginRequiredMixin, View):
    template_name = "ipfabric_netbox/inc/site_topology_modal.html"

    def get(self, request, pk, site, **kwargs):
        if request.htmx:
            try:
                site = get_object_or_404(Site, pk=site)
                source_id = request.GET.get("source")
                if not source_id:
                    raise Exception("Source ID not available in request.")
                source = get_object_or_404(IPFabricSource, pk=source_id)
                snapshot = request.GET.get("snapshot")
                if not snapshot:
                    raise Exception("Snapshot ID not available in request.")

                source.parameters.update(
                    {"snapshot_id": snapshot, "base_url": source.url}
                )

                ipf = IPFabric(parameters=source.parameters)
                snapshot_data = ipf.ipf.snapshots.get(snapshot)
                if not snapshot_data:
                    raise Exception(
                        f"Snapshot ({snapshot}) not available in IP Fabric."
                    )

                sites = ipf.ipf.inventory.sites.all(
                    filters={"siteName": ["eq", site.name]}
                )
                if not sites:
                    raise Exception(
                        f"{site.name} not available in snapshot ({snapshot})."
                    )

                net = Network(sites=site.name, all_network=False)
                settings = NetworkSettings()
                settings.hide_protocol("xdp")
                settings.hiddenDeviceTypes.extend(["transit", "cloud"])

                link = ipf.ipf.diagram.share_link(net, graph_settings=settings)
                svg_data = ipf.ipf.diagram.svg(net, graph_settings=settings).decode(
                    "utf-8"
                )
                error = None
            except Exception as e:
                error = e
                svg_data = link = None

            return render(
                request,
                self.template_name,
                {
                    "site": site,
                    "source": source,
                    "svg": svg_data,
                    "size": "xl",
                    "link": link,
                    "time": timezone.now(),
                    "snapshot": snapshot_data,
                    "error": error,
                },
            )
