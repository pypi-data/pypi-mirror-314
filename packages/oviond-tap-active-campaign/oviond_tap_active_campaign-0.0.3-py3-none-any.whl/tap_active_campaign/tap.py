"""ActiveCampaign tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_active_campaign import streams


class TapActiveCampaign(Tap):
    """ActiveCampaign tap class."""

    name = "tap-active-campaign"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType,
            required=True,
            secret=True,
            title="Auth Token",
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "api_url",
            th.StringType,
            required=True,
            title="API URL",
            description="The api url to authenticate against the API service",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.ActiveCampaignStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.CampaignsStream(self),
            streams.AutomationsStream(self),
            streams.DealsStream(self),
            streams.ContactsStream(self),
            streams.TagsStream(self),
            streams.CustomersStream(self),
        ]


if __name__ == "__main__":
    TapActiveCampaign.cli()
