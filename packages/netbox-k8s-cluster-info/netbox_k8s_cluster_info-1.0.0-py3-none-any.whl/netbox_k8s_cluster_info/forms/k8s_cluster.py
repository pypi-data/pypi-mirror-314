from django.urls import reverse_lazy
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm,NetBoxModelImportForm
from netbox_k8s_cluster_info.models import K8sCluster, K8sClusterType
from utilities.forms.fields import CommentField, TagFilterField, DynamicModelChoiceField, CSVModelChoiceField
from utilities.forms.rendering import FieldSet
from django import forms
from ipam.models import Prefix
from tenancy.models import Contact
from utilities.forms.widgets import APISelect, DatePicker

class K8sClusterForm(NetBoxModelForm):
    """Form for creating a new K8sClusterType object."""
    comments = CommentField()
    
    # type = DynamicModelChoiceField(
    #     queryset=K8sClusterType.objects.all(),
    #     widget=APISelect(attrs={"data-url": reverse_lazy("plugins-api:netbox_k8s_cluster_info-api:k8sclustertype-list")}),
    #     required=True,
    # )

    class Meta:
        model = K8sCluster
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

class K8sClusterFilterForm(NetBoxModelFilterSetForm):
    model = K8sCluster
    fieldsets = (FieldSet(None, ("q", "tag")),)
    tag = TagFilterField(model)

class K8sClusterImportForm(NetBoxModelImportForm):

    # contact = CSVModelChoiceField(
    #     queryset=Contact.objects.all(),
    #     to_field_name='name',
    #     help_text="Contact name"
    # )


    class Meta:
        model = K8sCluster
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