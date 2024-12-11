from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelImportForm
from netbox_k8s_cluster_info.models import K8sClusterType
from utilities.forms.fields import CommentField, TagFilterField,DynamicModelChoiceField
from utilities.forms.rendering import FieldSet

class K8sClusterTypeForm(NetBoxModelForm):
    """Form for creating a new K8sClusterType object."""
    class Meta:
        model = K8sClusterType
        fields = (
            "name",
            "tags",
            "description",
        )

# Delete multiple item 
class K8sClusterTypeFilterForm(NetBoxModelFilterSetForm):
    model = K8sClusterType
    fieldsets = (FieldSet(None, ("q", "tag")),)
    tag = TagFilterField(model)

# Import file to add multiple item 
class K8sClusterTypeImportForm(NetBoxModelImportForm):
    class Meta:
        model = K8sClusterType
        fields = (
            "name",
            "tags",
            "description",
        )