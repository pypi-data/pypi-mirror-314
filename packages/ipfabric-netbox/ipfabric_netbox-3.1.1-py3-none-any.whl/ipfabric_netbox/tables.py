import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from django_tables2 import Column
from extras.models import StagedChange
from netbox.tables import columns
from netbox.tables import NetBoxTable

from .models import IPFabricBranch
from .models import IPFabricData
from .models import IPFabricRelationshipField
from .models import IPFabricSnapshot
from .models import IPFabricSource
from .models import IPFabricSync
from .models import IPFabricTransformField
from .models import IPFabricTransformMap


DIFF_BUTTON = """
    <a href="#"
          hx-get="{% url 'plugins:ipfabric_netbox:ipfabricbranch_change_diff' pk=record.branch.pk change_pk=record.pk %}"
          hx-target="#htmx-modal-content"
          data-bs-toggle="modal"
          data-bs-target="#htmx-modal"
          class="btn btn-success btn-sm"
        >
        <i class="mdi mdi-code-tags">Diff</i>
    </a>
"""

DATA_BUTTON = """
    <a href="#"
          hx-get="{% url 'plugins:ipfabric_netbox:ipfabricdata_data' pk=record.pk %}"
          hx-target="#htmx-modal-content"
          data-bs-toggle="modal"
          data-bs-target="#htmx-modal"
          class="btn btn-success btn-sm"
        >
        <i class="mdi mdi-code-tags">JSON</i>
    </a>
"""


class IPFabricRelationshipFieldTable(NetBoxTable):
    actions = columns.ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = IPFabricRelationshipField
        fields = ("source_model", "target_field", "coalesce", "actions")
        default_columns = ("source_model", "target_field", "coalesce", "actions")


class IPFabricTransformFieldTable(NetBoxTable):
    id = tables.Column()
    actions = columns.ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = IPFabricTransformField
        fields = ("id", "source_field", "target_field", "coalesce", "actions")
        default_columns = ("source_field", "target_field", "coalesce", "actions")


class IPFabricTransformMapTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = IPFabricTransformMap
        fields = ("name", "source_model", "target_model", "status")
        default_columns = ("name", "source_model", "target_model", "status")


class BranchTable(NetBoxTable):
    name = tables.Column(linkify=True)
    sync = tables.Column(verbose_name="IP Fabric Sync", linkify=True)
    changes = tables.Column(accessor="staged_changes", verbose_name="Number of Changes")
    actions = columns.ActionsColumn(actions=("delete",))

    def render_changes(self, value):
        return value.count()

    class Meta(NetBoxTable.Meta):
        model = IPFabricBranch
        fields = ("name", "sync", "description", "user", "changes")
        default_columns = ("name", "sync", "description", "user", "changes")


class IPFabricSnapshotTable(NetBoxTable):
    name = tables.Column(linkify=True)
    source = tables.Column(linkify=True)
    tags = columns.TagColumn(url_name="core:datasource_list")
    actions = columns.ActionsColumn(actions=("delete",))
    status = columns.ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = IPFabricSnapshot
        fields = (
            "pk",
            "id",
            "name",
            "snapshot_id",
            "status",
            "date",
            "created",
            "last_updated",
        )
        default_columns = ("pk", "name", "source", "snapshot_id", "status", "date")


class IPFabricSourceTable(NetBoxTable):
    name = tables.Column(linkify=True)
    status = columns.ChoiceFieldColumn()
    snapshot_count = tables.Column(verbose_name="Snapshots")
    tags = columns.TagColumn(url_name="core:datasource_list")

    class Meta(NetBoxTable.Meta):
        model = IPFabricSource
        fields = (
            "pk",
            "id",
            "name",
            "status",
            "description",
            "comments",
            "created",
            "last_updated",
        )
        default_columns = ("pk", "name", "status", "description", "snapshot_count")


class SyncTable(NetBoxTable):
    actions = None
    status = columns.ChoiceFieldColumn()
    snapshot_name = tables.Column(
        verbose_name="Snapshot Name", accessor="snapshot_data"
    )

    def render_snapshot_name(self, value):
        return value.get("name", "---")

    class Meta(NetBoxTable.Meta):
        model = IPFabricSync
        fields = ("id", "status", "snapshot_name")
        default_columns = ("id", "status", "snapshot_name")


class StagedChangesTable(NetBoxTable):
    pk = None
    object_type = tables.Column(
        accessor="object_type.model", verbose_name="Object Type"
    )
    name = tables.Column(accessor="object_type.name", verbose_name="Name")
    actions = columns.TemplateColumn(template_code=DIFF_BUTTON)

    def render_name(self, value, record):
        models_with_names = [
            "site",
            "manufacturer",
            "device role",
            "device",
            "interface",
            "platform",
            "inventory item",
            "VLAN",
        ]
        if record.data:
            if value in models_with_names:
                name = record.data["name"]
            elif value == "device type":
                name = record.data["model"]
            elif value == "IP address":
                name = record.data["address"]
            elif value == "tagged item":
                name = f"Tagging object ({record.data['object_id']})"
            elif value == "prefix":
                name = f"{record.data['prefix']} ({record.data['vrf']})"
            else:
                name = record.data
        else:
            name = record.object.__str__()
        return name

    class Meta(NetBoxTable.Meta):
        model = StagedChange
        name = "staged_changes"
        fields = ("name", "action", "object_type", "actions")
        default_columns = ("name", "action", "object_type", "actions")


class DeviceIPFTable(tables.Table):
    hostname = Column()

    class Meta:
        attrs = {
            "class": "table table-hover object-list",
        }
        empty_text = _("No results found")

    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)


class IPFabricDataTable(NetBoxTable):
    JSON = columns.TemplateColumn(template_code=DATA_BUTTON)
    actions = columns.ActionsColumn(actions=("delete",))

    class Meta(NetBoxTable.Meta):
        model = IPFabricData
        fields = ("snapshot_data", "type", "JSON")
        default_columns = ("snapshot_data", "type", "JSON")
