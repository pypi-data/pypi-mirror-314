import json
import os
from json import JSONDecodeError
from typing import Any, Dict, Optional

import requests
from requests.adapters import HTTPAdapter, Retry
from requests.models import Response

from pcli.responses import InvalidFilterCriteriaException, InvalidJobManifestException
from pcli.util.formatter import (
    format_instance_type_query,
    format_accelerator_type_query,
)

from perian.models import Name


def get_config_directory():
    return os.path.join(os.path.expanduser("~"), ".config")


def get_perian_config_directory():
    return os.path.join(get_config_directory(), "perian")


def load_instance_type_filter_from_json(filters):
    filter_criteria = None
    try:
        if ".json" in filters:
            full_path = os.path.join(os.path.dirname(__file__), filters)

            # the provided json file could be locally or provided as a full path
            possible_file_paths = [filters, full_path]
            for path in possible_file_paths:
                if os.path.isfile(path):
                    f = open(path)
                    filter_criteria = json.load(f)

            # could not find json file
            if not filter_criteria:
                raise InvalidFilterCriteriaException(
                    "Failed to load JSON file. Please provide the full path to the file."
                )
        else:
            filter_criteria = json.loads(filters)

        return format_instance_type_query(filter_criteria)
    except JSONDecodeError:
        raise InvalidFilterCriteriaException(
            "Failed to load JSON file. The JSON seems to be malformed."
        )


def load_instance_type_filter_from_values(
    cores: Optional[int] = None,
    memory: Optional[int] = None,
    accelerators: Optional[int] = None,
    accelerator_type: Optional[str] = None,
    country_code: Optional[str] = None,
    billing_granularity: Optional[str] = None,
):
    """Create a filter query for instance types based on the provided values."""
    instance_type_filters: Dict[str, Any] = {}

    if cores:
        instance_type_filters["cpu"] = {"cores": cores}

    if memory:
        instance_type_filters["ram"] = {"size": memory}

    if accelerators:
        instance_type_filters["accelerator"] = {"no": accelerators}

    if accelerator_type:
        if "accelerator" in instance_type_filters:
            instance_type_filters["accelerator"]["name"] = Name(accelerator_type)
        else:
            instance_type_filters["accelerator"] = {
                "name": Name(accelerator_type)
            }

    if country_code:
        country_code = validate_and_format_country_code(country_code)
        instance_type_filters["region"] = {"location": country_code, "status": "ACTIVE"}
        
    if billing_granularity:
        instance_type_filters["billing_granularity"] = billing_granularity

    # Add default provider status
    instance_type_filters["provider"] = {"status": "ACTIVE"}

    # Add default options
    instance_type_filters["options"] = {"order": "PRICE"}

    if len(instance_type_filters) == 0:
        raise InvalidFilterCriteriaException(
            "No valid filter criteria were provided. Please adjust your criteria."
        )

    return format_instance_type_query(instance_type_filters)


def validate_and_format_country_code(country_code: str) -> str:
    """Validate and convert the provided country code to uppercase."""
    if len(country_code) != 2:
        raise InvalidFilterCriteriaException(
            "Invalid country code. Please provide a valid two-letter country code. (e.g. DE)"
        )
    return country_code.upper()


def load_job_manifest_from_json(filters):
    job_manifest = None
    try:
        if ".json" in filters:
            full_path = os.path.join(os.path.dirname(__file__), filters)

            # the provided json file could be locally or provided as a full path
            possible_file_paths = [filters, full_path]
            for path in possible_file_paths:
                if os.path.isfile(path):
                    f = open(path)
                    job_manifest = json.load(f)

            # could not find json file
            if not job_manifest:
                raise InvalidJobManifestException(
                    "Failed to load JSON file. Please provide the full path to the file."
                )
        else:
            job_manifest = json.loads(filters)

        return job_manifest
    except JSONDecodeError:
        raise InvalidJobManifestException(
            "Failed to load JSON file. The JSON seems to be malformed."
        )


def load_accelerator_type_filter_from_values(
    memory: int = None, vendor: str = None, name: str = None
):
    accelerator_type_filters = {}

    if memory:
        accelerator_type_filters["memory"] = {"size": memory}

    if vendor:
        accelerator_type_filters["vendor"] = vendor

    if name:
        accelerator_type_filters["name"] = Name(name)

    if len(accelerator_type_filters) == 0:
        raise InvalidFilterCriteriaException(
            "No valid filter criteria were provided. Please adjust your criteria."
        )

    return format_accelerator_type_query(accelerator_type_filters)


def get_with_retry(url: str) -> Response:
    """Get a URL with retries on 5xx errors."""
    session = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
    session.mount(url, HTTPAdapter(max_retries=retries))
    return session.get(url)
