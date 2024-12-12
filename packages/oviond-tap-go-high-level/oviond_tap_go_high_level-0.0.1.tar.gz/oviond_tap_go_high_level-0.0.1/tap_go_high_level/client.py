"""REST client handling, including GoHighLevelStream base class."""

from __future__ import annotations

import decimal
import typing as t
from importlib import resources

from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator  # noqa: TC002
from singer_sdk.streams import RESTStream

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context


class GoHighLevelStream(RESTStream):
    """GoHighLevel stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return "https://services.leadconnectorhq.com"

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=self.config.get("auth_token", ""),
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        return {
            "Accept": "application/json",
            "Version": "2021-07-28",
        }

    def get_url_params(
        self,
        context: Context | None,  # noqa: ARG002
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """

        location_id = self.config["location_id"]
        params = {}

        if self.name == "go_high_level_contacts":
            params["locationId"] = location_id
        else:
            params["location_id"] = location_id

        return params

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """

        location_id = self.config["location_id"]

        for record in extract_jsonpath(self.records_jsonpath, input=response.json()):
            yield {**record, "profile_id": location_id}
