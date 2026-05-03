from .connection_manager import ConnectionManager, manager


def get_connection_manager() -> ConnectionManager:
    return manager
