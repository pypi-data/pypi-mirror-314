from django.contrib.contenttypes.models import ContentType

from ipfabric_netbox.models import IPFabricRelationshipField
from ipfabric_netbox.models import IPFabricTransformField
from ipfabric_netbox.models import IPFabricTransformMap


def BuildField(data):
    if "target_model" in data:
        ct = ContentType.objects.get(
            app_label=data["target_model"]["app_label"],
            model=data["target_model"]["model"],
        )
        data["target_model"] = ct
    elif "source_model" in data:
        ct = ContentType.objects.get(
            app_label=data["source_model"]["app_label"],
            model=data["source_model"]["model"],
        )
        data["source_model"] = ct
    return data


def BuildTransformMaps(data):
    for tm in data:
        field_data = BuildField(tm["data"])
        tm_obj = IPFabricTransformMap.objects.create(**field_data)
        for fm in tm["field_maps"]:
            field_data = BuildField(fm)
            IPFabricTransformField.objects.create(transform_map=tm_obj, **field_data)
        for rm in tm["relationship_maps"]:
            relationship_data = BuildField(rm)
            IPFabricRelationshipField.objects.create(
                transform_map=tm_obj, **relationship_data
            )
