from datetime import date as Date
from decimal import Decimal

from pydantic import Field

from factored_api.models.base import ContractModel, contract_config
from factored_api.models.enums import Currency


class DailyExchangeRate(ContractModel):
    """Daily exchange rates for currency conversion."""

    model_config = contract_config(
        "daily_exchange_rates",
        kind="reference",
        source="Reference",
        partition="daily",
        primary_key=["date", "source_currency", "target_currency"],
    )

    date: Date = Field(..., description="Exchange rate date")
    source_currency: Currency = Field(..., description="Source currency")
    target_currency: Currency = Field(..., description="Target currency")
    exchange_rate: Decimal = Field(..., max_digits=12, decimal_places=6, description="Exchange rate")
    buy_rate: Decimal | None = Field(
        default=None,
        max_digits=12,
        decimal_places=6,
        description="Bank buy rate",
    )
    sell_rate: Decimal | None = Field(
        default=None,
        max_digits=12,
        decimal_places=6,
        description="Bank sell rate",
    )
    source: str | None = Field(default=None, max_length=50, description="Exchange rate source")
