from datetime import datetime
from decimal import Decimal, getcontext
from typing import List, Optional, Union

from perian.models import (
    BillingGranularity,
    Currency,
    InboundSpeed,
    Name,
    OutboundSpeed,
    Size,
    Speed,
    UnitPrice,
)
from perian.models.job_status import JobStatus
from perian.models.job_view import JobView
from rich import box
from rich import print as rprint
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from pcli.colors import PERIAN_PURPLE_LIGHT, PERIAN_LIME
from pcli.responses import CHECKMARK_EMOJI_UNICODE
from pcli.settings import cli_settings
from pcli.util.string_similarity import validate_billing_granularity

from pcli.colors import PERIAN_PURPLE_LIGHT, PERIAN_LIME
from pcli.responses import CHECKMARK_EMOJI_UNICODE
from pcli.settings import cli_settings


def _format_zone_name(zone_name: str):
    """Formats a provider zone name to a nice string. Especially for default zones."""
    if "DEFAULT" in zone_name:
        return "Default"

    return zone_name


def _format_billing_granularity(billing_granularity: BillingGranularity):
    """Formats a billing granularity to a human-readable string."""
    if billing_granularity == BillingGranularity.PER_SECOND:
        return "Per Second"
    elif billing_granularity == BillingGranularity.PER_MINUTE:
        return "Per Minute"
    elif billing_granularity == BillingGranularity.PER_HOUR:
        return "Per Hour"
    elif billing_granularity == BillingGranularity.PER_10_MINUTES:
        return "Per 10 Minutes"
    else:
        return "Undefined"


