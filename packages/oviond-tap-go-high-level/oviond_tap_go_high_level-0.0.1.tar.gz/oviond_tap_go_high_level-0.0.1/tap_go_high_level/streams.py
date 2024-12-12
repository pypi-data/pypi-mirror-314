"""Stream type classes for tap-go-high-level."""

from __future__ import annotations

import typing as t
from importlib import resources
from singer_sdk import typing as th
from tap_go_high_level.client import GoHighLevelStream


class OpportunitiesStream(GoHighLevelStream):
    """Define custom stream."""

    name = "go_high_level_opportunities"
    path = "/opportunities/search/"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.opportunities[*]"
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("monetaryValue", th.IntegerType),
        th.Property("pipelineId", th.StringType),
        th.Property("pipelineStageId", th.StringType),
        th.Property("assignedTo", th.StringType),
        th.Property("status", th.StringType),
        th.Property("source", th.StringType),
        th.Property("lastStatusChangeAt", th.DateTimeType),
        th.Property("lastStageChangeAt", th.DateTimeType),
        th.Property("lastActionDate", th.DateTimeType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("indexVersion", th.IntegerType),
        th.Property("contactId", th.StringType),
        th.Property("locationId", th.StringType),
        th.Property("contact", th.ObjectType(additional_properties=True)),
        th.Property("notes", th.ArrayType(th.StringType)),
        th.Property("tasks", th.ArrayType(th.StringType)),
        th.Property("calendarEvents", th.ArrayType(th.StringType)),
        th.Property(
            "customFields", th.ArrayType(th.ObjectType(additional_properties=True))
        ),
        th.Property("profile_id", th.StringType),
    ).to_dict()


class ContactsStream(GoHighLevelStream):
    """Define custom stream."""

    name = "go_high_level_contacts"
    path = "/contacts/"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.contacts[*]"
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("locationId", th.StringType),
        th.Property("email", th.StringType),
        th.Property("timezone", th.StringType),
        th.Property("country", th.StringType),
        th.Property("source", th.StringType),
        th.Property("dateAdded", th.DateTimeType),
        th.Property("businessId", th.StringType),
        th.Property("followers", th.ArrayType(th.StringType)),
        th.Property("customFields", th.ArrayType(th.ObjectType(additional_properties=True))),
        th.Property("tags", th.ArrayType(th.StringType)),
        th.Property("attributions", th.ArrayType(th.ObjectType(additional_properties=True))),
        th.Property("profile_id", th.StringType),
    ).to_dict()
