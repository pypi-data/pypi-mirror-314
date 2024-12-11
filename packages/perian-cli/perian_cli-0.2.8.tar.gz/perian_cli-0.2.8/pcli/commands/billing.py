from datetime import datetime, timezone
from locale import currency
from typing import Annotated
import typer

from pcli import PerianTyper
from pcli.api.billing import generate_bill, get_topup_payment_link, check_balance
from pcli.responses import (
    BillingTimeOrderException,
    BothBillingTimesNeededException,
    DefaultApiException,
    ExceptionLevel,
    handle_exception, OrganizationValidationException, OrganizationInvalidTierException,
)
from pcli.util.formatter import print_billing_information, print_topup_payment_url, print_quota_balance

billing_command = PerianTyper(
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Managed and interact with billing information",
)


@billing_command.command("get", help="Get billing information for a given time")
@handle_exception(DefaultApiException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(BillingTimeOrderException, exit=True, level=ExceptionLevel.WARNING)
@handle_exception(BothBillingTimesNeededException, exit=True, level=ExceptionLevel.WARNING)
def get_bill(
    start_time: Annotated[datetime, typer.Option(
        help="Start time for the billing information. Defaults to the beginning of the last month")] = None,
    end_time: Annotated[datetime, typer.Option(
        help="End time for the billing information. Defaults to the end of the last month")] = None,
):
    """Get billing information for a given time. If no time is provided, the billing information for the last month is returned."""
    if start_time and not end_time:
        raise BothBillingTimesNeededException()

    # adding timezone information to the datetime objects
    if start_time:
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)
    if end_time:
        if end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=timezone.utc)

    billing_information = generate_bill(start_time, end_time)

    print_billing_information(billing_information)


@billing_command.command("balance", help="Display the quota balance")
@handle_exception(DefaultApiException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(OrganizationInvalidTierException, exit=True, level=ExceptionLevel.ERROR)
def get_quota_balance():
    response = check_balance()
    balance = response.current_amount
    currency = response.currency
    print_quota_balance(balance, currency)

@billing_command.command("topup", help="Add topup amount into your quota")
@handle_exception(DefaultApiException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(OrganizationInvalidTierException, exit=True, level=ExceptionLevel.ERROR)
def topup_quota(
        amount: Annotated[str, typer.Option(
            help="Amount to be added to your quota in EUR"
        )]
):
    response = get_topup_payment_link(amount)
    topup_payment_url = response.payment_url
    print_topup_payment_url(topup_payment_url)
