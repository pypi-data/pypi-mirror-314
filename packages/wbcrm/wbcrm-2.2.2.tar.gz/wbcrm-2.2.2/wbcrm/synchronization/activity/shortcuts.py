from dynamic_preferences.registries import global_preferences_registry
from wbcore.utils.importlib import import_from_dotted_path

from .backend import SyncBackend


def get_backend() -> "SyncBackend":
    if backend := global_preferences_registry.manager()["wbactivity_sync__sync_backend_calendar"]:
        return import_from_dotted_path(backend)
