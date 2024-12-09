from netbox.api.routers import NetBoxRouter
from netbox_workload_manager.api.views import (
    NetboxWorkloadManagerRootView,
    WorkloadClusterTypeViewSet,
    WorkloadServiceViewSet,
    WorkloadClusterViewSet,
)

router = NetBoxRouter()
router.APIRootView = NetboxWorkloadManagerRootView

router.register("workload_clusters", WorkloadClusterViewSet)
router.register("workload_cluster_types", WorkloadClusterTypeViewSet)
router.register("workload_services", WorkloadServiceViewSet)
urlpatterns = router.urls
