"""Top-level package for NetBox cesnet_services Plugin."""

__author__ = """Jan Krupa"""
__email__ = "jan.krupa@cesnet.cz"
__version__ = "0.0.1"


from netbox.plugins import PluginConfig


class NetBoxAuthorizeKeysConfig(PluginConfig):
    name = "netbox_authorized_keys"
    verbose_name = "NetBox Authorized key Plugin"
    description = ""
    version = __version__
    base_url = "authorized-keys"


config = NetBoxAuthorizeKeysConfig
