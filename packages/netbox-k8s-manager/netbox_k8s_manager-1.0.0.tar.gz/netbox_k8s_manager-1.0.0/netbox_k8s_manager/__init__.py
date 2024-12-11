from netbox.plugins import PluginConfig

__version__ = "1.0.0"

class K8sManagerConfig(PluginConfig):
    name = "netbox_k8s_manager"
    verbose_name = "K8s Manager"
    description = "K8s Manager Netbox Plugin."
    version = __version__
    author = "ducna"
    author_email = "ducna@hcd.com.vn"
    base_url = "k8s-manager"
    required_settings = []
    default_settings = {"version_info": False}

config = K8sManagerConfig
