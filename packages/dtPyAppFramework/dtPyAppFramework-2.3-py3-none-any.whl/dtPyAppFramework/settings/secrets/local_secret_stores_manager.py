from ...paths import ApplicationPaths
from .local_secret_store import LocalSecretStore
import multiprocessing
from threading import Thread
import logging
from enum import Enum

class LocalSecretsManagerCommands(Enum):
    CMD_GET_SECRET = 1
    CMD_SET_SECRET = 2
    CMD_SET_PERSISTENT_SECRET = 3
    CMD_DELETE_SECRET = 4
    CMD_STORE_AVAILABLE = 5
    CMD_GET_INDEX = 6
    CMD_STORE_READ_ONLY = 7
    CMD_EXIT = 8
    CMD_SHUTDOWN = 9
    CMD_SUCCESS = 10
    CMD_STORE_NAMES = 11

class LocalSecretsManagerServer(Thread):

    def __init__(self, application_paths, application_settings):
        super().__init__(name='LocalSecretStoresManager_ServerThread')
        self.application_paths = application_paths
        self.application_settings = application_settings
        self.stores = []
        self.store_names = []
        self.pipe_registry = multiprocessing.Queue()
        self._load_stores()

    def _load_stores(self):
        if not self.application_paths:
            self.application_paths = ApplicationPaths()

        self.stores.append(LocalSecretStore(store_name="User_Local_Store",
                                            store_priority=-0,
                                            root_store_path=self.application_paths.usr_data_root_path,
                                            application_settings=self.application_settings,
                                            app_short_name=self.application_paths.app_short_name))

        try:
            # Add local app secret store (if it exists)
            self.stores.append(LocalSecretStore(store_name="App_Local_Store",
                                                store_priority=1,
                                                root_store_path=self.application_paths.app_data_root_path,
                                                application_settings=self.application_settings,
                                                app_short_name=self.application_paths.app_short_name))
        except Exception as ex:
            print(f'Skipping APP Local Secret Store. {ex}')

        for store in self.stores:
            self.store_names.append(store.store_name)

    def run(self):
        running = True
        while running:
            conn = self.pipe_registry.get()  # Iterate over a copy to allow dynamic modifications
            if conn.poll():  # Check if there is a message from this pipe
                try:
                    command, key, value, store_name = conn.recv()
                    match command:
                        case LocalSecretsManagerCommands.CMD_GET_SECRET:
                            conn.send(self._get_secret(key, value, store_name))

                        case LocalSecretsManagerCommands.CMD_SET_SECRET:
                            conn.send(self._set_secret(key, value, store_name))

                        case LocalSecretsManagerCommands.CMD_SET_PERSISTENT_SECRET:
                            conn.send(self._set_persistent_setting(key, value))

                        case LocalSecretsManagerCommands.CMD_DELETE_SECRET:
                            conn.send(self._delete_secret(key, store_name))

                        case LocalSecretsManagerCommands.CMD_STORE_AVAILABLE:
                            conn.send(self._store_available(store_name))

                        case LocalSecretsManagerCommands.CMD_GET_INDEX:
                            conn.send(self._get_index(store_name))

                        case LocalSecretsManagerCommands.CMD_STORE_READ_ONLY:
                            conn.send(self._store_read_only(store_name))

                        case LocalSecretsManagerCommands.CMD_STORE_NAMES:
                            conn.send(self.store_names)

                        case LocalSecretsManagerCommands.CMD_EXIT:
                            conn.close()
                            logging.warning('Closed Connection following EXIT request.')

                        case LocalSecretsManagerCommands.CMD_SHUTDOWN:
                            running = False

                        case _:
                            logging.error(
                                f'Unrecognised Request: command = {command}, key = {key}, value = {value}, store_name = {store_name}')

                    if not conn.closed:
                        self.pipe_registry.put(conn)

                except EOFError as ex:
                    logging.exception(ex)

            else:
                self.pipe_registry.put(conn)

        while not self.pipe_registry.empty():
            pipe = self.pipe_registry.get()
            pipe.close()
        logging.warning('Closed All Connections following SHUTDOWN request.')
        return

    def _get_store(self, store_name):
        """
        Get a secret store by name.

        Args:
            store_name (str): Name of the secret store.

        Returns:
            Secret store instance if found, else None.
        """
        for store in self.stores:
            if store_name == store.store_name:
                return store
        return None

    def _store_available(self, store_name):
        store: LocalSecretStore = self._get_store(store_name)
        return store.store_available

    def _get_index(self, store_name):
        store: LocalSecretStore = self._get_store(store_name)
        return store.get_index()

    def _store_read_only(self, store_name):
        store: LocalSecretStore = self._get_store(store_name)
        return store.store_read_only

    def _get_secret(self, key, default_value=None, store_name=None):
        value = None
        if len(key.split(".")) == 2 and key.split(".")[0] in self.store_names:
            elements = key.split(".")
            store_name = elements[0]
            key = elements[1]

        for store in self.stores:
            if store_name and store_name == store.store_name:
                if store.store_available:
                    value = store.get_secret(key, None)
                else:
                    logging.error(f'Store {store.store_name} is not available to retrieve secret.')
                break
            elif not store_name:
                if store.store_available:
                    value = store.get_secret(key, None)
                    if value:
                        break

        if not value:
            logging.debug(f'The Secret {key} was not found. Returning default value.')
            value = default_value

        return value

    def _set_persistent_setting(self, key, value):
        for store in self.stores:
            if 'User_Local_Store' == store.store_name:
                if store.store_available and not store.store_read_only:
                    store.set_persistent_setting(key, value)
                else:
                    logging.warning(f'Secrets Store {store.store_name} is either not available or is read only.')
                break
        return LocalSecretsManagerCommands.CMD_SUCCESS

    def _set_secret(self, key, value, store_name='User_Local_Store'):
        if not store_name:
            store_name = 'User_Local_Store'
        for store in self.stores:
            if store_name == store.store_name:
                if store.store_available and not store.store_read_only:
                    store.set_secret(key, value)
                else:
                    logging.warning(f'Secrets Store {store.store_name} is either not available or is read only.')
                break
        return LocalSecretsManagerCommands.CMD_SUCCESS

    def _delete_secret(self, key, store_name='User_Local_Store'):
        for store in self.stores:
            if store_name and store_name == store.name():
                value = store.delete_secret(key)
                break

        return LocalSecretsManagerCommands.CMD_SUCCESS


