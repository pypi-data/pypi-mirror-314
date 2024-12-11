from netbox.plugins import PluginMenuButton, PluginMenuItem
from netbox.choices import ButtonColorChoices


try:
    from netbox.plugins import PluginMenu
    HAVE_MENU = True
except ImportError:
    HAVE_MENU = False
    PluginMenu = PluginMenuItem

menu_buttons = (
    # button workload cluster type
    PluginMenuItem(
        link="plugins:netbox_workload_manager:workloadclustertype_list",
        link_text="Workload Cluster Type",
        #permissions=["netbox_workload_manager.add_workload_cluster_type"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_workload_manager:workloadclustertype_add",
                "Add",
                "mdi mdi-plus-thick",
                #permissions=["netbox_workload_manager.add_workload_cluster_type"],
            ),
        ),
    ),

    # button workload cluster 
    PluginMenuItem(
        link="plugins:netbox_workload_manager:workloadcluster_list",
        link_text="Workload Cluster",
        #permissions=["netbox_workload_manager.add_workload_cluster"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_workload_manager:workloadcluster_add",
                "Add",
                "mdi mdi-plus-thick",
                #permissions=["netbox_workload_manager.add_workload_cluster"],
            ),
        ),
    ),

    # button workload service
    PluginMenuItem(
        link="plugins:netbox_workload_manager:workloadservice_list",
        link_text="Workload Service",
        #permissions=["netbox_workload_manager.add_workload_service"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_workload_manager:workloadservice_add",
                "Add",
                "mdi mdi-plus-thick",
                #permissions=["netbox_workload_manager.add_workload_service"],
            ),
        ),
    ),
)


if HAVE_MENU:
    menu = PluginMenu(
        label=f'Workload Cluster',
        groups=(
            ('Workload Cluster', menu_buttons),
        ),
        icon_class='mdi mdi-clipboard-text-multiple-outline'
    )
else:
    # display under plugins
    menu_items = menu_buttons


