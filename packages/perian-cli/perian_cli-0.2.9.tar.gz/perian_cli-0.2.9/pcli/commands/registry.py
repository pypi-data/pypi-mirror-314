from datetime import datetime
from typing import Annotated

import typer
import validators
from rich.prompt import Confirm

from pcli import PerianTyper
from pcli import db
from pcli.responses import (
    success,
    warning,
    DuplicateRegistryException,
    InvalidRegistryUrlException,
    NoRegistriesWarning,
    AbortedException,
    handle_exception,
    ExceptionLevel,
)
from pcli.util.formatter import print_registry_list, print_registry_description

registry_subcommand = PerianTyper(
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Manage private docker registries",
)


@registry_subcommand.command("add")
@handle_exception(InvalidRegistryUrlException, exit=True, level=ExceptionLevel.ERROR)
@handle_exception(DuplicateRegistryException, exit=True, level=ExceptionLevel.ERROR)
def add_registry(
    username: Annotated[str, typer.Argument(help="Your container registry username")],
    password: Annotated[
        str, typer.Argument(help="Your container registry password or token")
    ],
    url: Annotated[str, typer.Argument(help="Your container registry url. Dont forget to add the url schema e.g. 'https://'")],
    name: Annotated[
        str, typer.Argument(help="A reference name for this registry")
    ] = "default",
):
    # validating parameter values
    if not validators.url(url):
        raise InvalidRegistryUrlException(
            f"The provided registry url '[bold underline]{url}[/bold underline]' is invalid. Please check the given url and dont forget to add the url schema e.g. 'https://'"
        )

    # getting already stored registry data
    registry_data = db.get("registry")

    # check if registry with this name already exists
    if registry_data and name in registry_data:
        raise DuplicateRegistryException(
            f"A registry with the name '[bold underline]{name}[/bold underline]' already exists."
        )

    # no previous registry exist
    if not registry_data:
        registry_data = {}

    registry_data[name] = {
        "name": name,
        "username": username,
        "password": password,
        "url": url,
        "created": str(datetime.utcnow()),
    }

    # warning about plain text storage
    warning("The registry credentials are stored in plain text locally on your device. Please be aware of this.")

    # saving registry data
    db.set("registry", registry_data)
    success(f"Registry '[bold underline]{name}[/bold underline]' added successfully.")


@registry_subcommand.command("list")
@handle_exception(NoRegistriesWarning, exit=True, level=ExceptionLevel.WARNING)
def list_registry():
    # getting already stored registry data
    registry_data = db.get("registry")

    # no registries available
    if not registry_data:
        raise NoRegistriesWarning()

    print_registry_list(registry_data)


@registry_subcommand.command("get")
@handle_exception(NoRegistriesWarning, exit=True, level=ExceptionLevel.WARNING)
def get_registry(
    name: Annotated[str, typer.Argument(help="A reference name for this registry")]
):
    # getting already stored registry data
    registry_data = db.get("registry")

    # no registries available
    if not registry_data:
        raise NoRegistriesWarning()

    if name not in registry_data:
        raise NoRegistriesWarning(
            f"No registries with the name '[bold underline]{name}[/bold underline]' could be found."
        )

    print_registry_description(registry_data[name])


@registry_subcommand.command("delete")
@handle_exception(NoRegistriesWarning, exit=True, level=ExceptionLevel.WARNING)
@handle_exception(AbortedException, exit=True, level=ExceptionLevel.WARNING)
def delete_registry(
    name: Annotated[str, typer.Argument(help="A reference name for this registry")]
):
    # getting already stored registry data
    registry_data = db.get("registry")

    # no registries available
    if not registry_data:
        raise NoRegistriesWarning()

    if name not in registry_data:
        raise NoRegistriesWarning(
            f"No registries with the name '[bold underline]{name}[/bold underline]' could be found."
        )

    confirm = Confirm.ask(
        f"Are you sure you want to delete the registry '[bold underline]{name}[bold underline]' ?"
    )
    if not confirm:
        raise AbortedException()

    # deleting registry from db
    del registry_data[name]

    # saving registry data
    db.set("registry", registry_data)
    success(f"Registry '[bold underline]{name}[/bold underline]' deleted successfully.")
