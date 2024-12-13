from typing import Callable

from typer.main import TyperCommand, TyperGroup
from typer.models import CommandFunctionType
import click
import rich
import typer

# overwriting typer default rich utils with perian branding
from pcli.util import rich_utils as perian_branding
from .util.db import DB


db = DB()


class PerianGroup(TyperGroup):
    def format_help(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        if not rich:
            return super().format_help(ctx, formatter)
        return perian_branding.rich_format_help(
            obj=self,
            ctx=ctx,
            markup_mode=self.rich_markup_mode,
        )


class PerianCommand(TyperCommand):
    def format_help(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        if not rich:
            return super().format_help(ctx, formatter)
        return perian_branding.rich_format_help(
            obj=self,
            ctx=ctx,
            markup_mode=self.rich_markup_mode,
        )


class PerianTyper(typer.Typer):
    def __init__(self, *args, cls=PerianGroup, **kwargs) -> None:
        super().__init__(*args, cls=cls, **kwargs)

    def command(self, *args, cls=PerianCommand, **kwargs
                ) -> Callable[[CommandFunctionType], CommandFunctionType]:
        return super().command(*args, cls=cls, **kwargs)
