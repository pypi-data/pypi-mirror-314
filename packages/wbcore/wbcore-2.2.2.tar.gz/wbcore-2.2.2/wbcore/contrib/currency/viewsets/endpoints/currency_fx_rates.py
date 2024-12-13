from rest_framework.reverse import reverse
from wbcore.metadata.configs.endpoints import EndpointViewConfig


class CurrencyFXRatesCurrencyEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return None

    def get_list_endpoint(self, **kwargs):
        return reverse(
            "wbcore:currency:currency-currencyfxrates-list",
            args=[self.view.kwargs["currency_id"]],
            request=self.request,
        )
