from django.db import models
from django.urls import reverse
from django.utils import safestring

from netbox.models import NetBoxModel
from utilities.querysets import RestrictedQuerySet

class WorkloadClusterType(NetBoxModel):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_workload_manager:workloadclustertype",  args=[self.pk])