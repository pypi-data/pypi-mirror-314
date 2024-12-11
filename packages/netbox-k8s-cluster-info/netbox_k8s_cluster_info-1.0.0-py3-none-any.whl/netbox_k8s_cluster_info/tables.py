from django.db.models import Count, F, Value
import django_tables2 as tables
from netbox.tables import NetBoxTable, ToggleColumn, columns
from netbox_k8s_cluster_info.models import K8sCluster, K8sService, K8sClusterType
from tenancy.models import Contact

class K8sClusterTypeTable(NetBoxTable):
    """Table for displaying K8sClusterType objects."""

    pk = ToggleColumn()
    name = tables.LinkColumn()
    class Meta(NetBoxTable.Meta):
        model = K8sClusterType
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

class K8sClusterTable(NetBoxTable):
    """Table for displaying K8sCluster objects."""

    pk = ToggleColumn()
    name = tables.LinkColumn()
    type = tables.Column()

    class Meta(NetBoxTable.Meta):
        model = K8sCluster
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

class K8sServiceTable(NetBoxTable):
    """Table for displaying K8sCluster objects."""

    pk = ToggleColumn()
    name = tables.LinkColumn()
    class Meta(NetBoxTable.Meta):
        model = K8sService
        fields = (
            "pk",
            "name",
            "application",
            "namespace",
            "memory",
            "cpu",
            "gpu",
            "comment",
            "k8s_cluster",
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
