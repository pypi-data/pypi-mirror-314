from netbox.views import generic
from netbox_k8s_cluster_info import forms, tables, filtersets, models
from netbox_k8s_cluster_info.models import K8sClusterType

class K8sClsuterTypeListView(generic.ObjectListView):
    """View for listing all existing K8s Cluster Type."""

    queryset = K8sClusterType.objects.all()
    filterset = filtersets.K8sClusterTypeFilterSet
    filterset_form = forms.K8sClusterTypeForm
    table = tables.K8sClusterTypeTable

class K8sClsuterTypeView(generic.ObjectView):
    """Display K8s Cluster Type details"""
    queryset = K8sClusterType.objects.all()


class K8sClsuterTypeEditView(generic.ObjectEditView):
    """View for editing and creating a K8s Cluster Type instance."""

    queryset = K8sClusterType.objects.all()
    form = forms.K8sClusterTypeForm

class K8sClsuterTypeDeleteView(generic.ObjectDeleteView):
    """View for deleting a K8sClusterType instance"""

    queryset = K8sClusterType.objects.all()

# Delete multiple item 
class K8sClsuterTypeBulkDeleteView(generic.BulkDeleteView):
    queryset = K8sClusterType.objects.all()
    table = tables.K8sClusterTypeTable

# Import file to add multiple item 
class K8sClsuterTypeBulkImportView(generic.BulkImportView):
    queryset = K8sClusterType.objects.all()
    model_form = forms.K8sClusterTypeImportForm