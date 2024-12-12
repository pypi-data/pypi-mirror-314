"""GoHighLevel tap class."""

from __future__ import annotations
from singer_sdk import Tap
from singer_sdk import typing as th
from tap_go_high_level import streams


class TapGoHighLevel(Tap):
    """GoHighLevel tap class."""

    name = "tap-go-high-level"

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
            "location_id",
            th.StringType,
            title="Location ID",
            description="The location to authenticate against the API service",
        ),
        th.Property(
            "company_id",
            th.StringType,
            title="Company ID",
            description="The company to authenticate against the API service",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.GoHighLevelStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.OpportunitiesStream(self),
            streams.ContactsStream(self),
        ]


if __name__ == "__main__":
    TapGoHighLevel.cli()
