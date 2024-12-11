from netbox.api.routers import NetBoxRouter
from netbox_k8s_manager.api.views import (
    NetboxK8sManagerRootView,
    K8sClusterTypeViewSet,
    K8sServiceViewSet,
    K8sClusterViewSet,
)

router = NetBoxRouter()
router.APIRootView = NetboxK8sManagerRootView

router.register("k8s_clusters", K8sClusterViewSet)
router.register("k8s_cluster_types", K8sClusterTypeViewSet)
router.register("k8s_services", K8sServiceViewSet)
urlpatterns = router.urls
