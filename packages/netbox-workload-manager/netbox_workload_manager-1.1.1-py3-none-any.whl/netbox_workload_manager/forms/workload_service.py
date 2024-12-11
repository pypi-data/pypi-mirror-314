from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelImportForm
from netbox_workload_manager.models import WorkloadService
from utilities.forms.fields import CommentField, TagFilterField , DynamicModelChoiceField
from utilities.forms.rendering import FieldSet
from ipam.models import Prefix



class WorkloadServiceForm(NetBoxModelForm):
    """Form for creating a new WorkloadService object."""
    comments = CommentField()
    
    class Meta:
        model = WorkloadService
        fields = (
            "name",
            "application",
            "namespace",
            "memory",
            "cpu",
            "gpu",
            "workload_cluster",
            "contact",
            "description",
            "tags",
            "comments",
        )

class WorkloadServiceFilterForm(NetBoxModelFilterSetForm):
    model = WorkloadService
    fieldsets = (FieldSet(None, ("q", "tag")),)
    tag = TagFilterField(model)

class WorkloadServiceImportForm(NetBoxModelImportForm):

    class Meta:
        model = WorkloadService
        fields = (
            "name",
            "application",
            "namespace",
            "memory",
            "cpu",
            "gpu",
            "workload_cluster",
            "contact",
            "description",
            "tags",
            "comments",
        )