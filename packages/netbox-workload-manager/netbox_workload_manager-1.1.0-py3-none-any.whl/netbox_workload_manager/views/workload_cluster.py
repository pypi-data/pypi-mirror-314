from netbox.views import generic
from netbox_workload_manager import forms, tables, filtersets
from netbox_workload_manager.models import WorkloadCluster, WorkloadService


class WorkloadClsuterListView(generic.ObjectListView):
    """View for listing all existing Workload Cluster."""

    queryset = WorkloadCluster.objects.all()
    filterset = filtersets.WorkloadClusterFilterSet
    filterset_form = forms.WorkloadClusterForm
    table = tables.WorkloadClusterTable

class WorkloadClsuterView(generic.ObjectView):
    """Display Workload Cluster details"""

    queryset = WorkloadCluster.objects.all()


class WorkloadClsuterEditView(generic.ObjectEditView):
    """View for editing and creating a Workload Cluster instance."""

    queryset = WorkloadCluster.objects.all()
    form = forms.WorkloadClusterForm

class WorkloadClsuterDeleteView(generic.ObjectDeleteView):
    """View for deleting a WorkloadCluster instance"""

    queryset = WorkloadCluster.objects.all()

# Delete multiple item 
class WorkloadClsuterBulkDeleteView(generic.BulkDeleteView):
    queryset = WorkloadCluster.objects.all()
    table = tables.WorkloadClusterTable

# Import file to add multiple item 
class WorkloadClsuterBulkImportView(generic.BulkImportView):
    queryset = WorkloadCluster.objects.all()
    model_form = forms.WorkloadClusterImportForm