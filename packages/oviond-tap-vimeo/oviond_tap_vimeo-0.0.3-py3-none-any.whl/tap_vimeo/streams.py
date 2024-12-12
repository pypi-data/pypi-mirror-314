"""Stream type classes for tap-vimeo."""

from __future__ import annotations

import typing as t
from importlib import resources
from singer_sdk import typing as th
from tap_vimeo.client import VimeoStream


class VideosStream(VimeoStream):
    """Define custom stream."""

    name = "vimeo_videos"
    path = "/videos"
    primary_keys = ["uri"]
    replication_key = None
    records_jsonpath = "$.data[*]"
    schema = th.PropertiesList(
        th.Property("uri", th.StringType),
        th.Property("account", th.StringType),
        th.Property("name", th.StringType),
        th.Property("description", th.StringType),
        th.Property("created_time", th.DateTimeType),
        th.Property("link", th.StringType),
        th.Property("height", th.IntegerType),
        th.Property("width", th.IntegerType),
        th.Property("metadata", th.ObjectType(additional_properties=True)),
        th.Property("stats", th.ObjectType(additional_properties=True)),
        th.Property("profile_id", th.StringType),
    ).to_dict()


class FollowersStream(VimeoStream):
    """Define custom stream."""

    name = "vimeo_followers"
    path = "/followers"
    primary_keys = ["uri"]
    replication_key = None
    records_jsonpath = "$.data[*]"
    schema = th.PropertiesList(
        th.Property("account", th.StringType),
        th.Property("available_for_hire", th.BooleanType),
        th.Property("bandwidth", th.ObjectType(additional_properties=True)),
        th.Property("bio", th.StringType),
        th.Property("can_work_remotely", th.BooleanType),
        th.Property("capabilities", th.ArrayType(th.StringType)),
        th.Property("clients", th.StringType),
        th.Property("content_filter", th.ArrayType(th.StringType)),
        th.Property("created_time", th.DateTimeType),
        th.Property("gender", th.StringType),
        th.Property("has_invalid_email", th.BooleanType),
        th.Property("is_expert", th.BooleanType),
        th.Property("is_staff_picked", th.BooleanType),
        th.Property("link", th.StringType),
        th.Property("location", th.StringType),
        th.Property(
            "location_details", th.ArrayType(th.ObjectType(additional_properties=True))
        ),
        th.Property("metadata", th.ObjectType(additional_properties=True)),
        th.Property("name", th.StringType),
        th.Property("profile_discovery", th.BooleanType),
        th.Property("resource_key", th.StringType),
        th.Property("short_bio", th.StringType),
        th.Property("skills", th.ObjectType(additional_properties=True)),
        th.Property("uri", th.StringType),
        th.Property("websites", th.ObjectType(additional_properties=True)),
        th.Property("profile_id", th.StringType),
    ).to_dict()
