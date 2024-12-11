from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from netbox_workload_manager.models import WorkloadClusterType, WorkloadCluster, WorkloadService


class WorkloadClusterTypeSerializer(NetBoxModelSerializer):
    display = serializers.SerializerMethodField()
    
    class Meta:
        model = WorkloadClusterType
        fields = (
            "id",
            "name",
            "description",
            "tags",
            "custom_field_data",
            "created",
            "last_updated",
        )
        brief_fields = ("id", "name", "description")

    def get_display(self, obj):
        return f"{obj}"


class WorkloadClusterSerializer(NetBoxModelSerializer):
    display = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_svm-api:softwareproduct-detail")

    class Meta:
        model = WorkloadCluster
        fields = (
            "id",
            "name",
            "description",
            "tags",
            "comments",
            "custom_field_data",
            "created",
            "last_updated",
        )
        brief_fields = ("id", "display", "url", "name", "description")

    def get_display(self, obj):
        return f"{obj.manufacturer} - {obj}"


class WorkloadServiceSerializer(NetBoxModelSerializer):
    display = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_svm-api:softwareproductversion-detail")

    class Meta:
        model = WorkloadService
        fields = (
            "id",
            "name",
            "application",
            "namespace",
            "memory",
            "cpu",
            "gpu",
            "description",
            "tags",
            "comments",
            "custom_field_data",
            "created",
            "last_updated",
        )
        brief_fields = ("id", "display", "url", "name")

    def get_display(self, obj):
        return f"{obj}"
