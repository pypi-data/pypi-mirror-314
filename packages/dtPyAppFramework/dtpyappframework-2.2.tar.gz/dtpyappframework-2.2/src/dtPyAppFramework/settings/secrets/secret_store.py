import string
import random

class AbstractSecretStore(object):
    """
    An abstract class representing a generic secret store.

    Attributes:
        store_name (str): Name of the secret store.
        store_type (str): Type of the secret store.
        store_priority (int): Priority of the secret store.
        application_settings (Settings): An instance of Settings providing application settings.

    Methods:
        __init__(store_name, store_type, store_priority, application_settings): Constructor to initialize the AbstractSecretStore.
        priority(): Get the priority of the secret store.
        get_store_setting(key, default=None): Get a specific setting for the secret store from application settings.
        name(): Get the name of the secret store.
        __str__(): String representation of the secret store.
        get_secret(key, default_value=None): Retrieve a secret from the secret store.
        set_secret(key, value): Set a secret in the secret store.
        delete_secret(key): Delete a secret from the secret store.
        create_secret(name, length=18): Generate a random secret and store it in the secret store.

    Exceptions:
        SecretsStoreException: Custom exception for errors related to secret stores.
    """

    def __init__(self, store_name, store_type, store_priority, application_settings) -> None:
        """
        Initialize the AbstractSecretStore.

        Args:
            store_name (str): Name of the secret store.
            store_type (str): Type of the secret store.
            store_priority (int): Priority of the secret store.
            application_settings (Settings): An instance of Settings providing application settings.
        """
        super().__init__()
        self.store_name = store_name
        self.store_priority = store_priority
        self.store_type = store_type
        self.application_settings = application_settings
        self.store_available: bool = False
        self.store_read_only: bool = True

    def priority(self):
        """Get the priority of the secret store."""
        return self.store_priority

    def get_store_setting(self, key, default=None):
        """
        Get a specific setting for the secret store from application settings.

        Args:
            key (str): Setting key.
            default: Default value if the setting is not found.

        Returns:
            Setting value or default if not found.
        """
        full_key = f'secrets_manager.cloud_stores.{self.store_name}.{key}'
        return self.application_settings.get(full_key, default)

    def name(self):
        """Get the name of the secret store."""
        return self.store_name

    def __str__(self) -> str:
        """String representation of the secret store."""
        return f'{self.store_name}-SecretStore-{self.__hash__()} [Priority: {self.store_priority}]'

    def get_secret(self, key, default_value=None):
        """
        Retrieve a secret from the secret store.

        Args:
            key (str): Key of the secret.
            default_value: Default value to return if the secret is not found.

        Raises:
            NotImplementedError: This method should be implemented in concrete subclasses.

        Returns:
            Secret value if found, else default_value.
        """
        raise NotImplementedError

    def set_secret(self, key, value):
        """
        Set a secret in the secret store.

        Args:
            key (str): Key of the secret.
            value: Value of the secret.

        Raises:
            NotImplementedError: This method should be implemented in concrete subclasses.
        """
        raise NotImplementedError

    def delete_secret(self, key):
        """
        Delete a secret from the secret store.

        Args:
            key (str): Key of the secret.

        Raises:
            NotImplementedError: This method should be implemented in concrete subclasses.
        """
        raise NotImplementedError

    def create_secret(self, name: str, length: int = 18) -> str:
        """
        Generate a random secret and store it in the secret store.

        Args:
            name (str): Key of the secret.
            length (int): Length of the generated secret (default: 18).

        Returns:
            Generated secret value.
        """
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        numbers = string.digits
        symbols = string.punctuation

        secret = random.sample(lower + upper + numbers + symbols, length)
        secret = "".join(secret)

        self.set_secret(key=name, value=secret)
        return secret


class SecretsStoreException(Exception):
    """Custom exception for errors related to secret stores."""
    pass
