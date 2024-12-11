import django_filters
from core.choices import DataSourceStatusChoices
from django.db.models import Q
from django.utils.translation import gettext as _
from extras.choices import ChangeActionChoices
from netbox.filtersets import BaseFilterSet
from netbox.filtersets import ChangeLoggedModelFilterSet
from netbox.filtersets import NetBoxModelFilterSet
from netbox.staging import StagedChange

from .models import IPFabricBranch
from .models import IPFabricData
from .models import IPFabricSnapshot
from .models import IPFabricSource
from .models import IPFabricSync
from .models import IPFabricTransformMap


class IPFabricStagedChangeFilterSet(BaseFilterSet):
    q = django_filters.CharFilter(method="search")
    action = django_filters.MultipleChoiceFilter(choices=ChangeActionChoices)

    class Meta:
        model = StagedChange
        fields = ["branch", "action", "object_type"]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(data__values__contains=value)
            | Q(action__icontains=value)
            | Q(object_type__model__icontains=value)
        )


class IPFabricDataFilterSet(BaseFilterSet):
    q = django_filters.CharFilter(method="search")

    class Meta:
        model = IPFabricData
        fields = ["snapshot_data", "type"]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(snapshot_data__icontains=value) | Q(type__icontains=value)
        )


class IPFabricSnapshotFilterSet(ChangeLoggedModelFilterSet):
    q = django_filters.CharFilter(method="search")
    source_id = django_filters.ModelMultipleChoiceFilter(
        queryset=IPFabricSource.objects.all(),
        label=_("Source (ID)"),
    )
    source = django_filters.ModelMultipleChoiceFilter(
        field_name="source__name",
        queryset=IPFabricSource.objects.all(),
        to_field_name="name",
        label=_("Source (name)"),
    )
    snapshot_id = django_filters.CharFilter(
        label=_("Snapshot ID"), lookup_expr="icontains"
    )

    class Meta:
        model = IPFabricSnapshot
        fields = ("id", "name", "status", "snapshot_id")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value))


class IPFabricSourceFilterSet(NetBoxModelFilterSet):
    status = django_filters.MultipleChoiceFilter(
        choices=DataSourceStatusChoices, null_value=None
    )

    class Meta:
        model = IPFabricSource
        fields = ("id", "name")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(comments__icontains=value)
        )


class IPFabricBranchFilterSet(BaseFilterSet):
    q = django_filters.CharFilter(method="search")
    sync_id = django_filters.ModelMultipleChoiceFilter(
        queryset=IPFabricSync.objects.all(),
        label=_("Sync (ID)"),
    )
    sync = django_filters.ModelMultipleChoiceFilter(
        field_name="sync__name",
        queryset=IPFabricSync.objects.all(),
        to_field_name="name",
        label=_("Sync (name)"),
    )

    class Meta:
        model = IPFabricBranch
        fields = ("id", "name", "sync")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) | Q(sync__name__icontains=value)
        )


class IPFabricTransformFieldFilterSet(BaseFilterSet):
    transform_map = django_filters.ModelMultipleChoiceFilter(
        queryset=IPFabricTransformMap.objects.all(), label=_("Transform Map")
    )
