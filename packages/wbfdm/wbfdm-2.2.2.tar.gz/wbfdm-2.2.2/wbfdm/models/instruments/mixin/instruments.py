import calendar
import math
from collections import defaultdict
from contextlib import suppress
from datetime import date, timedelta
from decimal import Decimal
from typing import Dict, Optional

import numpy as np
import pandas as pd
from pandas.tseries.offsets import BDay
from wbcore.contrib.currency.models import CurrencyFXRates
from wbfdm.analysis.financial_analysis.financial_statistics_analysis import (
    FinancialStatistics,
)
from wbfdm.backends.dto import PriceDTO
from wbfdm.enums import MarketData
from wbfdm.models.instruments.instrument_prices import InstrumentPrice


class InstrumentPMSMixin:
    def get_prices_df_with_calculated(self, market_data: MarketData = MarketData.CLOSE, **kwargs) -> pd.DataFrame:
        prices = pd.DataFrame(self.get_prices(values=[market_data], **kwargs)).rename(
            columns={"valuation_date": "date"}
        )
        if "calculated" not in prices.columns:
            prices["calculated"] = False

        if not prices.empty and market_data.value in prices.columns:
            prices = prices[[market_data.value, "calculated", "date"]].sort_values(by="calculated")
            prices = prices.groupby("date").first()
            prices.index = pd.to_datetime(prices.index)
            prices = prices.replace([np.inf, -np.inf, np.nan], None)
            return prices.sort_index()
        return pd.DataFrame()

    def get_prices_df(self, market_data: MarketData = MarketData.CLOSE, **kwargs) -> pd.Series:
        prices = self.get_prices_df_with_calculated(market_data=market_data, **kwargs)

        if market_data.value in prices.columns:
            return prices[market_data.value].astype(float)
        return pd.Series(dtype="float64")

    def get_price(self, val_date: date, price_date_timedelta: int = 3) -> Decimal:
        if self.is_cash:
            return Decimal(1)
        return self._build_dto(val_date, price_date_timedelta=price_date_timedelta).close

    def _build_dto(self, val_date: date, price_date_timedelta: int = 3) -> PriceDTO:  # for backward compatibility
        try:
            price = self.valuations.get(date=val_date)
            close = float(price.net_value)
            return PriceDTO(
                pk=price.id,
                instrument=self.id,
                date=val_date,
                open=close,
                close=close,
                high=close,
                low=close,
                volume=close,
                market_capitalization=price.market_capitalization,
                outstanding_shares=float(price.outstanding_shares) if price.outstanding_shares else None,
            )
        except InstrumentPrice.DoesNotExist:
            prices = sorted(
                self.get_prices(from_date=(val_date - BDay(price_date_timedelta)).date(), to_date=val_date),
                key=lambda x: x["valuation_date"],
                reverse=True,
            )
            if (
                prices
                and (p := prices[0])
                and (close := p.get("close", None))
                and (p_date := p.get("valuation_date", None))
            ):
                return PriceDTO(
                    pk=p["id"],
                    instrument=self.id,
                    date=p_date,
                    open=p.get("open", None),
                    close=close,
                    high=p.get("high", None),
                    low=p.get("low", None),
                    volume=p.get("volume", None),
                    market_capitalization=p.get("market_capitalization", None),
                    outstanding_shares=p.get("outstanding_shares", None),
                )
            raise ValueError("Not price was found")

    # Instrument Prices Utility Functions
    @classmethod
    def _compute_performance(cls, prices: pd.Series, freq: str = "BME") -> pd.DataFrame:
        if prices.empty:
            raise ValueError("Price series cannot be empty")
        performance = FinancialStatistics(prices).compute_performance(freq=freq)  # For backward compatibility
        return pd.concat([prices, performance], axis=1).dropna(
            how="any", subset=["performance"]
        )  # For backward compatibility

    @classmethod
    def extract_monthly_performance_df(cls, prices: pd.Series) -> pd.DataFrame:
        if prices.empty:
            raise ValueError("Price series cannot be empty")
        performance = FinancialStatistics(prices).extract_monthly_performance_df()  # For backward compatibility
        df = pd.concat([performance], axis=1, keys=["performance"])
        df["year"] = df.index.year
        df["month"] = df.index.month
        return df.dropna(how="any", subset=["performance"]).reset_index(drop=True)  # For backward compatibility

    @classmethod
    def extract_annual_performance_df(cls, prices: pd.Series) -> pd.DataFrame:
        if prices.empty:
            raise ValueError("Price series cannot be empty")
        performance = FinancialStatistics(prices).extract_annual_performance_df()  # For backward compatibility
        df = pd.concat([performance], axis=1, keys=["performance"])
        df["year"] = df.index.year
        return df.dropna(how="any", subset=["performance"]).reset_index(drop=True)  # For backward compatibility

    @classmethod
    def extract_inception_performance_df(cls, prices: pd.Series) -> float:
        if prices.empty:
            raise ValueError("Price series cannot be empty")
        return FinancialStatistics(prices).extract_inception_performance_df()  # For backward compatibility

    @classmethod
    def extract_daily_performance_df(cls, prices: pd.Series) -> pd.DataFrame:
        if prices.empty:
            raise ValueError("Price series cannot be empty")
        performance = FinancialStatistics(prices).extract_daily_performance_df()
        df = pd.concat([performance], axis=1, keys=["performance"])
        df["year"] = df.index.year
        return df.dropna(how="any", subset=["performance"])  # For backward compatibility

    def get_monthly_return_summary(
        self, start: Optional[date] = None, end: Optional[date] = None, **kwargs
    ) -> pd.DataFrame:
        if not (prices := self.get_prices_df_with_calculated(from_date=start, to_date=end, **kwargs)).empty:
            calculated_mask = prices[["calculated"]].copy().asfreq("BME", method="ffill")
            calculated_mask["year"] = calculated_mask.index.year
            calculated_mask["month"] = calculated_mask.index.month
            calculated_mask = (
                calculated_mask[["year", "month", "calculated"]]
                .reset_index(drop=True)
                .groupby(["year", "month"])
                .any()
            )
            monthly_perfs = self.extract_monthly_performance_df(prices.close)
            annual_perfs = self.extract_annual_performance_df(prices.close)
            annual_perfs["month"] = "annual"
            perfs = pd.concat([monthly_perfs, annual_perfs], axis=0, ignore_index=True)

            return perfs.replace([np.inf, -np.inf, np.nan], None), calculated_mask
        return pd.DataFrame(), pd.DataFrame()

    def get_monthly_return_summary_dict(
        self, start: Optional[date] = None, end: Optional[date] = None, **kwargs
    ) -> Dict:
        perfs, calculated_mask = self.get_monthly_return_summary(start, end, **kwargs)
        res = defaultdict(dict)
        if not perfs.empty:
            for year, df in perfs.sort_values(by="year", ascending=False).groupby("year", sort=False):
                df = df.set_index("month")
                for i in range(1, 13):
                    try:
                        perf = float(df.loc[i, "performance"])
                    except (IndexError, KeyError):
                        perf = None
                    try:
                        calculated = bool(calculated_mask.loc[(year, i), "calculated"])
                    except (IndexError, KeyError):
                        calculated = False
                    res[year][calendar.month_abbr[i]] = {"performance": perf, "calculated": calculated}
                try:
                    res[year]["annual"] = {
                        "performance": float(df.loc["annual", "performance"]),
                        "calculated": bool(calculated_mask.loc[(year, slice(None)), "calculated"].any()),
                    }
                except (IndexError, KeyError):
                    res[year]["annual"] = {"performance": None, "calculated": False}

        return dict(res)

    def build_benchmark_df(self, end_date: Optional[date] = None, **kwargs) -> pd.Series:
        df = pd.Series(dtype="float64")
        prices_df = self.get_prices_df(to_date=end_date).rename("net_value")
        if not prices_df.empty and (benchmark := self.primary_benchmark) and self.primary_risk_instrument:
            start_date = prices_df.index[0]
            end_date = prices_df.index[-1]
            kwargs = {"from_date": start_date, "to_date": end_date}
            # Get and prepare Risk free rate dataframe from stainly
            risk_df = self.primary_risk_instrument.get_prices_df(**kwargs).rename("rate")

            benchmark_df = benchmark.get_prices_df(**kwargs).rename("benchmark_net_value")
            # Prepare final dataframe, fill the NAN with backward index
            df = pd.concat([risk_df, benchmark_df, prices_df], axis=1).astype("float64").ffill(axis=0).sort_index()
            df.index = pd.to_datetime(df.index)

        return df

    def save_prices_in_db(self, from_date: date, to_date: date, clear: bool = False):
        df = pd.DataFrame(
            self.__class__.objects.filter(id=self.id).dl.market_data(
                from_date=from_date
                - timedelta(
                    days=90
                ),  # we make sure to at least import the last 80 days to be sure to be able to compute the volume 50d
                to_date=to_date,
                values=[MarketData.CLOSE, MarketData.VOLUME, MarketData.MARKET_CAPITALIZATION],
            )
        )
        if not df.empty:
            df["calculated"] = False
            df = df.set_index("valuation_date").sort_index()

            # # if market cap is not found, maybe we have better chance on the primary exhange
            if not df.market_capitalization.notnull().any() and self.parent and (company := self.parent.get_root()):
                with suppress(KeyError):
                    df["market_capitalization"] = pd.DataFrame(
                        self.__class__.objects.filter(id=company.id).dl.market_data(
                            from_date=from_date,
                            to_date=to_date,
                            values=[MarketData.MARKET_CAPITALIZATION],
                        )
                    ).set_index("valuation_date")["market_capitalization"]

            ts = pd.date_range(df.index.min(), df.index.max(), freq="B")
            # fill forward missing data
            df = df.reindex(ts)
            df[["close", "market_capitalization"]] = df[["close", "market_capitalization"]].ffill()
            df.volume = df.volume.fillna(0)
            df.calculated = df.calculated.astype(bool).fillna(
                True
            )  # we do not ffill calculated but set the to True to mark them as "estimated"/"not real"
            df["volume_50d"] = df["volume"].rolling(50).mean()
            df = df[df.index.date >= from_date]  # we import only from the requested from_date
            df = df.reset_index().dropna(subset=["index", "close"])
            df = df.replace([np.inf, -np.inf, np.nan], None)
            update_objs = []
            create_objs = []
            for row in df.to_dict("records"):
                if (_date := row.get("index")) and (close := row.get("close", None)):
                    # we make sure data does not exist 10 digits (for db constraint)
                    if int(math.log10(close)) + 1 < 10:
                        try:
                            p = InstrumentPrice.objects.get(instrument=self, date=_date)

                            # update only if net value is different with existing instrument price
                            if (
                                round(p.net_value, 2) != round(close, 2)
                                or (p.market_capitalization != row.get("market_capitalization"))
                                or (p.volume != row.get("volume"))
                                or (p.calculated != row.get("calculated"))
                                or clear
                            ):
                                p.net_value = close
                                p.gross_value = close
                                p.calculated = row["calculated"]
                                p.volume = row.get("volume", p.volume)
                                p.volume_50d = row.get("volume_50d", p.volume_50d)
                                p.market_capitalization = row.get("market_capitalization", p.market_capitalization)
                                p.market_capitalization_consolidated = p.market_capitalization
                                p.set_dynamic_field(False)
                                update_objs.append(p)
                        except InstrumentPrice.DoesNotExist:
                            with suppress(CurrencyFXRates.DoesNotExist):
                                p = InstrumentPrice(
                                    currency_fx_rate_to_usd=CurrencyFXRates.objects.get(  # we need to get the currency rate because we bulk create the object, and thus save is not called
                                        date=_date, currency=self.currency
                                    ),
                                    instrument=self,
                                    date=_date,
                                    calculated=row["calculated"],
                                    net_value=close,
                                    gross_value=close,
                                    volume=row.get("volume", None),
                                    market_capitalization=row.get("market_capitalization", None),
                                    volume_50d=row.get("volume_50d", None),
                                )
                                p.set_dynamic_field(False)
                                create_objs.append(p)
            InstrumentPrice.objects.bulk_update(
                update_objs,
                fields=[
                    "net_value",
                    "gross_value",
                    "volume",
                    "market_capitalization",
                    "market_capitalization_consolidated",
                    "calculated",
                    "volume_50d",
                ],
            )
            InstrumentPrice.objects.bulk_create(create_objs, ignore_conflicts=True)
