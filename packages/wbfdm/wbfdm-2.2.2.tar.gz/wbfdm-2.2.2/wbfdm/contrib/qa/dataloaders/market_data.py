from datetime import date
from enum import Enum
from typing import Iterator

from django.db import connections
from jinjasql import JinjaSql  # type: ignore
from wbcore.contrib.dataloader.dataloaders import Dataloader
from wbcore.contrib.dataloader.utils import dictfetchall
from wbfdm.dataloaders.protocols import MarketDataProtocol
from wbfdm.dataloaders.types import MarketDataDict
from wbfdm.enums import Frequency, MarketData


class DS2MarketData(Enum):
    OPEN = ("Open_", None)
    CLOSE = ("Close_", None)
    HIGH = ("High", None)
    LOW = ("Low", None)
    BID = ("Bid", None)
    ASK = ("Ask", None)
    VWAP = ("VWAP", None)
    VOLUME = ("Volume", None)
    MARKET_CAPITALIZATION = ("ConsolMktVal", 1_000_000)
    SHARES_OUTSTANDING = ("ConsolNumShrs", 1_000)


class DatastreamMarketDataDataloader(MarketDataProtocol, Dataloader):
    def market_data(
        self,
        values: list[MarketData] | None = [MarketData.CLOSE],
        from_date: date | None = None,
        to_date: date | None = None,
        exact_date: date | None = None,
        frequency: Frequency = Frequency.DAILY,
        target_currency: str | None = None,
        **kwargs,
    ) -> Iterator[MarketDataDict]:
        """Get market data for instruments.

        Args:
            queryset (QuerySet["Instrument"]): The queryset of instruments.
            values (list[MarketData]): List of values to include in the results.
            from_date (date | None): The starting date for filtering prices. Defaults to None.
            to_date (date | None): The ending date for filtering prices. Defaults to None.
            frequency (Frequency): The frequency of the requested data

        Returns:
            Iterator[MarketDataDict]: An iterator of dictionaries conforming to the DailyValuationDict.
        """

        lookup = {
            f"{k[0]},{k[1]}": v for k, v in self.entities.values_list("dl_parameters__market_data__parameters", "id")
        }
        value_mapping = [(DS2MarketData[x.name].value, x.value) for x in values or []]

        sql = """
            SELECT
                CONCAT(pricing.InfoCode, ',', ExchIntCode) as external_identifier,
                CONCAT(pricing.InfoCode, ',', ExchIntCode, '_', CONVERT(DATE, MarketDate)) as id,
                CONVERT(DATE, MarketDate) as valuation_date,
                'qa-ds2' as source,
                {% if target_currency %}
                '{{ target_currency|sqlsafe }}' as 'currency',
                {% else %}
                Currency as 'currency',
                {% endif %}
                {% for value in values %}
                {% if target_currency %}
                    COALESCE(fx_rate.midrate, 1) *
                {% endif %}
                {{ value[0][0] | sqlsafe }}{% if value[0][1] %} * {{ value[0][1] | sqlsafe }}{% endif %} as '{{ value[1] | sqlsafe }}'{% if not loop.last %}, {% endif %}
                {% endfor %}
            FROM vw_Ds2Pricing as pricing
            LEFT JOIN DS2MktVal as market_val
                ON pricing.InfoCode = market_val.InfoCode
                AND pricing.MarketDate = market_val.ValDate
            {% if target_currency %}
            LEFT JOIN Ds2FxCode as fx_code
                ON fx_code.FromCurrCode = '{{target_currency|sqlsafe}}'
                AND fx_code.ToCurrCode = pricing.Currency
                AND fx_code.RateTypeCode = 'SPOT'
            LEFT JOIN Ds2FxRate as fx_rate
                ON fx_rate.ExRateIntCode = fx_code.ExRateIntCode
                AND fx_rate.ExRateDate = pricing.MarketDate
            {% endif %}

            WHERE (
                {% for instrument in instruments %}
                    (pricing.InfoCode = {{instrument[0]}} AND ExchIntCode = {{instrument[1]}}) {% if not loop.last %} OR {% endif %}
                {% endfor %}
            )
            AND AdjType = 2
            {% if from_date %} AND MarketDate >= {{ from_date }} {% endif %}
            {% if to_date %} AND MarketDate <= {{ to_date }} {% endif %}
            {% if exact_date %} AND MarketDate = {{ exact_date }} {% endif %}

            ORDER BY MarketDate DESC
        """
        query, bind_params = JinjaSql(param_style="format").prepare_query(
            sql,
            {
                "instruments": self.entities.values_list("dl_parameters__market_data__parameters", flat=True),
                "values": value_mapping,
                "from_date": from_date,
                "to_date": to_date,
                "exact_date": exact_date,
                "target_currency": target_currency,
            },
        )
        with connections["qa"].cursor() as cursor:
            cursor.execute(
                query,
                bind_params,
            )
            for row in dictfetchall(cursor):
                row["instrument_id"] = lookup[row["external_identifier"]]
                yield row
