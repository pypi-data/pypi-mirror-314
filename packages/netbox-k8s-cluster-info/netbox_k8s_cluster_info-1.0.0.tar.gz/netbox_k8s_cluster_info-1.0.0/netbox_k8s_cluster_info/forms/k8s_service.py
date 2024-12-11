from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelImportForm
from netbox_k8s_cluster_info.models import K8sService
from utilities.forms.fields import CommentField, TagFilterField , DynamicModelChoiceField
from utilities.forms.rendering import FieldSet
from ipam.models import Prefix



class K8sServiceForm(NetBoxModelForm):
    """Form for creating a new K8sService object."""
    comments = CommentField()
    
    class Meta:
        model = K8sService
        fields = (
            "name",
            "application",
            "namespace",
            "memory",
            "cpu",
            "gpu",
            "k8s_cluster",
            "contact",
            "description",
            "tags",
            "comments",
        )

class K8sServiceFilterForm(NetBoxModelFilterSetForm):
    model = K8sService
    fieldsets = (FieldSet(None, ("q", "tag")),)
    tag = TagFilterField(model)

class K8sServiceImportForm(NetBoxModelImportForm):

    class Meta:
        model = K8sService
        fields = (
            "name",
            "application",
            "namespace",
            "memory",
            "cpu",
            "gpu",
            "k8s_cluster",
            "contact",
            "description",
            "tags",
            "comments",
        )