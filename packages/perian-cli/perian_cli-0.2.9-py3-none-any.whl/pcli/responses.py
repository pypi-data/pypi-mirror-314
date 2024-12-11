from enum import Enum
from functools import wraps

from rich import print as rprint
from rich.panel import Panel
from typer import Exit

from pcli.colors import PERIAN_LIME, PERIAN_PURPLE_LIGHT

CHECKMARK_EMOJI_UNICODE = "[green bold] :heavy_check_mark: [/green bold]"
WARNING_EMOJI_UNICODE = ""
CROSS_EMOJI_UNICODE = ""
MAGNIFYING_GLASS_EMOJI_UNICODE = "\U0001F50D "


class ExceptionLevel(str, Enum):
    ERROR = "Error"
    WARNING = "Warning"
    INFO = "Info"


class DefaultException(Exception):
    message: str = None
    detail: str = None

    def __init__(self, message: str = None):
        # Call the base class constructor with the parameters it needs
        super().__init__(message if message else self.detail)
        self.message = message


def success(message: str):
    rprint(
        Panel(
            "[bold " + PERIAN_LIME + "]" + message + "[/bold " + PERIAN_LIME + "]",
            border_style=PERIAN_LIME,
        )
    )


def error(exception, exit: bool = True):
    rprint(
        Panel(
            CROSS_EMOJI_UNICODE + "[bold red]Error:[/bold red] " + str(exception),
            border_style="red",
        )
    )
    if exit:
        raise Exit(code=1)


def warning(exception, exit: bool = False):
    rprint(
        Panel(
            WARNING_EMOJI_UNICODE
            + "[bold "
            + PERIAN_PURPLE_LIGHT
            + "]Warning:[/bold "
            + PERIAN_PURPLE_LIGHT
            + "] "
            + str(exception),
            border_style=PERIAN_PURPLE_LIGHT,
        )
    )

    if exit:
        raise Exit(code=0)


def info(message: str):
    rprint(message)


class DuplicateRegistryException(DefaultException):
    detail: str = "A registry with the given name already exists."


class InvalidRegistryUrlException(DefaultException):
    detail: str = "The provided registry url is invalid. Please check the given url."


class NoRegistriesWarning(DefaultException):
    detail: str = "No previously saved registries available."


class AbortedException(DefaultException):
    detail: str = "Aborted."


class InvalidMailException(DefaultException):
    detail: str = "The provided e-mail is invalid."


class NoOrganizationException(DefaultException):
    detail: str = "No organization found."


class InvalidFilterCriteriaException(DefaultException):
    detail: str = "Invalid filter criteria provided."


class DefaultApiException(DefaultException):
    detail: str = (
        "An error occurred while connecting to the Sky Platform. Please try again or contact our support."
    )


class InstanceTypeApiException(DefaultException):
    detail: str = (
        "An error occurred while retrieving instance types. Please try again or contact our support."
    )


class InvalidInstanceTypeIdException(DefaultException):
    detail: str = "Invalid or malformed instance type ID. Please check the provided ID."


class InstanceTypeNotFoundException(DefaultException):
    detail: str = (
        "No instance types for given filters found. Please verify your filters."
    )


class JobNotFoundException(DefaultException):
    detail: str = "No job found with provided ID."


class JobAPIException(DefaultException):
    detail: str = (
        "An error occurred while retrieving jobs. Please try again or contact our support."
    )


class InvalidJobIdException(DefaultException):
    detail: str = "Invalid or malformed instance type ID. Please check the provided ID."


class JobAlreadyDoneException(DefaultException):
    detail: str = "The job you are trying to cancel is already done."


class InvalidJobManifestException(DefaultException):
    detail: str = "Malformed job manifest."


class InvalidParametersException(DefaultException):
    detail: str = "The provided parameters are invalid."


class InvalidAcceleratorTypeIdException(DefaultException):
    detail: str = (
        "Invalid or malformed accelerator type ID. Please check the provided ID."
    )


class AcceleratorTypeNotFoundException(DefaultException):
    detail: str = (
        "No accelerator types for given filters found. Please verify your filters."
    )


class AcceleratorTypeAPIException(DefaultException):
    detail: str = (
        "An error occurred while retrieving accelerator types. Please try again or contact our support."
    )


class CurrencyAPIException(DefaultException):
    detail: str = "An error occurred while retrieving currencies."


class BillingTimeOrderException(DefaultException):
    detail: str = (
        "Start date of billing time must be before end date. Please check the provided dates."
    )


class BothBillingTimesNeededException(DefaultException):
    detail: str = (
        "If you provide a start time for the billing period you must specify an end time as well."
    )


class OrganizationValidationException(DefaultException):
    detail: str = "Account validation failed. Please check your login and account data."


class AuthenticationFailedException(DefaultException):
    detail: str = "Authentication failed. Please check your login data."


class InsufficientQuotaException(DefaultException):
    detail: str = (
        "You have insufficient quota to create a new job. Please unlock your account by adding payment information."
    )

class OrganizationInvalidTierException(DefaultException):
    detail: str = (
        "Organization tier must be limited to topup your quota"
    )

def handle_exception(
    which_exception,
    exit_code=1,
    exit: bool = False,
    level: ExceptionLevel = ExceptionLevel.ERROR,
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except which_exception as e:
                if level == ExceptionLevel.ERROR:
                    error(e, exit=exit)
                elif level == ExceptionLevel.WARNING:
                    warning(e, exit=exit)
                if exit:
                    raise Exit(code=exit_code)

        return wrapper

    return decorator
