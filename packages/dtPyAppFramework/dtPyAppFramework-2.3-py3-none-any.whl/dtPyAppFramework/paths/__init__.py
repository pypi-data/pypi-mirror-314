import platform
import os
import shutil
import logging

from multiprocessing import current_process
from ..decorators import singleton


@singleton()
class ApplicationPaths(object):
    """
    Singleton class for managing application paths based on the operating system.

    Attributes:
        app_short_name (str): Short name or abbreviation of the application.
        forced_os (str): Forced operating system type.
        spawned_instance (bool): Indicates whether it's a spawned instance.
        auto_create (bool): Automatically create directories if True.
        clean_temp (bool): Clean temporary directory if True.
        forced_dev_mode (bool): Force development mode if True.
        worker_id (int): Worker ID for spawned instances.
    """

    def __init__(self, app_short_name, forced_os=None, forced_dev_mode=False, auto_create=True,
                 clean_temp=True, spawned_instance=False, worker_id=None, *args, **kwargs) -> None:
        super().__init__()
        # Initialization of attributes
        self.app_short_name = app_short_name
        self.forced_os = forced_os
        self.spawned_instance = spawned_instance
        self.auto_create = auto_create
        self.clean_temp = clean_temp
        self.forced_dev_mode = forced_dev_mode
        self.worker_id = worker_id

        # Set development mode environment variable
        if self.forced_dev_mode:
            os.environ['DEV_MODE'] = "True"

        # Initialise various paths
        self.logging_root_path = self.__init_logging_root_path()
        self.app_data_root_path = self.__init_app_data_root_path()
        self.usr_data_root_path = self.__init_usr_data_root_path()
        self.tmp_root_path = self.__init_tmp_root_path()

        # Initialise directories
        self.__init_directories()

    def log_paths(self):
        """
        Log the paths for debugging purposes.
        """
        logging.info(f'Logging Root Path: {self.logging_root_path}')
        logging.info(f'Application Data Root Path: {self.app_data_root_path}')
        logging.info(f'User Data Root Path: {self.usr_data_root_path}')
        logging.info(f'Temp Root Path: {self.tmp_root_path}')

    def __init_directories(self):
        """
        Initialize directories based on configuration.
        """
        # Clean temporary directory if configured
        if self.clean_temp and os.path.exists(self.tmp_root_path):
            shutil.rmtree(self.tmp_root_path, ignore_errors=False)

        # Automatically create directories if configured
        if self.auto_create:
            os.makedirs(self.tmp_root_path, exist_ok=True)
            os.makedirs(self.logging_root_path, exist_ok=True)
            os.makedirs(self.usr_data_root_path, exist_ok=True)

            try:
                os.makedirs(self.app_data_root_path, exist_ok=True)
            except Exception as ex:
                print(f'Skipping creation of application data path {self.app_data_root_path}. {ex}')

    def __os(self):
        """
        Get the operating system type.

        Returns:
            str: Operating system type.
        """
        if self.forced_os:
            return self.forced_os
        else:
            return platform.system()

    def __init_logging_root_path(self):
        """
        Initialize the logging root path based on the operating system.

        Returns:
            str: Logging root path.
        """
        _path = None
        if os.environ.get("DEV_MODE", None):
            _path = f'{os.getcwd()}/logs'
        elif self.__os() == "Windows":
            _path = f'{os.environ.get("LOCALAPPDATA")}/{self.app_short_name}/logs'
        elif self.__os() == "Darwin":
            _path = f'{os.path.expanduser("~/Library/Logs")}/{self.app_short_name}'
        elif self.__os() == "Linux":
            _path = f'/var/log/{self.app_short_name}'

        os.environ['dt_LOGGING_PATH'] = _path
        return _path

    def __init_app_data_root_path(self):
        """
        Initialize the application data root path based on the operating system.

        Returns:
            str: Application data root path.
        """
        _path = None
        if os.environ.get("DEV_MODE", None):
            _path = f'{os.getcwd()}/data/app'
        elif self.__os() == "Windows":
            _path = f'{os.environ.get("ALLUSERSPROFILE")}/{self.app_short_name}'
        elif self.__os() == "Darwin":
            _path = f'{os.path.expanduser("/Library/Application Support")}/{self.app_short_name}'
        elif self.__os() == "Linux":
            _path = f'/etc/{self.app_short_name}'

        os.environ['dt_APP_DATA'] = _path
        return _path

    def __init_usr_data_root_path(self):
        """
        Initialize the user data root path based on the operating system.

        Returns:
            str: User data root path.
        """
        _path = None
        if os.environ.get("DEV_MODE", None):
            _path = f'{os.getcwd()}/data/usr'
        elif self.__os() == "Windows":
            _path = f'{os.environ.get("APPDATA")}/{self.app_short_name}'
        elif self.__os() == "Darwin":
            _path = f'{os.path.expanduser("~/Library/Application Support")}/{self.app_short_name}'
        elif self.__os() == "Linux":
            _path = f'{os.path.expanduser("~/.config")}/{self.app_short_name}'

        os.environ['dt_USR_DATA'] = _path
        return _path

    def __init_tmp_root_path(self):
        """
        Initialize the temporary root path based on the operating system.

        Returns:
            str: Temporary root path.
        """
        _path = None
        if os.environ.get("DEV_MODE", None):
            _path = f'{os.getcwd()}/temp'
        elif self.__os() == "Windows":
            _path = f'{os.environ.get("TEMP")}/{self.app_short_name}'
        elif self.__os() == "Darwin":
            _path = f'{os.environ.get("TMPDIR")}{self.app_short_name}'
        elif self.__os() == "Linux":
            _path = f'{os.path.expanduser("/tmp")}/{self.app_short_name}'

        if self.spawned_instance:
            _path = f'{_path}/{self.worker_id}'

        os.environ['dt_TMP'] = _path
        return _path
