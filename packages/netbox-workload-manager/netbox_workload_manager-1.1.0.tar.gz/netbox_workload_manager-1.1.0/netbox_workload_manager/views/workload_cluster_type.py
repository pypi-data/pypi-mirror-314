from netbox.views import generic
from netbox_workload_manager import forms, tables, filtersets
from netbox_workload_manager.models import WorkloadClusterType


class WorkloadClsuterTypeListView(generic.ObjectListView):
    """View for listing all existing Workload Cluster Type."""

    queryset = WorkloadClusterType.objects.all()
    filterset = filtersets.WorkloadClusterTypeFilterSet
    filterset_form = forms.WorkloadClusterTypeForm
    table = tables.WorkloadClusterTypeTable

class WorkloadClsuterTypeView(generic.ObjectView):
    """Display Workload Cluster Type details"""
    queryset = WorkloadClusterType.objects.all()


class WorkloadClsuterTypeEditView(generic.ObjectEditView):
    """View for editing and creating a Workload Cluster Type instance."""

    queryset = WorkloadClusterType.objects.all()
    form = forms.WorkloadClusterTypeForm

class WorkloadClsuterTypeDeleteView(generic.ObjectDeleteView):
    """View for deleting a WorkloadClusterType instance"""

    queryset = WorkloadClusterType.objects.all()

# Delete multiple item 
class WorkloadClsuterTypeBulkDeleteView(generic.BulkDeleteView):
    queryset = WorkloadClusterType.objects.all()
    table = tables.WorkloadClusterTypeTable

# Import file to add multiple item 
class WorkloadClsuterTypeBulkImportView(generic.BulkImportView):
    queryset = WorkloadClusterType.objects.all()
    model_form = forms.WorkloadClusterTypeImportForm