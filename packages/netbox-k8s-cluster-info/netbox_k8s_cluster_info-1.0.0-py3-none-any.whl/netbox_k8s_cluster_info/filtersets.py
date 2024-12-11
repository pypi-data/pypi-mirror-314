from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from netbox_k8s_cluster_info.models import K8sClusterType, K8sCluster, K8sService
from tenancy.models import Contact

class K8sClusterTypeFilterSet(NetBoxModelFilterSet):
    """Filter capabilities for K8sClusterType instances."""

    class Meta:
        model = K8sClusterType
        fields = tuple()

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(description__icontains=value)
        )
        return queryset.filter(qs_filter)


class K8sClusterFilterSet(NetBoxModelFilterSet):
    """Filter capabilities for K8sCluster instances."""

    class Meta:
        model = K8sCluster
        #fields = ("k8s_cluster_type",)
        fields = tuple()

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(type__name__icontains=value)
            | Q(contact__name__icontains=value)
        )
        return queryset.filter(qs_filter)


class K8sServiceFilterSet(NetBoxModelFilterSet):
    """Filter capabilities for K8sService instances."""

    class Meta:
        model = K8sService
        fields = ("k8s_cluster",)

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(k8s_cluster__name__icontains=value)
            | Q(namespace__icontains=value)
            | Q(name__icontains=value)
            | Q(application__icontains=value)
        )
        return queryset.filter(qs_filter)
