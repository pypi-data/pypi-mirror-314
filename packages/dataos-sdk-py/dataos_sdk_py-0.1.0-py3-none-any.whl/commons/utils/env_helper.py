import os

from commons.utils.constants import *


def get_depot_service_url():
    return get_env_or_throw(DEPOT_SERVICE_URL)


def get_heimdall_url():
    return get_env_or_throw(HEIMDALL_URL)


def get_hera_url():
    return get_env_or_throw(HERA_URL)


def get_gateway_url():
    return get_env_or_throw(GATEWAY_URL)


def get_secret_dir():
    return get_env_or_throw(DATAOS_SECRET_DIR)


def heimdall_ssl():
    enable_ssl = str(get_env_val(HEIMDALL_SSL)).lower() in ("true", "t", "1")
    return enable_ssl


def get_env_val(key: str):
    return os.environ.get(key)


def get_env_or_throw(key: str):
    value = get_env_val(key)
    if value is None:
        raise Exception("Fatal! env {0} not provided".format(key))
    return value


def get_ca_cert_file():
    ca_cert_file = get_or_else(get_env_val(SSL_CA_CERT_FILE), '/etc/dataos/certs/ca.crt')
    return ca_cert_file


def get_cert_file():
    cert_file = get_or_else(get_env_val(SSL_CERT_FILE), '/etc/dataos/certs/tls.crt')
    return cert_file


def get_key_file():
    key_file = get_or_else(get_env_val(SSL_KEYFILE), '/etc/dataos/certs/tls.key')
    return key_file


def get_key_store_file():
    key_file = get_or_else(get_env_val(SSL_KEYSTORE_PATH), '/etc/dataos/certs/keystore.jks')
    return key_file


def get_key_store_pass():
    key_pass = get_env_or_throw(SSL_KEYSTORE_PASSWORD)
    return key_pass


def get_or_else(optional: str, default: str) -> str:
    if optional is None:
        return default
    else:
        return optional


def get_dataos_fqdn():
    return get_env_or_throw(DATAOS_FQDN)


def get_env_value_or_default(key: str, default=None):
    """
    Retrieves the value of an environment variable by its key.
    If the variable is not set, returns the provided default value.
    If no default value is provided and the variable is not set, raises an exception.

    Args:
        key (str): The name of the environment variable to retrieve.
        default (optional): The default value to return if the environment variable is not set. Defaults to None.

    Returns:
        The value of the environment variable if set, otherwise the default value.

    Raises:
        Exception: If the environment variable is not set and no default value is provided.

    Example:
        # Example with default value
        db_host = get_env_value_or_default("DB_HOST", default="localhost")

        # Example without default value (raises Exception if not set)
        db_host = get_env_value_or_default("DB_HOST")
    """
    value = get_env_val(key)
    if value is None:
        if default is not None:
            return default
        raise Exception(f"Fatal! Environment variable '{key}' not provided and no default value set.")
    return value
