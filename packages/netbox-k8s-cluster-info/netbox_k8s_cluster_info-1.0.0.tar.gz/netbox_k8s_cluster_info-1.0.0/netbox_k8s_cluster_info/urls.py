from django.urls import path
from netbox_k8s_cluster_info.models import K8sCluster, K8sClusterType, K8sService
from netbox_k8s_cluster_info import views
from netbox.views.generic import ObjectChangeLogView


urlpatterns = (
    # K8s cluster type 
    path("k8s-cluster-type/", views.K8sClsuterTypeListView.as_view(), name="k8sclustertype_list"),
    path("k8s-cluster-type/add/", views.K8sClsuterTypeEditView.as_view(), name="k8sclustertype_add"),
    path("k8s-cluster-type/<int:pk>/", views.K8sClsuterTypeView.as_view(), name="k8sclustertype"),
    path("k8s-cluster-type/<int:pk>/edit/", views.K8sClsuterTypeEditView.as_view(), name="k8sclustertype_edit"),
    path("k8s-cluster-type/<int:pk>/delete/", views.K8sClsuterTypeDeleteView.as_view(), name="k8sclustertype_delete"),
    path(
        "k8s-cluster-type/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="k8sclustertype_changelog",
        kwargs={"model": K8sClusterType},
    ),
    path(
        "k8s-cluster-type/delete/", views.K8sClsuterTypeBulkDeleteView.as_view(), name="k8sclustertype_bulk_delete"
    ),
    path(
        'k8s-cluster-type/import/', 
        views.K8sClsuterTypeBulkImportView.as_view(), 
        name='k8sclustertype_import'
    ),

    # K8s Cluster
    path("k8s-cluster/", views.K8sClsuterListView.as_view(), name="k8scluster_list"),
    path("k8s-cluster/add/", views.K8sClsuterEditView.as_view(), name="k8scluster_add"),
    path("k8s-cluster/<int:pk>/", views.K8sClsuterView.as_view(), name="k8scluster"),
    path("k8s-cluster/<int:pk>/edit/", views.K8sClsuterEditView.as_view(), name="k8scluster_edit"),
    path("k8s-cluster/<int:pk>/delete/", views.K8sClsuterDeleteView.as_view(), name="k8scluster_delete"),
    path(
        "k8s-cluster/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="k8scluster_changelog",
        kwargs={"model": K8sCluster},
    ),
    path(
        "k8s-cluster/delete/", views.K8sClsuterBulkDeleteView.as_view(), name="k8scluster_bulk_delete"
    ),

    path(
        'k8s-cluster/import/', 
        views.K8sClsuterBulkImportView.as_view(), 
        name='k8scluster_import'
    ),
    
    # K8s Service
    path("k8s-service/", views.K8sServiceListView.as_view(), name="k8sservice_list"),
    path("k8s-service/add/", views.K8sServiceEditView.as_view(), name="k8sservice_add"),
    path("k8s-service/<int:pk>/", views.K8sServiceView.as_view(), name="k8sservice"),
    path("k8s-service/<int:pk>/edit/", views.K8sServiceEditView.as_view(), name="k8sservice_edit"),
    path("k8s-service/<int:pk>/delete/", views.K8sServiceDeleteView.as_view(), name="k8sservice_delete"),

    path(
        "k8s-service/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="k8sservice_changelog",
        kwargs={"model": K8sService},
    ),

    path(
        "k8s-service/delete/", views.K8sServiceBulkDeleteView.as_view(), name="k8sservice_bulk_delete"
    ),

    path(
        'k8s-service/import/', 
        views.K8sServiceBulkImportView.as_view(), 
        name='k8sservice_import'
    ),
)