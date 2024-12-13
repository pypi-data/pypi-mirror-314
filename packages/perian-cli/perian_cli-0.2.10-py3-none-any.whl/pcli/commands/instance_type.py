from typing import Annotated, Optional, List
from typing import Annotated
from uuid import UUID

from perian import InstanceTypeView

import typer

from pcli import PerianTyper
from pcli.api.instance_type import get_by_id, get_by_requirements
from pcli.responses import (
    InvalidFilterCriteriaException,
    InstanceTypeApiException,
    DefaultApiException,
    handle_exception,
    ExceptionLevel,
    InvalidInstanceTypeIdException,
    InstanceTypeNotFoundException,
    NoOrganizationException,
    CurrencyAPIException,
    warning,
)
from pcli.util import (
    load_instance_type_filter_from_json,
    load_instance_type_filter_from_values,
)
from pcli.util.formatter import (
    print_instance_types_list,
    print_instance_type_description,
)
from pcli.util.string_similarity import validate_billing_granularity
from perian import InstanceTyperQueryView, ProviderName

instance_type_command = PerianTyper(
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Find and compare instance types",
)


def aggregate_instance_types(
    instance_types: List[InstanceTypeView],
) -> List[InstanceTypeView]:
    """
    Aggregates instance types and combines similar ones into one instance
    Currently this is only necessary for instances types on the same provider in different availability zones
    Only OTC and GCP have multiple availability zones
    This can be enhanced in the future to aggregate the instance types rather than filtering them as currently done
    """
    instance_type_identifiers = []
    aggregated_instance_types = []

    for instance_type in instance_types:
        if (
            instance_type.provider.name == ProviderName.OPEN_TELEKOM_CLOUD
            or instance_type.provider.name == ProviderName.GOOGLE_CLOUD_PLATFORM
        ):
            instance_type_identifier = f"{instance_type.name}_{instance_type.region.name}_{instance_type.zone.name}"
            if instance_type_identifier not in instance_type_identifiers:
                instance_type_identifiers.append(instance_type_identifier)
                aggregated_instance_types.append(instance_type)
        else:
            aggregated_instance_types.append(instance_type)
    return aggregated_instance_types


@instance_type_command.command("get", help="Get available instance types")
@handle_exception(DefaultApiException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(InstanceTypeApiException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(NoOrganizationException, exit=True, level=ExceptionLevel.WARNING)
@handle_exception(InvalidInstanceTypeIdException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(
    InstanceTypeNotFoundException, exit=True, level=ExceptionLevel.WARNING
)
@handle_exception(CurrencyAPIException, exit=True, level=ExceptionLevel.ERROR)
def get_instance_type(
    instance_type_id: Annotated[
        Optional[str], typer.Argument(help="ID of instance type")
    ] = None,
    cores: Annotated[Optional[int], typer.Option(help="Number of cpu cores")] = None,
    memory: Annotated[Optional[int], typer.Option(help="Gigabyte of RAM")] = None,
    accelerators: Annotated[
        Optional[int], typer.Option(help="Number of Accelerators")
    ] = None,
    accelerator_type: Annotated[
        Optional[str],
        typer.Option(
            help="Name of accelerator type. See accelerator-type command for a list of all supported ones"
        ),
    ] = None,
    country_code: Annotated[
        Optional[str], typer.Option(help="Country code (e.g. DE)")
    ] = None,
    billing_granularity: Annotated[
        Optional[str],
        typer.Option(
            help="Billing granularity (PER_SECOND, PER_MINUTE, PER_HOUR, PER_10_MINUTES)"
        ),
    ] = None,
    filters: Annotated[
        Optional[str],
        typer.Option(
            help="Filter criteria to select instance types. A JSON string or the path to a JSON file is expected here"
        ),
    ] = None,
    limit: Annotated[
        int, typer.Option(help="Number of instance types to display")
    ] = 25,
):
    if instance_type_id:
        try:
            instance_type_id = UUID(instance_type_id)
        except Exception:
            raise InvalidInstanceTypeIdException()

        instance_type = get_by_id(instance_type_id)
        print_instance_type_description(instance_type)

    elif not instance_type_id:
        instance_type_filters = None

        if filters:
            instance_type_filters = load_instance_type_filter_from_json(filters)
        else:
            instance_type_filters = load_instance_type_filter_from_values(
                cores=cores,
                memory=memory,
                accelerators=accelerators,
                accelerator_type=accelerator_type,
                country_code=country_code,
                billing_granularity=billing_granularity,
            )

        if billing_granularity:
            validated_granularity = validate_billing_granularity(billing_granularity)
            if not validated_granularity:
                warning(f"Invalid billing granularity: '{billing_granularity}'. Valid options are: PER_SECOND, PER_MINUTE, PER_HOUR, PER_10_MINUTES")
                return
            billing_granularity = validated_granularity

        instance_type_filters = load_instance_type_filter_from_values(
            cores=cores,
            memory=memory,
            accelerators=accelerators,
            accelerator_type=accelerator_type,
            country_code=country_code,
            billing_granularity=billing_granularity,
        )

        # creating instance type query
        instance_type_query = InstanceTyperQueryView(**instance_type_filters)

        # calling API
        instance_types = get_by_requirements(instance_type_query, limit)

        # aggregating instance types
        instance_types = aggregate_instance_types(instance_types)

        if len(instance_types) == 0:
            raise InstanceTypeNotFoundException(
                "No instance types for given filters found."
            )

        print_instance_types_list(instance_types)
