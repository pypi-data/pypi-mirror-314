from pcli import db
from pcli.responses import (
    DefaultApiException,
    AcceleratorTypeNotFoundException,
    AcceleratorTypeAPIException,
    AcceleratorTypeNotFoundException,
)
from pcli.util.organization import validate_organization, generate_organization_header
from perian import (
    AcceleratorTypeApi,
    Configuration,
    ApiException,
    ApiClient,
    GetAcceleratorTypeRequest,
)


def get_by_id(accelerator_type_id):
    # validating if organization is logged into CLI
    organization_data = validate_organization()

    configuration = Configuration(host=db.get("perian_endpoint"))

    with ApiClient(configuration) as api_client:
        api_instance = AcceleratorTypeApi(api_client)

        try:
            api_response = api_instance.get_accelerator_type_by_id(
                accelerator_type_id=str(accelerator_type_id),
                _headers=generate_organization_header(organization_data),
            )

            return api_response.accelerator_types[0]

        except ApiException as e:
            if "No accelerator type found" in str(e):
                raise AcceleratorTypeNotFoundException(
                    f"No accelerator type with ID '[bold underline]{accelerator_type_id}[/bold underline]' found."
                )
            else:
                raise AcceleratorTypeAPIException(AcceleratorTypeAPIException.detail + "\n\n" +  str(e))
        except Exception as e:
            raise DefaultApiException(DefaultApiException.detail + "\n\n" +  str(e))


def get_all():
    # validating if organization is logged into CLI
    organization_data = validate_organization()

    configuration = Configuration(host=db.get("perian_endpoint"))

    with ApiClient(configuration) as api_client:
        api_instance = AcceleratorTypeApi(api_client)

        try:
            api_response = api_instance.get_all_accelerator_types(
                _headers=generate_organization_header(organization_data)
            )

            return api_response.accelerator_types

        except ApiException as e:
            raise AcceleratorTypeAPIException(AcceleratorTypeAPIException.detail + "\n\n" +  str(e))
        except Exception as e:
            raise DefaultApiException(DefaultApiException.detail + "\n\n" +  str(e))


def get_by_requirements(accelerator_type_query):
    # validating if organization is logged into CLI
    organization_data = validate_organization()

    configuration = Configuration(host=db.get("perian_endpoint"))

    with ApiClient(configuration) as api_client:
        api_instance = AcceleratorTypeApi(api_client)
        get_accelerator_types_request = GetAcceleratorTypeRequest(
            accelerator_type_query=accelerator_type_query
        )

        try:
            api_response = api_instance.get_accelerator_type_by_requirements(
                get_accelerator_types_request,
                _headers=generate_organization_header(organization_data),
            )

            return api_response.accelerator_types

        except ApiException as e:
            if "No accelerator type found" in str(e):
                raise AcceleratorTypeNotFoundException()
            elif "Unknown accelerator name" in str(e):
                raise AcceleratorTypeNotFoundException(
                    "No accelerator types for given filters found. The given accelerator name is invalid."
                )
            raise AcceleratorTypeAPIException(AcceleratorTypeAPIException.detail + "\n\n" +  str(e))
        except Exception as e:
            raise DefaultApiException(DefaultApiException.detail +  "\n\n" + str(e))