class LocalSecretStoresManager:

    def __init__(self, application_paths=None, application_settings=None, pipe_registry=None):
        self.application_paths = application_paths
        self.application_settings = application_settings
        self.child_connection = None
        self.server_thread = None
        self.pipe_registry = pipe_registry

        if self.pipe_registry is None and self.server_thread is None:
            self.server_thread = LocalSecretsManagerServer(self.application_paths, self.application_settings)
            self.server_thread.start()

            control_pipe_parent, self.child_connection = multiprocessing.Pipe()
            self.server_thread.pipe_registry.put(control_pipe_parent)

        elif self.pipe_registry is not None:
            parent_conn, self.child_connection = multiprocessing.Pipe()
            self.pipe_registry = pipe_registry
            self.pipe_registry.put(parent_conn)

        else:
            logging.error('Unexpected State for LocalSecretStoresManager')
            raise Exception('Unexpected State for LocalSecretStoresManager')

    def close(self):
        if self.pipe_registry is None and self.server_thread is not None:
            self.child_connection.send((LocalSecretsManagerCommands.CMD_SHUTDOWN, None, None, None))
        elif self.pipe_registry is not None:
            self.child_connection.send((LocalSecretsManagerCommands.CMD_EXIT, None, None, None))
        else:
            logging.error('Unexpected State for LocalSecretStoresManager')
            raise Exception('Unexpected State for LocalSecretStoresManager')

    def get_local_stores_index(self):
        _index = {"User_Local_Store": {}, "App_Local_Store": {}}
        for key in _index:
            try:
                _index[key]['available'] = self.store_available(key)
                _index[key]['index'] = self.get_index(key)
                _index[key]['read_only'] = self.store_read_only(key)
            except Exception as ex:
                logging.error(str(ex))
                _index[key]['available'] = False

        return _index

    @property
    def store_names(self):
        self.child_connection.send((LocalSecretsManagerCommands.CMD_STORE_NAMES, None, None, None))
        return self.child_connection.recv()

    def store_available(self, store_name):
        self.child_connection.send((LocalSecretsManagerCommands.CMD_STORE_AVAILABLE, None, None, store_name))
        return self.child_connection.recv()

    def get_index(self, store_name):
        self.child_connection.send((LocalSecretsManagerCommands.CMD_GET_INDEX, None, None, store_name))
        return self.child_connection.recv()

    def store_read_only(self, store_name):
        self.child_connection.send((LocalSecretsManagerCommands.CMD_STORE_READ_ONLY, None, None, store_name))
        return self.child_connection.recv()

    def get_secret(self, key, default_value=None, store_name=None):
        self.child_connection.send((LocalSecretsManagerCommands.CMD_GET_SECRET, key, default_value, store_name))
        return self.child_connection.recv()

    def set_persistent_setting(self, key, value):
        self.child_connection.send((LocalSecretsManagerCommands.CMD_SET_PERSISTENT_SECRET, key, value, None))
        resp = self.child_connection.recv()
        if resp != LocalSecretsManagerCommands.CMD_SUCCESS:
            logging.error(resp)

    def set_secret(self, key, value, store_name='User_Local_Store'):
        self.child_connection.send((LocalSecretsManagerCommands.CMD_SET_SECRET, key, value, store_name))
        resp = self.child_connection.recv()
        if resp != LocalSecretsManagerCommands.CMD_SUCCESS:
            logging.error(resp)

    def delete_secret(self, key, store_name='User_Local_Store'):
        self.child_connection.send((LocalSecretsManagerCommands.CMD_DELETE_SECRET, key, store_name))
        resp = self.child_connection.recv()
        if resp != LocalSecretsManagerCommands.CMD_SUCCESS:
            logging.error(resp)
