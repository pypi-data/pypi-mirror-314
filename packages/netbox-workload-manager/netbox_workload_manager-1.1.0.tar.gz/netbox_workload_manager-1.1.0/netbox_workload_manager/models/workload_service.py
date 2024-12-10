from django.db import models
from django.urls import reverse

from netbox.models import NetBoxModel
from utilities.querysets import RestrictedQuerySet

class WorkloadService(NetBoxModel):
    name = models.CharField(max_length=128)
    application = models.CharField(max_length=128, null=True, blank=True)
    namespace = models.CharField(max_length=128, null=True, blank=True)
    memory = models.PositiveIntegerField(null=True, blank=True, verbose_name = 'Memory')
    cpu = models.PositiveIntegerField(null=True, blank=True, verbose_name = 'CPU')
    gpu = models.PositiveIntegerField(null=True, blank=True, verbose_name = 'GPU')
    description = models.CharField(max_length=255, null=True, blank=True)
    comments = models.TextField(blank=True)
    workload_cluster =  models.ForeignKey(to="netbox_workload_manager.WorkloadCluster", on_delete=models.PROTECT,default=None, blank=True,null=True )
    contact = models.ManyToManyField(
        to='tenancy.Contact',
        related_name='workload_service_contact',
        blank=True,
        default=None
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_workload_manager:workloadservice", kwargs={"pk": self.pk})
