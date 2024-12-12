from wbcore import filters
from wbcore.filters.defaults import five_year_data_range
from wbfdm.enums import CalendarType, DataType, Indicator, MarketDataChartType
from wbfdm.models.instruments import Instrument


class MarketDataChartFilterSet(filters.FilterSet):
    period = filters.FinancialPerformanceDateRangeFilter(
        label="Period",
        method="fake_filter",
        default=five_year_data_range,
    )
    chart_type = filters.ChoiceFilter(
        method="fake_filter",
        label="Chart Type",
        choices=MarketDataChartType.choices,
        default="close",
    )
    benchmarks = filters.ModelMultipleChoiceFilter(
        label="Benchmarks",
        queryset=Instrument.objects.all(),
        endpoint=Instrument.get_representation_endpoint(),
        value_key=Instrument.get_representation_value_key(),
        label_key=Instrument.get_representation_label_key(),
        filter_params={"is_security": True},
        method="fake_filter",
    )
    indicators = filters.MultipleChoiceFilter(
        method="fake_filter",
        label="Indicators",
        choices=Indicator.choices,
        required=False,
    )
    volume = filters.BooleanFilter(
        method="fake_filter",
        label="Add Volume",
        default=False,
        required=False,
    )
    show_estimates = filters.BooleanFilter(
        method="fake_filter",
        label="Show Estimates",
        default=True,
        required=False,
    )

    class Meta:
        model = Instrument
        fields = {}


class FinancialRatioFilterSet(filters.FilterSet):
    ttm = filters.BooleanFilter(
        method="fake_filter",
        label="TTM/FTM",
        default=True,
    )

    period = filters.FinancialPerformanceDateRangeFilter(
        method="fake_filter",
        label="Period",
        default=five_year_data_range,
    )

    class Meta:
        model = Instrument
        fields = {}


class StatementFilter(filters.FilterSet):
    data_type = filters.ChoiceFilter(
        method="fake_filter",
        label="Data Type",
        choices=DataType.choices,
        required=True,
        default=DataType.STANDARDIZED,
    )

    class Meta:
        model = Instrument
        fields = {}


class StatementWithEstimateFilter(filters.FilterSet):
    calendar_type = filters.ChoiceFilter(
        method="fake_filter",
        label="Calendar Type",
        choices=CalendarType.choices,
        required=True,
        default=CalendarType.FISCAL,
    )

    class Meta:
        model = Instrument
        fields = {}
