from pcli import PerianTyper
from pcli.commands.registry import registry_subcommand
from pcli.commands.currency import currency_subcommand

config_command = PerianTyper(no_args_is_help=True, rich_markup_mode="rich")
config_command.add_typer(registry_subcommand, name="registry")
config_command.add_typer(currency_subcommand, name="currency")


