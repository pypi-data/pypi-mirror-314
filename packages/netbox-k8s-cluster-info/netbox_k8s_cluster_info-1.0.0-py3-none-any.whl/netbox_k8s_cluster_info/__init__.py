from netbox.plugins import PluginConfig

__version__ = "1.0.0"

class K8sClusterInfoConfig(PluginConfig):
    name = "netbox_k8s_cluster_info"
    verbose_name = "K8s Cluster Info"
    description = "K8s Cluster Info Netbox Plugin."
    version = __version__
    author = "ducna"
    author_email = "ducna@hcd.com.vn"
    base_url = "k8s-cluster-info"
    required_settings = []
    default_settings = {"version_info": False}

config = K8sClusterInfoConfig
