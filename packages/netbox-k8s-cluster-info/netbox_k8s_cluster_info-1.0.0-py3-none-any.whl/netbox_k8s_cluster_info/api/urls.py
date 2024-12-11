from netbox.api.routers import NetBoxRouter
from netbox_k8s_cluster_info.api.views import (
    NetboxK8sClusterInfoRootView,
    K8sClusterTypeViewSet,
    K8sServiceViewSet,
    K8sClusterViewSet,
)

router = NetBoxRouter()
router.APIRootView = NetboxK8sClusterInfoRootView

router.register("k8s_clusters", K8sClusterViewSet)
router.register("k8s_cluster_types", K8sClusterTypeViewSet)
router.register("k8s_services", K8sServiceViewSet)
urlpatterns = router.urls
