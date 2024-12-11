import os

from pcli import db
from pcli.util import get_perian_config_directory, get_config_directory
from pcli.settings import cli_settings
from perian.models import Currency

def _create_config_directory():
    # creating general config dir if not present
    config_directory = get_config_directory()
    if not os.path.isdir(config_directory):
        os.mkdir(config_directory)

    # creating perian config dir if not present
    perian_config_directory = get_perian_config_directory()
    if not os.path.isdir(perian_config_directory):
        os.mkdir(perian_config_directory)

    # creating db file if not present
    config_file = os.path.join(get_perian_config_directory(), "db.json")
    if not os.path.exists(config_file):
        with open(config_file, "w") as f:
            f.write("{}")
    os.chmod(config_file, 0o600)


def _store_defaults():
    db.set("perian_endpoint", cli_settings.perian_endpoint)

    if db.get("base_currency") is None:
        db.set("base_currency", str(cli_settings.base_currency.value))
    else:
        cli_settings.base_currency = Currency(db.get("base_currency"))


def setup():
    _create_config_directory()
    _store_defaults()
