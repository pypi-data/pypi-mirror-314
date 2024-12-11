from rest_framework.routers import APIRootView

from netbox.api.viewsets import NetBoxModelViewSet
from netbox_k8s_cluster_info.api.serializers import (
    K8sClusterSerializer,
    K8sClusterTypeSerializer,
    K8sServiceSerializer,
)
from netbox_k8s_cluster_info.filtersets import (
    K8sClusterFilterSet,
    K8sClusterTypeFilterSet,
    K8sServiceFilterSet,
)
from netbox_k8s_cluster_info.models import K8sService, K8sCluster, K8sClusterType


class NetboxK8sClusterInfoRootView(APIRootView):
    """
    NetboxK8sClusterInfo API root view
    """

    def get_view_name(self):
        return "NetboxK8sClusterInfo"

class K8sClusterViewSet(NetBoxModelViewSet):
    queryset = K8sCluster.objects.all()
    serializer_class = K8sClusterSerializer
    filterset_class = K8sClusterFilterSet


class K8sClusterTypeViewSet(NetBoxModelViewSet):
    queryset = K8sClusterType.objects.all()
    serializer_class = K8sClusterTypeSerializer
    filterset_class = K8sClusterTypeFilterSet


class K8sServiceViewSet(NetBoxModelViewSet):
    queryset = K8sService.objects.all()
    serializer_class = K8sServiceSerializer
    filterset_class = K8sServiceFilterSet

