from agently_workflow.utils import PluginManager
from agently_workflow.plugins import install_plugins

global_plugin_manager = PluginManager()
install_plugins(global_plugin_manager)