from datetime import datetime, timedelta

from pcli.util.organization import validate_organization, generate_organization_header
from pcli import db

from pcli.responses import (
    DefaultApiException,
    BillingTimeOrderException, OrganizationInvalidTierException
)

from perian import (
    BillingApi,
    Configuration,
    ApiException,
    ApiClient, CreditTopUpRequest, Amount, BillingGranularity
)

from pcli.settings import cli_settings


def generate_bill(start_time, end_time):
    if not start_time and not end_time:
        start_time = datetime.now() - timedelta(days=7)
        end_time = datetime.now()
    # validating if organization is logged into CLI
    organization_data = validate_organization()

    configuration = Configuration(host=db.get("perian_endpoint"))

    with ApiClient(configuration) as api_client:
        api_instance = BillingApi(api_client)

        try:
            api_response = api_instance.generate_bill(
                organization=organization_data['name'],
                start_time=start_time,
                end_time=end_time,
                currency=cli_settings.base_currency.value,
                _headers=generate_organization_header(organization_data),
            )
            return api_response

        except ApiException as e:
            if "Start date must be before end date" in str(e):
                raise BillingTimeOrderException(BillingTimeOrderException.detail + "\n\n" + "Default of start time is the beginning of the last month and the default of end time is the end of the last month.")
            raise e
        except Exception as e:
            raise DefaultApiException(DefaultApiException.detail + "\n\n" + str(e))

def check_balance():
    organization_data = validate_organization()
    configuration = Configuration(host=db.get("perian_endpoint"))

    with ApiClient(configuration) as api_client:
        api_instance = BillingApi(api_client)

        try:
            api_response = api_instance.get_remaining_credits(
                _headers=generate_organization_header(organization_data),
            )
            return api_response


        except ApiException as e:
            if "This organization is on an unlimited plan" in str(e):
                raise OrganizationInvalidTierException()
            raise e

        except Exception as e:
            raise DefaultApiException(DefaultApiException.detail + "\n\n" + str(e))

def get_topup_payment_link(amount):
    organization_data = validate_organization()
    configuration = Configuration(host=db.get("perian_endpoint"))

    with ApiClient(configuration) as api_client:
        api_instance = BillingApi(api_client)

        try:
            amount = Amount(amount)
            topup_request = CreditTopUpRequest(amount=amount)
            api_response = api_instance.quota_top_up(
                topup_request,
                _headers=generate_organization_header(organization_data),
            )
            return api_response


        except ApiException as e:
            if "This organization is on an unlimited plan" in str(e):
                raise OrganizationInvalidTierException()
            raise e

        except Exception as e:
            raise DefaultApiException(DefaultApiException.detail + "\n\n" + str(e))
