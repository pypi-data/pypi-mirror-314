from django.urls import reverse_lazy
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm,NetBoxModelImportForm
from netbox_workload_manager.models import WorkloadCluster, WorkloadClusterType
from utilities.forms.fields import CommentField, TagFilterField, DynamicModelChoiceField, CSVModelChoiceField
from utilities.forms.rendering import FieldSet
from django import forms
from ipam.models import Prefix
from tenancy.models import Contact
from utilities.forms.widgets import APISelect, DatePicker

class WorkloadClusterForm(NetBoxModelForm):
    """Form for creating a new WorkloadClusterType object."""
    comments = CommentField()
    
    # type = DynamicModelChoiceField(
    #     queryset=WorkloadClusterType.objects.all(),
    #     widget=APISelect(attrs={"data-url": reverse_lazy("plugins-api:netbox_workload_manager-api:workloadclustertype-list")}),
    #     required=True,
    # )

    class Meta:
        model = WorkloadCluster
        fields = (
            "name",
            "description",
            "contact",
            "devices",
            "virtualmachine",
            "type",
            "tags",
            "comments",
        )

class WorkloadClusterFilterForm(NetBoxModelFilterSetForm):
    model = WorkloadCluster
    fieldsets = (FieldSet(None, ("q", "tag")),)
    tag = TagFilterField(model)

class WorkloadClusterImportForm(NetBoxModelImportForm):

    # contact = CSVModelChoiceField(
    #     queryset=Contact.objects.all(),
    #     to_field_name='name',
    #     help_text="Contact name"
    # )


    class Meta:
        model = WorkloadCluster
        fields = (
            "name",
            "description",
            "contact",
            "devices",
            "virtualmachine",
            "type",
            "tags",
            "comments",
        )