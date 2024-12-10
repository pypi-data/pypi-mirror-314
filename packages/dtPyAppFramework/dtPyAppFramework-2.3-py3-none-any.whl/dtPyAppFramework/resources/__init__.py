from ..paths import ApplicationPaths
from ..decorators import singleton

import os
import logging


@singleton()
class ResourceManager(object):
    """
    Singleton class for managing resources within the application.

    Attributes:
        application_paths (ApplicationPaths): Object managing application paths.
        resource_paths (list): List of paths where resources can be located.
    """

    def __init__(self, application_paths=None) -> None:
        """
        Initialize ResourceManager.

        Args:
            application_paths (ApplicationPaths, optional): Object managing application paths.
        """
        super().__init__()
        self.application_paths = application_paths
        if not self.application_paths:
            self.application_paths = ApplicationPaths()
        self.resource_paths = self.__load_default_paths__()
        self._sort_paths()

    def _sort_paths(self):
        self.resource_paths.sort(key=lambda x: x[1])

    def __load_default_paths__(self):
        """
        Load default resource paths.

        Returns:
            list: List of default resource paths.
        """
        return [(os.path.join(self.application_paths.usr_data_root_path, "resources"), 100),
                (os.path.join(self.application_paths.app_data_root_path, "resources"), 200),
                (os.path.join(os.getcwd(), "resources"), 300)]

    def add_resource_path(self, path, priority=10):
        """
        Add a custom resource path.

        Args:
            path (str): Path to be added to the resource paths.
            priority (int): The priority of the path when doing lookups. Lower the number, the higher the priority.
        """
        self.resource_paths.append((path, priority))
        self._sort_paths()

    def remove_resource_path(self, path):
        """
        Remove a custom resource path.

        Args:
            path (str): Path to be removed from the resource paths.
        """
        p_to_remove = None
        for p in self.resource_paths:
            if p[0] == path:
                p_to_remove = p
                break

        if p_to_remove is not None:
            self.resource_paths.remove(p_to_remove)

    def get_resource_path(self, resource):
        """
        Get the full path to a resource.

        Args:
            resource (str): Name of the resource.

        Returns:
            str: Full path to the resource, or None if not found.
        """
        for path in self.resource_paths:
            if os.path.exists(os.path.join(path[0], resource)):
                logging.info(f'Returning resource from: "{os.path.join(path[0], resource)}"')
                return os.path.join(path[0], resource)

        logging.error(f'Resource: "{resource}" could not be found')
        return None
