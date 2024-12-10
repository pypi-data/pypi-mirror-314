import base64
import configparser
import json
import urllib
from urllib.parse import urlparse

from commons.utils import constants


def get_absolute_url(address_info):
    depot_type = str(address_info.get("type")).upper()
    connection = address_info.get("connection")
    if depot_type == "ABFSS":
        return connection.get("abfssUrl")
    elif depot_type == "WASBS":
        return connection.get("wasbsUrl")
    elif depot_type == "GCS":
        return connection.get("gcsUrl")
    elif depot_type == "S3":
        return connection.get("s3Url")
    elif depot_type == "FILE":
        return connection.get("url")
    raise Exception("Unsupported depot type: ", depot_type)


def decode_base64(s):
    s = str(s).strip()
    try:
        return base64.b64decode(s).decode('utf-8')
    except Exception:
        raise Exception("Invalid base64 string: {}".format(s))


def get_content(key: str, secret_res: dict):
    if secret_res.get("data", None) is None:
        raise Exception("Key : '%s' not found in secrets" % "data")
    for item in secret_res['data']:
        if item.get("key", None) is None:
            raise Exception("Key : '%s' not found in secrets" % "key")
        if item["key"] == key:
            if item.get("base64Value", None) is None:
                raise Exception("Key : '%s' not found in secrets" % "base64Value")
            encoded_gcs_conf = item["base64Value"]
            decoded_gcs_conf = decode_base64(encoded_gcs_conf)
            return str(decoded_gcs_conf)
    raise Exception("Key: {0} not found in response".format(key))


def get_properties(decoded_str: str):
    result = {}
    for line in decoded_str.splitlines():
        if not line:
            continue  # Filter out blank lines
        key_value = line.split("=", 1)
        if len(key_value) == 2:
            result[key_value[0]] = key_value[1]
    return result


def write_file(file_name: str, content: str):
    file = open(file_name, "w")
    file.write(content)
    file.close()


def to_url(url_string: str) -> str:
    try:
        parsed_url = urlparse(url_string)
        return parsed_url.geturl()
    except ValueError as e:
        raise AssertionError(f"Malformed URL: {url_string}") from e


def decode_url(dataset_name: str) -> str:
    return urllib.parse.unquote(dataset_name)


def encode_url(dataset_name: str) -> str:
    return urllib.parse.quote(dataset_name)


def encode_url_if_not(url: str) -> str:
    try:
        decode_url(url)
        return url
    except ValueError:
        return encode_url(url)


def get_value_or_throw(key: str, data: dict):
    if data[key] is None:
        raise Exception("Key: {0} not found in abfss properties".format(key))
    return data[key]


def get_value_or_null(key: str, data: dict) -> str:
    if key in data:
        return data[key]
    else:
        return None


def convert_json_string_to_properties(json_string: str) -> dict:
    return json.loads(json_string)

def normalize_base_url(base_url):
    # Check if the base_url does not end with a slash
    if not base_url.endswith('/'):
        # Append a trailing slash to the base_url
        base_url = base_url + '/'
    return base_url
