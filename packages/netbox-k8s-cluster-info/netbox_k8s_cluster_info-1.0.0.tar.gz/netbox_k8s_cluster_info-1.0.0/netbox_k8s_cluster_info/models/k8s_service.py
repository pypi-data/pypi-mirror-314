from django.db import models
from django.urls import reverse

from netbox.models import NetBoxModel
from utilities.querysets import RestrictedQuerySet
from netbox.models.features import TagsMixin

class K8sService(NetBoxModel,TagsMixin):
    name = models.CharField(max_length=128)
    application = models.CharField(max_length=128, null=True, blank=True)
    namespace = models.CharField(max_length=128, null=True, blank=True)
    memory = models.PositiveIntegerField(null=True, blank=True, verbose_name = 'Memory')
    cpu = models.PositiveIntegerField(null=True, blank=True, verbose_name = 'CPU')
    gpu = models.PositiveIntegerField(null=True, blank=True, verbose_name = 'GPU')
    description = models.CharField(max_length=255, null=True, blank=True)
    comments = models.TextField(blank=True)
    k8s_cluster =  models.ForeignKey(to="netbox_k8s_cluster_info.K8sCluster", on_delete=models.PROTECT,default=None, blank=True,null=True )
    contact = models.ManyToManyField(
        to='tenancy.Contact',
        related_name='k8s_service_contact',
        blank=True,
        default=None
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_k8s_cluster_info:k8sservice", kwargs={"pk": self.pk})
