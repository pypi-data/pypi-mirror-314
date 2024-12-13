from rest_framework.reverse import reverse
from wbcore.metadata.configs.endpoints import EndpointViewConfig


class InstrumentPriceInstrumentEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return None

    def get_list_endpoint(self, **kwargs):
        return reverse("wbfdm:instrument-price-list", [self.view.kwargs["instrument_id"]], request=self.request)


class InstrumentPriceStatisticsInstrumentEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return reverse(
            "wbfdm:instrument-pricestatisticchart-list",
            [self.view.kwargs["instrument_id"]],
            request=self.request,
        )


class MonthlyPerformancesInstrumentEndpointConfig(InstrumentPriceInstrumentEndpointConfig):
    def get_list_endpoint(self, **kwargs):
        return reverse("wbfdm:monthly_performances-list", [self.view.kwargs["instrument_id"]], request=self.request)


class FinancialStatisticsInstrumentEndpointConfig(InstrumentPriceInstrumentEndpointConfig):
    def get_list_endpoint(self, **kwargs):
        return reverse(
            "wbfdm:instrument-financialstatistics-list",
            [self.view.kwargs["instrument_id"]],
            request=self.request,
        )


class InstrumentPriceInstrumentDistributionReturnsChartEndpointConfig(EndpointViewConfig):
    def get_list_endpoint(self, **kwargs):
        return reverse(
            "wbfdm:instrument-distributionreturnschart-list",
            args=[self.view.kwargs["instrument_id"]],
            request=self.request,
        )


class BestAndWorstReturnsInstrumentEndpointConfig(EndpointViewConfig):
    def get_list_endpoint(self, **kwargs):
        return reverse(
            "wbfdm:instrument-bestandworstreturns-list",
            [self.view.kwargs["instrument_id"]],
            request=self.request,
        )
