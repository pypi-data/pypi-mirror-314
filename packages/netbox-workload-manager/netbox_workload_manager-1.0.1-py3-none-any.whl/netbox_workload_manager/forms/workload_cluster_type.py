from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from netbox_workload_manager.models import WorkloadClusterType
from utilities.forms.fields import CommentField, TagFilterField,DynamicModelChoiceField
from utilities.forms.rendering import FieldSet
from ipam.models import Prefix

class WorkloadClusterTypeForm(NetBoxModelForm):
    """Form for creating a new WorkloadClusterType object."""
    comments = CommentField()
    fieldsets = (
        FieldSet('name', 'description', 'tags'),
    )
    class Meta:
        model = WorkloadClusterType
        
        fields = (
            "name",
            "description",
        )

class WorkloadClusterTypeFilterForm(NetBoxModelFilterSetForm):
    model = WorkloadClusterType
    fieldsets = (FieldSet(None, ("q", "tag")),)
    tag = TagFilterField(model)
