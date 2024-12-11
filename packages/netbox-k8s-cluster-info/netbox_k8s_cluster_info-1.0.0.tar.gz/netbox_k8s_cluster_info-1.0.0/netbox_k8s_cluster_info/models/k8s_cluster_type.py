from django.db import models
from django.urls import reverse
from django.utils import safestring

from netbox.models import NetBoxModel
from utilities.querysets import RestrictedQuerySet
from netbox.models.features import TagsMixin

class K8sClusterType(NetBoxModel,TagsMixin):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_k8s_cluster_info:k8sclustertype",  args=[self.pk])