from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelImportForm
from netbox_workload_manager.models import WorkloadClusterType
from utilities.forms.fields import CommentField, TagFilterField,DynamicModelChoiceField
from utilities.forms.rendering import FieldSet

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

# Delete multiple item 
class WorkloadClusterTypeFilterForm(NetBoxModelFilterSetForm):
    model = WorkloadClusterType
    fieldsets = (FieldSet(None, ("q", "tag")),)
    tag = TagFilterField(model)

# Import file to add multiple item 
class WorkloadClusterTypeImportForm(NetBoxModelImportForm):
    class Meta:
        model = WorkloadClusterType
        fields = ('name', 'description')