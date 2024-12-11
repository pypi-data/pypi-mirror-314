from typing import Annotated
from uuid import UUID

import typer

from pcli import PerianTyper
from pcli.api.accelerator_type import (
    get_by_id as get_accelerator_type_by_id,
    get_all as get_all_accelerator_types,
    get_by_requirements as get_accelerator_types_by_requirement,
)
from pcli.responses import (
    handle_exception,
    ExceptionLevel,
    InvalidAcceleratorTypeIdException,
    AcceleratorTypeNotFoundException,
    AcceleratorTypeAPIException,
    DefaultApiException,
    InvalidFilterCriteriaException,
    AcceleratorTypeNotFoundException,
)
from pcli.util import load_accelerator_type_filter_from_values
from pcli.util.formatter import (
    print_accelerator_type_description,
    print_accelerator_types_list,
)
from perian import AcceleratorTypeQuery

accelerator_type_command = PerianTyper(
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Find and compare accelerator types",
)


@accelerator_type_command.command("get", help="Get available accelerator types")
@handle_exception(
    InvalidAcceleratorTypeIdException, exit=True, level=ExceptionLevel.WARNING
)
@handle_exception(
    AcceleratorTypeNotFoundException, exit=True, level=ExceptionLevel.WARNING
)
@handle_exception(AcceleratorTypeAPIException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(DefaultApiException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(
    InvalidFilterCriteriaException, exit=True, level=ExceptionLevel.WARNING
)
@handle_exception(
    AcceleratorTypeNotFoundException, exit=True, level=ExceptionLevel.WARNING
)
def get_accelerator_type(
    accelerator_type_id: Annotated[str, typer.Argument(help="ID of accelerator type")] = None,
    memory: Annotated[int, typer.Option(help="Gigabyte of accelerator RAM")] = None,
    vendor: Annotated[str, typer.Option(help="Vendor name of accelerator")] = None,
    name: Annotated[str, typer.Option(help="Name of accelerator")] = None,
    all: Annotated[bool, typer.Option(help="Get all jobs for your account")] = False,
):
    # get accelerator type by specific id
    if not all and accelerator_type_id:
        try:
            accelerator_type_id = UUID(accelerator_type_id)
        except Exception:
            raise InvalidAcceleratorTypeIdException()

        accelerator_type = get_accelerator_type_by_id(accelerator_type_id)
        print_accelerator_type_description(accelerator_type)
    # get all accelerator types
    elif all:
        accelerator_types = get_all_accelerator_types()
        print_accelerator_types_list(accelerator_types)
    # get by requirements
    elif not all and not accelerator_type_id:
        accelerator_type_filters = load_accelerator_type_filter_from_values(
            memory=memory, vendor=vendor, name=name
        )
        # creating accelerator type query
        accelerator_type_query = AcceleratorTypeQuery(**accelerator_type_filters)

        accelerator_types = get_accelerator_types_by_requirement(accelerator_type_query)
        print_accelerator_types_list(accelerator_types)
