from netbox.views import generic
from netbox_k8s_cluster_info import forms, tables, filtersets
from netbox_k8s_cluster_info.models import K8sCluster

class K8sClsuterListView(generic.ObjectListView):
    """View for listing all existing K8s Cluster."""

    queryset = K8sCluster.objects.all()
    filterset = filtersets.K8sClusterFilterSet
    filterset_form = forms.K8sClusterForm
    table = tables.K8sClusterTable
    
class K8sClsuterView(generic.ObjectView):
    """Display K8s Cluster details"""
    queryset = K8sCluster.objects.all()

class K8sClsuterEditView(generic.ObjectEditView):
    """View for editing and creating a K8s Cluster instance."""

    queryset = K8sCluster.objects.all()
    form = forms.K8sClusterForm

class K8sClsuterDeleteView(generic.ObjectDeleteView):
    """View for deleting a K8sCluster instance"""

    queryset = K8sCluster.objects.all()

# Delete multiple item 
class K8sClsuterBulkDeleteView(generic.BulkDeleteView):
    queryset = K8sCluster.objects.all()
    table = tables.K8sClusterTable

# Import file to add multiple item 
class K8sClsuterBulkImportView(generic.BulkImportView):
    queryset = K8sCluster.objects.all()
    model_form = forms.K8sClusterImportForm