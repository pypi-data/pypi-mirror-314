from pcli import db
from pcli.responses import (
    JobNotFoundException,
    DefaultApiException,
    JobAPIException,
    JobAlreadyDoneException,
    InsufficientQuotaException
)
from pcli.util.organization import validate_organization, generate_organization_header
from perian import (
    JobApi,
    ApiClient,
    Configuration,
    ApiException,
)


def get_by_id(job_id):
    # validating if organization is logged into CLI
    organization_data = validate_organization()

    configuration = Configuration(host=db.get("perian_endpoint"))

    with ApiClient(configuration) as api_client:
        api_instance = JobApi(api_client)

        try:
            api_response = api_instance.get_job_by_id(
                job_id=str(job_id),
                _headers=generate_organization_header(organization_data),
            )
            return api_response.jobs[0]

        except ApiException as e:
            if "No job found" in str(e):
                raise JobNotFoundException(
                    f"No job with ID '[bold underline]{job_id}[/bold underline]' found."
                )
            else:
                raise JobAPIException(JobAPIException.detail + "\n\n" + str(e))
        except Exception as e:
            raise DefaultApiException(DefaultApiException.detail + "\n\n" + str(e))


def get_all():
    # validating if organization is logged into CLI
    organization_data = validate_organization()

    configuration = Configuration(host=db.get("perian_endpoint"))

    with ApiClient(configuration) as api_client:
        api_instance = JobApi(api_client)

        try:
            api_response = api_instance.get_all_jobs(
                _headers=generate_organization_header(organization_data)
            )
            return api_response.jobs

        except ApiException as e:
            raise JobAPIException(JobAPIException.detail + "\n\n" + str(e))
        except Exception as e:
            raise DefaultApiException(DefaultApiException.detail + "\n\n" + str(e))


def cancel_job(job_id):
    # validating if organization is logged into CLI
    organization_data = validate_organization()

    configuration = Configuration(host=db.get("perian_endpoint"))

    with ApiClient(configuration) as api_client:
        api_instance = JobApi(api_client)

        try:
            api_response = api_instance.cancel_job(
                job_id=str(job_id),
                _headers=generate_organization_header(organization_data),
            )
        except ApiException as e:
            if "already complete" in str(e):
                raise JobAlreadyDoneException()
            else:
                raise JobAPIException(JobAPIException.detail + "\n\n" + str(e))
        except Exception as e:
            raise DefaultApiException(DefaultApiException.detail + "\n\n" + str(e))


def create_job(job_request):
    # validating if organization is logged into CLI
    organization_data = validate_organization()

    configuration = Configuration(host=db.get("perian_endpoint"))

    with ApiClient(configuration) as api_client:
        api_instance = JobApi(api_client)

        try:
            api_response = api_instance.create_job(
                create_job_request=job_request,
                _headers=generate_organization_header(organization_data),
            )
            return api_response
        except ApiException as e:
            if "insufficient quota" in str(e):
                raise InsufficientQuotaException()
            raise JobAPIException(JobAPIException.detail + "\n\n" + str(e))
        except Exception as e:
            raise DefaultApiException(DefaultApiException.detail + "\n\n" + str(e))
