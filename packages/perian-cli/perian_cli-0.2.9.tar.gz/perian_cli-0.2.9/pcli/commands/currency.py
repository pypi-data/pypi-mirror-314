from datetime import datetime
from typing import Annotated

import typer

from pcli import PerianTyper
from pcli import db
from pcli.responses import (
    success
)
from pcli.util.formatter import print_currency_description
from perian.models import Currency

currency_subcommand = PerianTyper(
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Manage currency settings",
)

@currency_subcommand.command("set", help="Set the base currency for the CLI.")
def set_currency(
    currency: Annotated[str, typer.Argument(help="The base currency for the CLI. Allowed arguments are ['EUR', 'USD']")]
):


    db.set("base_currency", currency)
    success(f"Currency set to {currency}.")


@currency_subcommand.command("get", help="Get the base currency for the CLI.")
def get_currency():
    base_currency = Currency(db.get("base_currency"))
    print_currency_description(base_currency)

