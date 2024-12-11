from netbox.plugins import PluginMenuButton, PluginMenuItem
from netbox.choices import ButtonColorChoices


try:
    from netbox.plugins import PluginMenu
    HAVE_MENU = True
except ImportError:
    HAVE_MENU = False
    PluginMenu = PluginMenuItem

menu_buttons = (
    # button k8s cluster type
    PluginMenuItem(
        link="plugins:netbox_k8s_cluster_info:k8sclustertype_list",
        link_text="K8s Cluster Type",
        #permissions=["netbox_k8s_cluster_info.add_k8s_cluster_type"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_k8s_cluster_info:k8sclustertype_add",
                "Add",
                "mdi mdi-plus-thick",
                #permissions=["netbox_k8s_cluster_info.add_k8s_cluster_type"],
            ),
        ),
    ),

    # button k8s cluster 
    PluginMenuItem(
        link="plugins:netbox_k8s_cluster_info:k8scluster_list",
        link_text="K8s Cluster",
        #permissions=["netbox_k8s_cluster_info.add_k8s_cluster"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_k8s_cluster_info:k8scluster_add",
                "Add",
                "mdi mdi-plus-thick",
                #permissions=["netbox_k8s_cluster_info.add_k8s_cluster"],
            ),
        ),
    ),

    # button k8s service
    PluginMenuItem(
        link="plugins:netbox_k8s_cluster_info:k8sservice_list",
        link_text="K8s Service",
        #permissions=["netbox_k8s_cluster_info.add_k8s_service"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_k8s_cluster_info:k8sservice_add",
                "Add",
                "mdi mdi-plus-thick",
                #permissions=["netbox_k8s_cluster_info.add_k8s_service"],
            ),
        ),
    ),
)


if HAVE_MENU:
    menu = PluginMenu(
        label=f'K8s Cluster Info',
        groups=(
            ('K8s Cluster Info', menu_buttons),
        ),
        icon_class='mdi mdi-clipboard-text-multiple-outline'
    )
else:
    # display under plugins
    menu_items = menu_buttons


