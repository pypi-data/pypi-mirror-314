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
            | Q(comments__icontains=value)
        )
        return queryset.filter(qs_filter)


class WorkloadClusterFilterSet(NetBoxModelFilterSet):
    """Filter capabilities for WorkloadCluster instances."""

    class Meta:
        model = WorkloadCluster
        fields = ("type",)

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(workload_cluster_type__name__icontains=value)
            | Q(contact__icontains=value)
            | Q(devices__icontains=value)
        )
        return queryset.filter(qs_filter)


class WorkloadServiceFilterSet(NetBoxModelFilterSet):
    """Filter capabilities for WorkloadService instances."""

    contact_id = django_filters.ModelMultipleChoiceFilter(
        field_name='contact',
        queryset=Contact.objects.all(),
        label='Contact (ID)',
    )

    class Meta:
        model = WorkloadService
        fields = ("workload_cluster",)

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(workload_cluster_name__icontains=value)
            | Q(namespace__icontains=value)
            | Q(name__icontains=value)
            | Q(application__icontains=value)
            | Q(description__icontains=value)
            | Q(gpu__icontains=value)
        )
        return queryset.filter(qs_filter)
