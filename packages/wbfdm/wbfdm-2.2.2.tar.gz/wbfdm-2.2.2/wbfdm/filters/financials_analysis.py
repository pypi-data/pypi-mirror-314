from datetime import date

from django.db import models
from pandas.tseries.offsets import BYearEnd
from psycopg.types.range import DateRange
from wbcore import filters as wb_filters
from wbfdm.figures.financials.financial_analysis_charts import (
    PeriodChoices,
    VariableChoices,
)
from wbfdm.models.instruments.instruments import Instrument


def byearend_n_year_ago(n):
    today = date.today()
    return (today - BYearEnd(n)).date()


def byearend_2_year_ago(field, request, view):
    return byearend_n_year_ago(2)


class GroupKeyFinancialsFilterSet(wb_filters.FilterSet):
    group_keys = wb_filters.CharFilter(
        required=True,
        method=lambda q, n, v: q,
    )

    class Meta:
        models = Instrument
        fields = {}


class FinancialAnalysisFilterSet(wb_filters.FilterSet):
    class Meta:
        model = Instrument
        fields = {}


def _get_12m(field, request, view):
    return date(date.today().year - 1, 1, 1)


class FinancialAnalysisValuationRatiosFilterSet(wb_filters.FilterSet):
    date = wb_filters.FinancialPerformanceDateRangeFilter(
        method=lambda queryset, label, value: queryset,
        label="Date Range",
        required=True,
        clearable=False,
        default=lambda r, v, q: DateRange(_get_12m(r, v, q), date.today()),
    )

    class OutputChoices(models.TextChoices):
        TSTABLE = "TSTABLE", "Table (Time-series)"
        TABLE = "TABLE", "Table (Last Value)"
        CHART = "CHART", "Chart"

    class RangeChoices(models.TextChoices):
        MINMAX = "MINMAX", "Min-Max (entire period)"
        ROLLING = "ROLLING", "Rolling"

    output = wb_filters.ChoiceFilter(
        choices=OutputChoices.choices, label="Output", method="fake_filter", default=OutputChoices.CHART
    )
    period = wb_filters.ChoiceFilter(
        choices=PeriodChoices.choices, label="Period", method="fake_filter", default=PeriodChoices.NTM
    )
    vs_related = wb_filters.BooleanFilter(label="Versus related", default=False, method="fake_filter")
    clean_data = wb_filters.BooleanFilter(label="Clean data", default=True, method="fake_filter")
    ranges = wb_filters.BooleanFilter(label="Draw ranges", default=False, required=False, method="fake_filter")
    range_type = wb_filters.ChoiceFilter(
        choices=RangeChoices.choices,
        label="Range type",
        method="fake_filter",
        required=True,
        default=RangeChoices.MINMAX,
    )
    range_period = wb_filters.NumberFilter(
        precision=0, label="Rolling period", method="fake_filter", required=True, default=120
    )
    x_axis_var = wb_filters.ChoiceFilter(
        choices=VariableChoices.choices, label="X-Axis", method="fake_filter", default=VariableChoices.EPSG
    )
    y_axis_var = wb_filters.ChoiceFilter(
        choices=VariableChoices.choices, label="Y-Axis", method="fake_filter", default=VariableChoices.PE
    )
    z_axis_var = wb_filters.ChoiceFilter(
        choices=VariableChoices.choices, label="Bubble", method="fake_filter", default=VariableChoices.MKTCAP
    )
    median = wb_filters.BooleanFilter(label="Median", default=True, method="fake_filter")

    class Meta:
        model = Instrument
        fields = {}


class EarningsAnalysisFilterSet(wb_filters.FilterSet):
    date = wb_filters.FinancialPerformanceDateRangeFilter(
        method=lambda queryset, label, value: queryset,
        label="Date Range",
        required=True,
        clearable=False,
        default=lambda r, v, q: DateRange(_get_12m(r, v, q), date.today()),
    )

    class OutputChoices(models.TextChoices):
        EPS = "EPS", "Earnings ($)"

    analysis = wb_filters.ChoiceFilter(
        choices=OutputChoices.choices, label="Analysis", method=lambda q, n, v: q, default=OutputChoices.EPS
    )
    period = wb_filters.ChoiceFilter(
        choices=PeriodChoices.choices, label="Period", method=lambda q, n, v: q, default=PeriodChoices.NTM
    )
    vs_related = wb_filters.BooleanFilter(label="Show related", default=False, method=lambda q, n, v: q)

    class Meta:
        model = Instrument
        fields = {}
