from decimal import Decimal, getcontext

from pcli.util import get_with_retry
from perian.models import Currency
from pcli import db
from pcli.responses import CurrencyAPIException
from perian.models import BillingGranularity
from enum import Enum
from pcli.settings import cli_settings

def get_exchange_rate(base_currency: Currency, target_currency: Currency) -> Decimal:
    """Get the exchange rate from base_currency to target_currency.

    The exchange rate is fetched from frankfurter.app.com and cached for 1 hour."""

    if Currency.UNDEFINED in (base_currency, target_currency):
        raise ValueError("Currency cannot be UNDEFINED")

    url = (
        "https://api.frankfurter.app/latest?"
        f"&from={base_currency.value}"
    )

    try:
        response = get_with_retry(url)
        data = response.json()
    except Exception as e:
        raise CurrencyAPIException(CurrencyAPIException.detail + "\n\n" + str(e)) from e

    exchange_rate = data['rates'][target_currency.value]
    return Decimal(str(exchange_rate))


def convert_instance_type_currencies(instance_types: list):
    base_currency = Currency(db.get("base_currency"))

    for instance_type in instance_types:
        if instance_type.price.currency is not base_currency:
            exchange_rate = get_exchange_rate(base_currency, instance_type.price.currency)
            converted_price = Decimal(instance_type.price.unit_price) * exchange_rate
            instance_type.price.unit_price = str(converted_price)
            instance_type.price.currency = base_currency

    return instance_types

class BillingGranularity(str, Enum):
    PER_SECOND: str = "PER_SECOND"
    PER_MINUTE: str = "PER_MINUTE"
    PER_HOUR: str = "PER_HOUR"
    PER_10_MINUTES: str = "PER_10_MINUTES"
    UNDEFINED: str = "UNDEFINED"

    @classmethod
    def convert_price(
        cls, price: Decimal,
        from_granularity: "BillingGranularity",
        to_granularity: "BillingGranularity",
    ) -> Decimal:
        """Convert a price from one granularity to another.

        Example:
        >>> BillingGranularity.convert_price(0.1, BillingGranularity.PER_SECOND, BillingGranularity.PER_MINUTE)
        6.0"""
        factors = {
            (cls.PER_SECOND, cls.PER_MINUTE): 60,
            (cls.PER_SECOND, cls.PER_HOUR): 3600,
            (cls.PER_SECOND, cls.PER_10_MINUTES): 600,
            (cls.PER_MINUTE, cls.PER_SECOND): 1 / 60,
            (cls.PER_MINUTE, cls.PER_HOUR): 60,
            (cls.PER_MINUTE, cls.PER_10_MINUTES): 10,
            (cls.PER_HOUR, cls.PER_SECOND): 1 / 3600,
            (cls.PER_HOUR, cls.PER_MINUTE): 1 / 60,
            (cls.PER_HOUR, cls.PER_10_MINUTES): 1 / 6,
            (cls.PER_10_MINUTES, cls.PER_SECOND): 1 / 600,
            (cls.PER_10_MINUTES, cls.PER_MINUTE): 1 / 10,
            (cls.PER_10_MINUTES, cls.PER_HOUR): 6,
        }
        if from_granularity == to_granularity:
            return price
        if (from_granularity, to_granularity) in factors:
            return price * factors[(from_granularity, to_granularity)]
        raise ValueError(f"Cannot convert from {from_granularity} to {to_granularity}")


def convert_instance_type_billing_granularities(instance_types: list):
    for instance_type in instance_types:
        if instance_type.price.granularity is not cli_settings.billing_granularity:

            converted_unit_price = BillingGranularity.convert_price(
                Decimal(instance_type.price.unit_price),
                instance_type.price.granularity,
                cli_settings.billing_granularity,
            )
            instance_type.price.unit_price = str(converted_unit_price)
    return instance_types
