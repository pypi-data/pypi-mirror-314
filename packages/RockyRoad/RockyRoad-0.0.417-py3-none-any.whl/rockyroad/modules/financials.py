from uplink import (
    Consumer,
    get as http_get,
    post,
    patch,
    delete,
    returns,
    headers,
    Body,
    json,
    Query,
)


from .module_imports import key


@headers({"Ocp-Apim-Subscription-Key": key})
class _Financials(Consumer):
    """Inteface to Financials resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    def exchange_rates(self):
        """Inteface to Exchange Rates resource for the RockyRoad API."""
        return self._Exchange_Rates(self)

    @headers({"Ocp-Apim-Subscription-Key": key})
    class _Exchange_Rates(Consumer):
        """Inteface to exchange rates resource for the RockyRoad API."""

        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @http_get("financials/exchange-rates")
        def list(
            self,
            date: Query = None

        ):
            """This call will return detailed information for all exchange rates or for those for the specified params."""

        @returns.json
        @http_get("financials/exchange-rates/{uid}")
        def get(self, uid: str):
            """This call will return the specified exchange rate."""

        @delete("financials/exchange-rates/{uid}")
        def delete(self, uid: str):
            """This call will delete the exchange rate for the specified uid."""

        @returns.json
        @json
        @post("financials/exchange-rates")
        def insert(self, exchange_rates: Body):
            """This call will create a exchange rate with the specified parameters."""

        @json
        @patch("financials/exchange-rates/{uid}")
        def update(self, uid: str, exchange_rates: Body):
            """This call will update the exchange rate with the specified parameters."""
