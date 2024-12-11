from rest_framework.routers import APIRootView

from netbox.api.viewsets import NetBoxModelViewSet
from netbox_k8s_manager.api.serializers import (
    K8sClusterSerializer,
    K8sClusterTypeSerializer,
    K8sServiceSerializer,
)
from netbox_k8s_manager.filtersets import (
    K8sClusterFilterSet,
    K8sClusterTypeFilterSet,
    K8sServiceFilterSet,
)
from netbox_k8s_manager.models import K8sService, K8sCluster, K8sClusterType


class NetboxK8sManagerRootView(APIRootView):
    """
    NetboxK8sManager API root view
    """

    def get_view_name(self):
        return "NetboxK8sManager"

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

