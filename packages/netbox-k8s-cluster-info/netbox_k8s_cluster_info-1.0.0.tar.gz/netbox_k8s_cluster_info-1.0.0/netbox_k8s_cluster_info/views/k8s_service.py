from netbox.views import generic
from netbox_k8s_cluster_info import forms, tables, filtersets
from netbox_k8s_cluster_info.models import K8sService


class K8sServiceListView(generic.ObjectListView):
    """View for listing all existing K8s Service."""

    queryset = K8sService.objects.all()
    filterset = filtersets.K8sServiceFilterSet
    filterset_form = forms.K8sServiceFilterForm
    table = tables.K8sServiceTable

class K8sServiceView(generic.ObjectView):
    """Display K8s Service details"""
    queryset = K8sService.objects.all()


class K8sServiceEditView(generic.ObjectEditView):
    """View for editing and creating a K8s Service instance."""

    queryset = K8sService.objects.all()
    form = forms.K8sServiceForm

class K8sServiceDeleteView(generic.ObjectDeleteView):
    """View for deleting a K8sCluster instance"""

    queryset = K8sService.objects.all()

# Delete multiple item 
class K8sServiceBulkDeleteView(generic.BulkDeleteView):
    queryset = K8sService.objects.all()
    table = tables.K8sServiceTable

# Import file to add multiple item 
class K8sServiceBulkImportView(generic.BulkImportView):
    queryset = K8sService.objects.all()
    model_form = forms.K8sServiceImportForm