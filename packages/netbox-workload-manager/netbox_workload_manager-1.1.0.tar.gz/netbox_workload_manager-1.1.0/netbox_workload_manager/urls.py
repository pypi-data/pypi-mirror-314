from django.urls import path
from netbox_workload_manager.models import WorkloadCluster, WorkloadClusterType, WorkloadService
from netbox_workload_manager import views
from netbox.views.generic import ObjectChangeLogView


urlpatterns = (
    # Workload cluster type 
    path("workload-cluster-type/", views.WorkloadClsuterTypeListView.as_view(), name="workloadclustertype_list"),
    path("workload-cluster-type/add/", views.WorkloadClsuterTypeEditView.as_view(), name="workloadclustertype_add"),
    path("workload-cluster-type/<int:pk>/", views.WorkloadClsuterTypeView.as_view(), name="workloadclustertype"),
    path("workload-cluster-type/<int:pk>/edit/", views.WorkloadClsuterTypeEditView.as_view(), name="workloadclustertype_edit"),
    path("workload-cluster-type/<int:pk>/delete/", views.WorkloadClsuterTypeDeleteView.as_view(), name="workloadclustertype_delete"),
    path(
        "workload-cluster-type/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="workloadclustertype_changelog",
        kwargs={"model": WorkloadClusterType},
    ),
    path(
        "workload-cluster-type/delete/", views.WorkloadClsuterTypeBulkDeleteView.as_view(), name="workloadclustertype_bulk_delete"
    ),
    path(
        'workload-cluster-type/import/', 
        views.WorkloadClsuterTypeBulkImportView.as_view(), 
        name='workloadclustertype_import'
    ),
    #import data document 
    #https://netboxlabs.com/docs/netbox/en/stable/plugins/development/forms/

    # Workload Cluster
    path("workload-cluster/", views.WorkloadClsuterListView.as_view(), name="workloadcluster_list"),
    path("workload-cluster/add/", views.WorkloadClsuterEditView.as_view(), name="workloadcluster_add"),
    path("workload-cluster/<int:pk>/", views.WorkloadClsuterView.as_view(), name="workloadcluster"),
    path("workload-cluster/<int:pk>/edit/", views.WorkloadClsuterEditView.as_view(), name="workloadcluster_edit"),
    path("workload-cluster/<int:pk>/delete/", views.WorkloadClsuterDeleteView.as_view(), name="workloadcluster_delete"),
    path(
        "workload-cluster/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="workloadcluster_changelog",
        kwargs={"model": WorkloadCluster},
    ),
    path(
        "workload-cluster/delete/", views.WorkloadClsuterBulkDeleteView.as_view(), name="workloadcluster_bulk_delete"
    ),

    path(
        'workload-cluster/import/', 
        views.WorkloadClsuterBulkImportView.as_view(), 
        name='workloadcluster_import'
    ),
    # Workload Service
    path("workload-service/", views.WorkloadServiceListView.as_view(), name="workloadservice_list"),
    path("workload-service/add/", views.WorkloadServiceEditView.as_view(), name="workloadservice_add"),
    path("workload-service/<int:pk>/", views.WorkloadServiceView.as_view(), name="workloadservice"),
    path("workload-service/<int:pk>/edit/", views.WorkloadServiceEditView.as_view(), name="workloadservice_edit"),
    path("workload-service/<int:pk>/delete/", views.WorkloadServiceDeleteView.as_view(), name="workloadservice_delete"),

    path(
        "workload-service/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="workloadservice_changelog",
        kwargs={"model": WorkloadService},
    ),
    
    path(
        "workload-service/delete/", views.WorkloadServiceBulkDeleteView.as_view(), name="workloadservice_bulk_delete"
    ),

    path(
        'workload-service/import/', 
        views.WorkloadServiceBulkImportView.as_view(), 
        name='workloadservice_import'
    ),
)