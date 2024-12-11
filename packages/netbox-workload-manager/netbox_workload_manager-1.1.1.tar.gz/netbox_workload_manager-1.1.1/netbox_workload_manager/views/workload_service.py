from netbox.views import generic
from netbox_workload_manager import forms, tables, filtersets
from netbox_workload_manager.models import WorkloadService


class WorkloadServiceListView(generic.ObjectListView):
    """View for listing all existing Workload Service."""

    queryset = WorkloadService.objects.all()
    filterset = filtersets.WorkloadServiceFilterSet
    filterset_form = forms.WorkloadServiceFilterForm
    table = tables.WorkloadServiceTable

class WorkloadServiceView(generic.ObjectView):
    """Display Workload Service details"""
    queryset = WorkloadService.objects.all()


class WorkloadServiceEditView(generic.ObjectEditView):
    """View for editing and creating a Workload Service instance."""

    queryset = WorkloadService.objects.all()
    form = forms.WorkloadServiceForm

class WorkloadServiceDeleteView(generic.ObjectDeleteView):
    """View for deleting a WorkloadCluster instance"""

    queryset = WorkloadService.objects.all()

# Delete multiple item 
class WorkloadServiceBulkDeleteView(generic.BulkDeleteView):
    queryset = WorkloadService.objects.all()
    table = tables.WorkloadServiceTable

# Import file to add multiple item 
class WorkloadServiceBulkImportView(generic.BulkImportView):
    queryset = WorkloadService.objects.all()
    model_form = forms.WorkloadServiceImportForm