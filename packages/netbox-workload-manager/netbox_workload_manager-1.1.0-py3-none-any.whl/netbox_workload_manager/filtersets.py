from django.db.models import Q
# from netbox.filtersets import NetBoxModelFilterSet
from netbox.filtersets import NetBoxModelFilterSet
from netbox_workload_manager.models import WorkloadClusterType, WorkloadCluster, WorkloadService
import django_filters
from tenancy.models import Contact

class WorkloadClusterTypeFilterSet(NetBoxModelFilterSet):
    """Filter capabilities for WorkloadClusterType instances."""

    class Meta:
        model = WorkloadClusterType
        fields = tuple()

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(description__icontains=value)
        )
        return queryset.filter(qs_filter)


class WorkloadClusterFilterSet(NetBoxModelFilterSet):
    """Filter capabilities for WorkloadCluster instances."""

    class Meta:
        model = WorkloadCluster
        #fields = ("workload_cluster_type",)
        fields = tuple()

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(type__name__icontains=value)
            | Q(contact__name__icontains=value)
        )
        return queryset.filter(qs_filter)


class WorkloadServiceFilterSet(NetBoxModelFilterSet):
    """Filter capabilities for WorkloadService instances."""

    class Meta:
        model = WorkloadService
        fields = ("workload_cluster",)

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(workload_cluster__name__icontains=value)
            | Q(namespace__icontains=value)
            | Q(name__icontains=value)
            | Q(application__icontains=value)
        )
        return queryset.filter(qs_filter)
