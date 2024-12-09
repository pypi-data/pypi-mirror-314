from django.db.models import Count, F, Value
import django_tables2 as tables
from netbox.tables import NetBoxTable, ToggleColumn, columns
from netbox_workload_manager.models import WorkloadCluster, WorkloadService, WorkloadClusterType


class WorkloadClusterTypeTable(NetBoxTable):
    """Table for displaying WorkloadClusterType objects."""

    pk = ToggleColumn()
    name = tables.LinkColumn()
    class Meta(NetBoxTable.Meta):
        model = WorkloadClusterType
        fields = (
            "pk",
            "name",
            "tags",
            "description",
        )

        default_columns = (
            "pk",
            "name",
            "description",
        )

class WorkloadClusterTable(NetBoxTable):
    """Table for displaying WorkloadCluster objects."""

    pk = ToggleColumn()
    name = tables.LinkColumn()
    type = tables.Column()

    class Meta(NetBoxTable.Meta):
        model = WorkloadCluster
        fields = (
            "pk",
            "name",
            "type",
            "contact",
            "devices"
            "virtualmachine",
            "comment",
            "description",
        )

        default_columns = (
            "pk",
            "name",
            "type",
            "contact",
        )

class WorkloadServiceTable(NetBoxTable):
    """Table for displaying WorkloadCluster objects."""

    pk = ToggleColumn()
    name = tables.LinkColumn()
    class Meta(NetBoxTable.Meta):
        model = WorkloadService
        fields = (
            "pk",
            "name",
            "application",
            "namespace",
            "memory",
            "cpu",
            "gpu",
            "comment",
            "workload_cluster",
            "description",
            "contact",
        )
        
        default_columns = (
            "pk",
            "name",
            "application",
            "namespace",
            "memory",
            "cpu",
            "gpu",
            "contact",
        )
