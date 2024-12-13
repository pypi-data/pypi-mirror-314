import os
from typing import Optional
from pydantic_settings import BaseSettings
from perian.models import Currency, BillingGranularity
from decimal import Decimal


class Settings(BaseSettings):
    perian_endpoint: Optional[str] = (
        "https://api.perian.cloud"
        if not os.getenv("PERIAN_CLI_DEV_MODE")
        else "http://localhost:8000"
    )
    base_currency: Currency = Currency.EUR
    billing_granularity: BillingGranularity = BillingGranularity.PER_HOUR
    platform_commission_percent: Decimal = 7.5
    version: str = "0.2.10"


cli_settings = Settings()