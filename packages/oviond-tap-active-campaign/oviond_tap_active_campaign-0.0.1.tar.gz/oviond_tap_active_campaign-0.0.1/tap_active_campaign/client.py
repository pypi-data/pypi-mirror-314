"""REST client handling, including ActiveCampaignStream base class."""

from __future__ import annotations

import decimal
import typing as t
from importlib import resources
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator  # noqa: TC002
from singer_sdk.streams import RESTStream

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context


class ActiveCampaignStream(RESTStream):
    """ActiveCampaign stream class."""

    next_page_token_jsonpath = None

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        # TODO: hardcode a value here, or retrieve it from self.config

        api_url = self.config["api_url"]

        return "https://{api_url}/api/3"

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="Api-Token",
            value=self.config["auth_token"],
            location="header",
        )

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
        params = { "limit": 100, "offset": 0 }

        if next_page_token:
            params["offset"] = next_page_token

        return params

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        api_key = self.config["auth_token"]

        yield from (
            {
                **record,
                "profile_id": api_key,
            }
            for record in extract_jsonpath(self.records_jsonpath, input=response.json())
        )