def _format_decimal(value: Union[Decimal, str], places: int = 3):
    """Formats a value that can either be a decimal or a string to a decimal with two decimal places that are not rounded."""
    # converting to decimal if the value is a string
    if type(value) is str:
        value = Decimal(value)

    # Setting the context precision high enough to handle the input
    getcontext().prec = 28

    # Shifting the decimal point to the right by 'places' places
    factor = Decimal(10) ** places

    # Multiplying, truncating, and then shifting back
    truncated = (value * factor // Decimal(1)) / factor

    # Formatting the result as a string with the required decimal places
    return f"{truncated:.{places}f}"


def _colorize_text(text, color, additional_markup_parameters=""):
    return (
        "["
        + (additional_markup_parameters + " " if additional_markup_parameters else "")
        + color
        + "] "
        + text
        + "[/"
        + (additional_markup_parameters + " " if additional_markup_parameters else "")
        + color
        + "]"
    )


def _format_job_status(status: JobStatus, only_positive=False):
    if status == JobStatus.SERVERERROR:
        if only_positive:
            return str(status.value)

        return "[bold red] " + str(status.value) + "[/bold red]"
    elif status == JobStatus.DONE:
        return (
            "[bold "
            + PERIAN_LIME
            + "]"
            + str(status.value)
            + "[/bold "
            + PERIAN_LIME
            + " ]"
        )
    else:
        return str(status.value)


def _get_currency_symbol(currency: Currency):
    if currency == Currency.EUR:
        return "€"
    elif currency == Currency.USD:
        return "$"
    if currency == Currency.CHF:
        return "CHF"


def _format_datetime(dt: Optional[datetime]) -> str:
    """Formats a datetime object to a string."""
    if dt:
        return dt.strftime("%d-%m-%Y %H:%M:%S %Z")
    return "-"


def print_instance_types_list(instance_types):
    table = Table(box=box.SIMPLE, safe_box=True)

    columns = [
        "ID",
        "Name",
        "Provider",
        "CPU Cores",
        "RAM",
        "Accelerator",
        "Location",
        "Green Energy",
        "Instance Price ("
        + _get_currency_symbol(cli_settings.base_currency)
        + "/h) + Platform Fee",
    ]

    for column in columns:
        if column == "ID":
            table.add_column(column, no_wrap=True)
        else:
            table.add_column(column)

    for instance_type in instance_types:
        accelerator_data = "-"

        if instance_type.accelerator.no > 0:
            accelerator_data = (
                str(instance_type.accelerator.no)
                + " x "
                + instance_type.accelerator.accelerator_types[0].display_name
                + " ("
                + str(_format_decimal(instance_type.accelerator.memory.size, 2))
                + " GB)"
            )

        instance_price = Decimal(instance_type.price.unit_price)
        platform_fee = Decimal(instance_type.price.unit_price) * Decimal(
            cli_settings.platform_commission_percent / 100
        )
        combined_cost = instance_price + platform_fee

        cost_representation = (
            str(_format_decimal(combined_cost))
            + " ("
            + str(_format_decimal(instance_price))
            + " + "
            + str(_format_decimal(platform_fee))
            + ")"
        )

        table.add_row(
            instance_type.id,
            _colorize_text(instance_type.name, PERIAN_PURPLE_LIGHT, "bold"),
            str(instance_type.provider.name.value),
            str(instance_type.cpu.cores),
            str(_format_decimal(instance_type.ram.size)),
            accelerator_data,
            str(instance_type.region.location.value)
            + " ("
            + str(instance_type.region.city)
            + ")",
            CHECKMARK_EMOJI_UNICODE if instance_type.region.sustainable else None,
            cost_representation,
        )

    console = Console()
    console.print(table)


def print_instance_type_hardware_profile(
    instance_type, as_panel: bool = False, with_general_information=True
):
    no_accelerators = "-"
    accelerator_type = "-"
    total_accelerator_memory = "-"

    if instance_type.accelerator.no > 0:
        no_accelerators = str(instance_type.accelerator.no)
        accelerator_type = instance_type.accelerator.accelerator_types[0].display_name
        total_accelerator_memory = (
            str(_format_decimal(instance_type.accelerator.memory.size, 2)) + " GB"
        )

    if not as_panel:
        table = Table(box=box.SIMPLE)

        columns = [
            "CPU Cores",
            "RAM",
            "Green Energy",
            "No of Accelerators",
            "Accelerator Type",
            "Total Accelerator Memory",
        ]
        row_data = []

        for column in columns:
            table.add_column(column, justify="center")

        table.add_row(
            str(instance_type.cpu.cores),
            _format_decimal(str(instance_type.ram.size), 2),
            CHECKMARK_EMOJI_UNICODE if instance_type.region.sustainable else "",
            no_accelerators,
            accelerator_type,
            total_accelerator_memory,
        )

        console = Console()
        console.print(table)

    elif as_panel:
        Console().print(
            Panel.fit(
                (
                    "[bold underline]" + "Instance Type" + "[/bold underline]"
                    if with_general_information
                    else ""
                )
                + (
                    "[bold underline]" + "Hardware Profile" + "[/bold underline]"
                    if not with_general_information
                    else ""
                )
                + "\n\n"
                + (
                    "ID: "
                    + instance_type.id
                    + " \n"
                    + "Name: "
                    + instance_type.name
                    + " \n"
                    + "Type: "
                    + instance_type.type
                    + "\n\n"
                    + "Provider: "
                    + instance_type.provider.name
                    + " \n"
                    + "Region: "
                    + str(instance_type.region.location.value)
                    + " ("
                    + str(instance_type.region.city)
                    + ")"
                    + " \n"
                    + "Availability Zone: "
                    + _format_zone_name(instance_type.zone.name)
                    + "\n\n"
                    if with_general_information
                    else ""
                )
                + "CPU Cores: "
                + str(instance_type.cpu.cores)
                + "\n"
                + "RAM: "
                + str(_format_decimal(instance_type.ram.size, 2))
                + "\n"
                + "No of Accelerators: "
                + no_accelerators
                + " \n"
                + "Accelerator Type: "
                + accelerator_type
                + " \n"
                + "Total Accelerator Memory: "
                + total_accelerator_memory
            )
        )


def print_instance_type_description(instance_type):
    first_section = []
    first_section.append(
        Panel.fit(
            "[bold underline]"
            + "General Information"
            + "[/bold underline]"
            + "\n\n"
            + "Name: "
            + _colorize_text(instance_type.name, PERIAN_PURPLE_LIGHT, "bold")
            + " \n"
            + "Type: "
            + instance_type.type
            + "\n"
            + "ID: "
            + instance_type.id
        )
    )
    first_section.append(
        Panel.fit(
            "[bold underline]"
            + "Provider"
            + "[/bold underline]"
            + "\n\n"
            + "Name: "
            + instance_type.provider.name
            + " \n"
            + "Region: "
            + instance_type.region.name
            + " \n"
            + "Availability Zone: "
            + _format_zone_name(instance_type.zone.name)
        )
    )
    first_section.append(
        Panel.fit(
            "[bold underline]"
            + "Pricing"
            + "[/bold underline]"
            + "\n\n"
            + "Price: "
            + _format_decimal(instance_type.price.unit_price)
            + " "
            + _get_currency_symbol(cli_settings.base_currency)
            + " \n"
            + "Billing Period: "
            + _format_billing_granularity(cli_settings.billing_granularity)
            + " \n"
        )
    )
    Console().print(Columns(first_section))
    print_instance_type_hardware_profile(
        instance_type, as_panel=True, with_general_information=False
    )


def print_jobs_list(jobs: List[JobView]):
    table = Table(box=box.SIMPLE)

    columns = [
        "ID",
        "Status",
        "Create Time",
        "Start Time",
        "End Time",
        "Container Image",
    ]

    for column in columns:
        if column == "ID":
            table.add_column(column, no_wrap=True)
        else:
            table.add_column(column)

    for job in jobs:
        table.add_row(
            str(job.id),
            _format_job_status(job.status, only_positive=True),
            _format_datetime(job.created_at),
            _format_datetime(job.started_at),
            _format_datetime(job.done_at),
            str(job.docker_metadata.docker_run_parameters.image_name),
        )

    console = Console()
    console.print(table)


def print_job_description(job, related_instance_type=None):
    first_section = []
    first_section.append(
        Panel.fit(
            "[bold underline]"
            + "General Information"
            + "[/bold underline]"
            + "\n\n"
            + "Status: "
            + _format_job_status(job.status)
            + " \n"
            + "ID: "
            + str(job.id)
            + " \n"
            + "Create Time: "
            + _format_datetime(job.created_at)
            + " \n"
            + "Start Time: "
            + _format_datetime(job.started_at)
            + " \n"
            + "End Time: "
            + _format_datetime(job.done_at)
        )
    )

    first_section.append(
        Panel.fit(
            "[bold underline]"
            + "Workload"
            + "[/bold underline]"
            + "\n\n"
            + "Container Image: "
            + str(job.docker_metadata.docker_run_parameters.image_name)
            + " \n"
            + (
                (
                    "Container Tag: "
                    + str(job.docker_metadata.docker_run_parameters.image_tag)
                    + " \n"
                )
                if job.docker_metadata.docker_run_parameters.image_tag
                else ""
            )
            + (
                ("Command: " + str(job.docker_metadata.docker_run_parameters.command))
                if job.docker_metadata.docker_run_parameters.command
                else ""
            )
        )
    )

    # displaying general job data
    Console().print(Columns(first_section))

    # displaying instance type information if applicable
    if related_instance_type:
        print_instance_type_hardware_profile(related_instance_type, as_panel=True)

    # format logs and errors
    _log_text = ""
    if job.logs:
        _log_text = str(job.logs)
    if not job.logs and job.errors:
        _log_text = _colorize_text("No logs available", "", "italic")
    if not job.logs and not job.errors:
        _log_text = _colorize_text("No logs available", PERIAN_PURPLE_LIGHT, "italic")

    _error_text = ""
    if job.errors:
        _error_text = " \n" + "Errors: " + _colorize_text(str(job.errors), "red")

    rprint(
        Panel(
            "[bold underline]"
            + "Job Artifacts"
            + "[/bold underline]"
            + "\n\n"
            + "Logs: "
            + _log_text
            + _error_text
        )
    )


def format_instance_type_query(instance_type_query):
    if "ram" in instance_type_query:
        instance_type_query["ram"]["size"] = Size(
            str(instance_type_query["ram"]["size"])
        )

    if "storage" in instance_type_query:
        if "size" in instance_type_query["storage"]:
            instance_type_query["storage"]["size"] = Size(
                str(instance_type_query["storage"]["size"])
            )
        if "speed" in instance_type_query["storage"]:
            instance_type_query["storage"]["speed"] = Speed(
                str(instance_type_query["storage"]["speed"])
            )

    if "network" in instance_type_query:
        if "inbound_speed" in instance_type_query["network"]:
            instance_type_query["network"]["inbound_speed"] = InboundSpeed(
                str(instance_type_query["storage"]["inbound_speed"])
            )
        if "outbound_speed" in instance_type_query["network"]:
            instance_type_query["network"]["outbound_speed"] = OutboundSpeed(
                str(instance_type_query["storage"]["outbound_speed"])
            )

    if "billing_granularity" in instance_type_query:
        validated = validate_billing_granularity(str(instance_type_query["billing_granularity"]))
        if validated:
            instance_type_query["billing_granularity"] = BillingGranularity(validated)
        else:
            del instance_type_query["billing_granularity"]

    if "accelerator" in instance_type_query:
        if "name" in instance_type_query["accelerator"]:
            instance_type_query["accelerator"]["name"] = Name(
                instance_type_query["accelerator"]["name"]
            )

    # Ensure required fields are present
    if "provider" not in instance_type_query:
        instance_type_query["provider"] = {"status": "ACTIVE"}
    if "options" not in instance_type_query:
        instance_type_query["options"] = {"order": "PRICE"}

    return instance_type_query


def format_accelerator_type_query(accelerator_type_query):
    if "memory" in accelerator_type_query:
        accelerator_type_query["memory"]["size"] = Size(
            str(accelerator_type_query["memory"]["size"])
        )

    return accelerator_type_query


def print_accelerator_type_description(accelerator_type):
    first_section = []
    first_section.append(
        Panel.fit(
            "[bold underline]"
            + "General Information"
            + "[/bold underline]"
            + "\n\n"
            + "Name: "
            + _colorize_text(accelerator_type.display_name, PERIAN_PURPLE_LIGHT, "bold")
            + " \n"
            + "ID: "
            + accelerator_type.id
            + " \n"
        )
    )
    first_section.append(
        Panel.fit(
            "[bold underline]"
            + "Vendor"
            + "[/bold underline]"
            + "\n\n"
            + "Name: "
            + str(accelerator_type.vendor.value)
            + " \n"
        )
    )
    first_section.append(
        Panel.fit(
            "[bold underline]"
            + "Hardware Profile"
            + "[/bold underline]"
            + "\n\n"
            + "Memory: "
            + str(_format_decimal(accelerator_type.memory.size, 2))
            + " GB \n"
        )
    )
    Console().print(Columns(first_section))


def print_accelerator_types_list(accelerator_types: list):
    table = Table(box=box.SIMPLE)

    columns = ["ID", "Name", "Vendor", "Memory (GB)"]

    for column in columns:
        if column == "ID":
            table.add_column(column, no_wrap=True)
        else:
            table.add_column(column)
    for accelerator_type in accelerator_types:
        table.add_row(
            str(accelerator_type.id),
            _colorize_text(
                str(accelerator_type.name.value), PERIAN_PURPLE_LIGHT, "bold"
            ),
            str(accelerator_type.vendor.value),
            str(_format_decimal(accelerator_type.memory.size, 2)),
        )

    console = Console()
    console.print(table)


def print_registry_description(registry):
    registry_table = Table(box=box.SIMPLE)
    registry_table.add_column("Registry Name")
    registry_table.add_column("Username")
    registry_table.add_column("Password")
    registry_table.add_column("URL")
    registry_table.add_column("Created")

    registry_table.add_row(
        _colorize_text(registry["name"], PERIAN_PURPLE_LIGHT, "bold"),
        registry["username"],
        registry["password"],
        registry["url"],
        registry["created"],
    )

    console = Console()
    console.print(registry_table)


def print_registry_list(registries: dict):
    registry_table = Table(box=box.SIMPLE)
    registry_table.add_column("Registry Name")
    registry_table.add_column("Creation Time")

    for registry in registries:
        creation_time = datetime.strptime(
            registries[registry]["created"], "%Y-%m-%d %H:%M:%S.%f"
        )

        registry_table.add_row(
            _colorize_text(registry, PERIAN_PURPLE_LIGHT, "bold"),
            _format_datetime(creation_time),
        )

    console = Console()
    console.print(registry_table)


def print_currency_description(currency: Currency):
    Console().print(
        Panel.fit(
            "[bold underline]"
            + "Currency"
            + "[/bold underline]"
            + "\n\n"
            + str(currency.value)
        )
    )


def print_billing_items_list(billing_items: list, limit: int = 25):
    display_overhang = False
    initial_length = 0

    table = Table(box=box.SIMPLE)

    columns = ["Job ID", "Granularity", "Price"]

    for column in columns:
        if column == "Job ID":
            table.add_column(column, no_wrap=True)
        else:
            table.add_column(column)

    if len(billing_items) > limit:
        display_overhang = True
        initial_length = len(billing_items)
        billing_items = billing_items[:limit]

    for billing_item in billing_items:
        table.add_row(
            str(billing_item.job_id),
            _format_billing_granularity(billing_item.granularity),
            _format_decimal(billing_item.price, 2)
        )

    if display_overhang:
        table.add_row(str(initial_length - limit) + " more ...", "", "")

    console = Console()
    console.print(table)


def print_billing_information(billing_information):
    Console().print(
        Panel.fit(
            "[bold underline]"
            + "Billing Information"
            + "[/bold underline]"
            + "\n\n"
            + "Start Time: "
            + _format_datetime(billing_information.start_time)
            + "\n"
            + "End Time: "
            + _format_datetime(billing_information.end_time)
            + "\n\n"
            + "Total Amount: "
            + _colorize_text(
                str(_format_decimal(billing_information.total_price, 2)),
                PERIAN_PURPLE_LIGHT,
                "bold",
            )
            + " "
            + _get_currency_symbol(billing_information.currency)
        )
    )

    # displaying billing items
    if len(billing_information.items) > 0:
        print_billing_items_list(billing_information.items)


def print_quota_balance(balance, currency):
    Console().print(
        Panel.fit(
            "[bold underline]"
            + "Remaining balance"
            + "[/bold underline]"
            + "\n\n"
            + balance
            + _get_currency_symbol(currency)
            + "\n"
        )
    )

def print_topup_payment_url(topup_payment_url):
    hint_message = (
        "\nPlease follow this URL to process your payment. "
        "Credits will be added to your account once the payment is finalized.\n"
    )
    balance_hint = "\n\n[italic]After completing the payment, please run [bold]perian billing balance[/bold] to view your updated balance.[/italic]"

    Console().print(
        Panel.fit(
            "[bold underline]"
            + "Topup URL"
            + "[/bold underline]"
            + "\n"
            + hint_message
            + "\n\n"
            + topup_payment_url
            + balance_hint
        )
    )
