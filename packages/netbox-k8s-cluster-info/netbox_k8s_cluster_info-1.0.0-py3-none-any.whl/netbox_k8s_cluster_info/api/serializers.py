from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from netbox_k8s_cluster_info.models import K8sClusterType, K8sCluster, K8sService


class K8sClusterTypeSerializer(NetBoxModelSerializer):
    display = serializers.SerializerMethodField()
    
    class Meta:
        model = K8sClusterType
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


class K8sClusterSerializer(NetBoxModelSerializer):
    display = serializers.SerializerMethodField()

    class Meta:
        model = K8sCluster
        fields = (
            "id",
            "name",
            "description",
            "tags",
            "contact",
            "devices",
            "virtualmachine",
            "comments",
            "custom_field_data",
            "created",
            "last_updated",
        )
        brief_fields = ("id", "name", "description")
        
    def get_display(self, obj):
        return f"{obj}"
class K8sServiceSerializer(NetBoxModelSerializer):
    display = serializers.SerializerMethodField()

    class Meta:
        model = K8sService
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
        brief_fields = ("id", "name")

    def get_display(self, obj):
        return f"{obj}"
