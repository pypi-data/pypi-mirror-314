from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer
from netbox.api.serializers import WritableNestedSerializer
from rest_framework import serializers
from users.api.serializers_.nested import NestedUserSerializer

from ipfabric_netbox.models import IPFabricBranch
from ipfabric_netbox.models import IPFabricSnapshot
from ipfabric_netbox.models import IPFabricSource
from ipfabric_netbox.models import IPFabricSync
from ipfabric_netbox.models import IPFabricTransformMap

# from .serializers import IPFabricSyncSerializer

__all__ = (
    "NestedIPFabricSourceSerializer",
    "NestedIPFabricSnapshotSerializer",
    "NestedIPFabricTransformMapSerializer",
    "NestedIPFabricBranchSerializer",
    "NestedIPFabricSyncSerializer",
)


class NestedIPFabricSourceSerializer(WritableNestedSerializer):
    url = serializers.URLField()

    class Meta:
        model = IPFabricSource
        fields = ["id", "url", "display", "name", "type"]


class NestedIPFabricSnapshotSerializer(NetBoxModelSerializer):
    source = NestedIPFabricSourceSerializer(read_only=True)
    display = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = IPFabricSnapshot
        fields = [
            "id",
            "name",
            "source",
            "snapshot_id",
            "status",
            "date",
            "display",
            "sites",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_display(self, obj):
        return f"{obj.name} ({obj.snapshot_id})"


class NestedIPFabricSyncSerializer(NetBoxModelSerializer):
    snapshot_data = NestedIPFabricSnapshotSerializer(read_only=True)

    class Meta:
        model = IPFabricSync
        fields = [
            "id",
            "name",
            "display",
            "snapshot_data",
            "type",
            "status",
            "parameters",
            "last_synced",
        ]


class NestedIPFabricTransformMapSerializer(NetBoxModelSerializer):
    target_model = ContentTypeField(read_only=True)

    class Meta:
        model = IPFabricTransformMap
        fields = [
            "id",
            "source_model",
            "target_model",
            "status",
        ]


class NestedIPFabricBranchSerializer(NetBoxModelSerializer):
    user = NestedUserSerializer(read_only=True)
    sync = NestedIPFabricSyncSerializer(read_only=True)

    class Meta:
        model = IPFabricBranch
        fields = [
            "id",
            "name",
            "display",
            "sync",
            "description",
            "user",
        ]
