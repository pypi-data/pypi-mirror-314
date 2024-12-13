from pcli import db
from pcli.responses import (
    DefaultApiException,
    InstanceTypeNotFoundException,
    InstanceTypeApiException,
)
from pcli.util.organization import validate_organization, generate_organization_header
from perian import (
    InstanceTypeApi,
    Configuration,
    ApiException,
    ApiClient,
    GetInstanceTypeRequest
)

from pcli.util.currencies import convert_instance_type_currencies, convert_instance_type_billing_granularities


def get_by_id(instance_type_id):
    # validating if organization is logged into CLI
    organization_data = validate_organization()

    configuration = Configuration(host=db.get("perian_endpoint"))

    with ApiClient(configuration) as api_client:
        api_instance = InstanceTypeApi(api_client)

        try:
            api_response = api_instance.get_instance_type_by_id(
                instance_type_id=str(instance_type_id),
                _headers=generate_organization_header(organization_data),
            )

            instance_types = convert_instance_type_currencies(api_response.instance_types)
            instance_types = convert_instance_type_billing_granularities(instance_types)

            return instance_types[0]

        except ApiException as e:
            if "No instance type found" in str(e):
                raise InstanceTypeNotFoundException(
                    f"No instance type with ID '[bold underline]{instance_type_id}[/bold underline]' found."
                )
            else:
                raise InstanceTypeApiException(InstanceTypeApiException.detail + "\n\n" + str(e))
        except Exception as e:
            raise DefaultApiException(DefaultApiException.detail + "\n\n" + str(e))


def get_by_requirements(instance_type_query, limit):
    # validating if organization is logged into CLI
    organization_data = validate_organization()

    configuration = Configuration(host=db.get("perian_endpoint"))

    with ApiClient(configuration) as api_client:
        api_instance = InstanceTypeApi(api_client)
        get_instance_type_request = GetInstanceTypeRequest(
            instance_type_query=instance_type_query
        )

        try:
            api_response = api_instance.get_instance_type_by_requirements(
                get_instance_type_request,
                limit=limit,
                _headers=generate_organization_header(organization_data),
            )

            instance_types = convert_instance_type_currencies(api_response.instance_types)
            instance_types = convert_instance_type_billing_granularities(instance_types)

            return instance_types

        except ApiException as e:
            if "No accelerator type found" in str(e):
                raise InstanceTypeNotFoundException()
            elif "Unknown accelerator name" in str(e):
                raise InstanceTypeNotFoundException(
                    "No accelerator types for given filters found. The given accelerator name is invalid."
                )
            raise InstanceTypeApiException(InstanceTypeApiException.detail + "\n\n" + str(e))
        except Exception as e:
            raise DefaultApiException(DefaultApiException.detail + "\n\n" + str(e))
