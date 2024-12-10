from django.db import models
from django.urls import reverse

from netbox.models import NetBoxModel
from utilities.querysets import RestrictedQuerySet
from utilities.validators import EnhancedURLValidator
from netbox.models.features import TagsMixin

class WorkloadCluster(NetBoxModel,TagsMixin):
    name = models.CharField(max_length=128)
    type = models.ForeignKey(to="netbox_workload_manager.WorkloadClusterType", on_delete=models.PROTECT)
    description = models.CharField(max_length=255, null=True, blank=True)
    comments = models.TextField(blank=True)

    contact = models.ManyToManyField(
        to='tenancy.Contact',
        related_name='workload_cluster_contact',
        blank=True,
        default=None
    )

    devices = models.ManyToManyField(
        to='dcim.Device',
        related_name='workload_cluster_device',
        blank=True,
        default=None
    )

    virtualmachine = models.ManyToManyField(
        to='virtualization.VirtualMachine',
        related_name='workload_clsuter_vm',
        blank=True,
        default=None
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_workload_manager:workloadcluster", kwargs={"pk": self.pk})