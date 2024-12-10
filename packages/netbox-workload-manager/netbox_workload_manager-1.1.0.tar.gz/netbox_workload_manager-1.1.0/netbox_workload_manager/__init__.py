from netbox.plugins import PluginConfig

__version__ = "1.1.0"


class WorkLoadManagerConfig(PluginConfig):
    name = "netbox_workload_manager"
    verbose_name = "Workload Manager"
    description = "Workload Manager Netbox Plugin."
    version = __version__
    author = "ducna"
    author_email = "ducna@hcd.com.vn"
    base_url = "workload-manager"
    required_settings = []
    default_settings = {"version_info": False}


config = WorkLoadManagerConfig
