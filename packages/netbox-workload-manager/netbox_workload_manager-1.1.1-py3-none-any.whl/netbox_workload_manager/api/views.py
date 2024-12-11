from rest_framework.routers import APIRootView

from netbox.api.viewsets import NetBoxModelViewSet
from netbox_workload_manager.api.serializers import (
    WorkloadClusterSerializer,
    WorkloadClusterTypeSerializer,
    WorkloadServiceSerializer,
)
from netbox_workload_manager.filtersets import (
    WorkloadClusterFilterSet,
    WorkloadClusterTypeFilterSet,
    WorkloadServiceFilterSet,
)
from netbox_workload_manager.models import WorkloadService, WorkloadCluster, WorkloadClusterType


class NetboxWorkloadManagerRootView(APIRootView):
    """
    NetboxWorkloadManager API root view
    """

    def get_view_name(self):
        return "NetboxWorkloadManager"

class WorkloadClusterViewSet(NetBoxModelViewSet):
    queryset = WorkloadCluster.objects.all()
    serializer_class = WorkloadClusterSerializer
    filterset_class = WorkloadClusterFilterSet


class WorkloadClusterTypeViewSet(NetBoxModelViewSet):
    queryset = WorkloadClusterType.objects.all()
    serializer_class = WorkloadClusterTypeSerializer
    filterset_class = WorkloadClusterTypeFilterSet


class WorkloadServiceViewSet(NetBoxModelViewSet):
    queryset = WorkloadService.objects.all()
    serializer_class = WorkloadServiceSerializer
    filterset_class = WorkloadServiceFilterSet

