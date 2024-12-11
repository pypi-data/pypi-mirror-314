"""Stream type classes for tap-active-campaign."""

from __future__ import annotations

import typing as t
from importlib import resources
from singer_sdk import typing as th
from tap_active_campaign.client import ActiveCampaignStream


class CampaignsStream(ActiveCampaignStream):
    """Define custom stream."""

    name = "active_campaign_campaigns"
    path = "/campaigns"
    primary_keys = ["id"]
    records_jsonpath = "$.campaigns[*]"
    replication_key = None
    schema = th.PropertiesList(
        th.Property("type", th.StringType),
        th.Property("userid", th.StringType),
        th.Property("segmentid", th.StringType),
        th.Property("bounceid", th.StringType),
        th.Property("realcid", th.StringType),
        th.Property("sendid", th.StringType),
        th.Property("threadid", th.StringType),
        th.Property("seriesid", th.StringType),
        th.Property("formid", th.StringType),
        th.Property("basetemplateid", th.StringType),
        th.Property("basemessageid", th.StringType),
        th.Property("addressid", th.StringType),
        th.Property("source", th.StringType),
        th.Property("name", th.StringType),
        th.Property("cdate", th.DateTimeType),
        th.Property("mdate", th.DateTimeType),
        th.Property("sdate", th.DateTimeType),
        th.Property("ldate", th.DateTimeType),
        th.Property("send_amt", th.StringType),
        th.Property("total_amt", th.StringType),
        th.Property("opens", th.StringType),
        th.Property("uniqueopens", th.StringType),
        th.Property("linkclicks", th.StringType),
        th.Property("uniquelinkclicks", th.StringType),
        th.Property("subscriberclicks", th.StringType),
        th.Property("forwards", th.StringType),
        th.Property("uniqueforwards", th.StringType),
        th.Property("hardbounces", th.StringType),
        th.Property("softbounces", th.StringType),
        th.Property("unsubscribes", th.StringType),
        th.Property("unsubreasons", th.StringType),
        th.Property("updates", th.StringType),
        th.Property("socialshares", th.StringType),
        th.Property("replies", th.StringType),
        th.Property("uniquereplies", th.StringType),
        th.Property("status", th.StringType),
        th.Property("public", th.StringType),
        th.Property("mail_transfer", th.StringType),
        th.Property("mail_send", th.StringType),
        th.Property("mail_cleanup", th.StringType),
        th.Property("mailer_log_file", th.StringType),
        th.Property("tracklinks", th.StringType),
        th.Property("tracklinksanalytics", th.StringType),
        th.Property("trackreads", th.StringType),
        th.Property("trackreadsanalytics", th.StringType),
        th.Property("analytics_campaign_name", th.StringType),
        th.Property("tweet", th.StringType),
        th.Property("facebook", th.StringType),
        th.Property("survey", th.StringType),
        th.Property("embed_images", th.StringType),
        th.Property("htmlunsub", th.StringType),
        th.Property("textunsub", th.StringType),
        th.Property("htmlunsubdata", th.StringType),
        th.Property("textunsubdata", th.StringType),
        th.Property("recurring", th.StringType),
        th.Property("willrecur", th.StringType),
        th.Property("split_type", th.StringType),
        th.Property("split_content", th.StringType),
        th.Property("split_offset", th.StringType),
        th.Property("split_offset_type", th.StringType),
        th.Property("split_winner_messageid", th.StringType),
        th.Property("split_winner_awaiting", th.StringType),
        th.Property("responder_offset", th.StringType),
        th.Property("responder_type", th.StringType),
        th.Property("responder_existing", th.StringType),
        th.Property("reminder_field", th.StringType),
        th.Property("reminder_format", th.StringType),
        th.Property("reminder_type", th.StringType),
        th.Property("reminder_offset", th.StringType),
        th.Property("reminder_offset_type", th.StringType),
        th.Property("reminder_offset_sign", th.StringType),
        th.Property("reminder_last_cron_run", th.StringType),
        th.Property("activerss_interval", th.StringType),
        th.Property("activerss_url", th.StringType),
        th.Property("activerss_items", th.StringType),
        th.Property("ip4", th.StringType),
        th.Property("laststep", th.StringType),
        th.Property("managetext", th.StringType),
        th.Property("schedule", th.StringType),
        th.Property("scheduleddate", th.StringType),
        th.Property("waitpreview", th.StringType),
        th.Property("deletestamp", th.StringType),
        th.Property("replysys", th.StringType),
        th.Property("created_timestamp", th.DateTimeType),
        th.Property("updated_timestamp", th.DateTimeType),
        th.Property("created_by", th.StringType),
        th.Property("updated_by", th.StringType),
        th.Property("ip", th.StringType),
        th.Property("series_send_lock_time", th.StringType),
        th.Property("can_skip_approval", th.StringType),
        th.Property("use_quartz_scheduler", th.StringType),
        th.Property("verified_opens", th.StringType),
        th.Property("verified_unique_opens", th.StringType),
        th.Property("segmentname", th.StringType),
        th.Property("has_predictive_content", th.StringType),
        th.Property("message_id", th.StringType),
        th.Property("screenshot", th.StringType),
        th.Property("campaign_message_id", th.StringType),
        th.Property("ed_version", th.StringType),
        th.Property("id", th.StringType),
        th.Property("user", th.StringType),
        th.Property("automation", th.StringType),
        th.Property("profile_id", th.StringType),
    ).to_dict()


class AutomationsStream(ActiveCampaignStream):
    """Define custom stream."""

    name = "active_campaign_automations"
    path = "/automations"
    primary_keys = ["id"]
    records_jsonpath = "$.automations[*]"
    replication_key = None
    schema = th.PropertiesList(
        th.Property("name", th.StringType),
        th.Property("cdate", th.DateTimeType),
        th.Property("mdate", th.DateTimeType),
        th.Property("userid", th.StringType),
        th.Property("status", th.StringType),
        th.Property("entered", th.StringType),
        th.Property("exited", th.StringType),
        th.Property("hidden", th.StringType),
        th.Property("defaultscreenshot", th.StringType),
        th.Property("screenshot", th.StringType),
        th.Property("id", th.StringType),
        th.Property("opens", th.IntegerType),
        th.Property("uniqueopens", th.IntegerType),
        th.Property("linkclicks", th.IntegerType),
        th.Property("uniquelinkclicks", th.IntegerType),
        th.Property("subscriberclicks", th.IntegerType),
        th.Property("forwards", th.IntegerType),
        th.Property("uniqueforwards", th.IntegerType),
        th.Property("hardbounces", th.IntegerType),
        th.Property("softbounces", th.IntegerType),
        th.Property("unsubscribes", th.IntegerType),
        th.Property("unsubreasons", th.IntegerType),
        th.Property("updates", th.IntegerType),
        th.Property("socialshares", th.IntegerType),
        th.Property("replies", th.IntegerType),
        th.Property("uniquereplies", th.IntegerType),
        th.Property("send_amt", th.IntegerType),
        th.Property("profile_id", th.StringType),
    ).to_dict()


class DealsStream(ActiveCampaignStream):
    """Define custom stream."""

    name = "active_campaign_deals"
    path = "/deals"
    primary_keys = ["id"]
    records_jsonpath = "$.deals[*]"
    replication_key = None
    schema = th.PropertiesList(
        th.Property("owner", th.StringType),
        th.Property("contact", th.StringType),
        th.Property("organization", th.StringType),
        th.Property("group", th.StringType),
        th.Property("stage", th.StringType),
        th.Property("title", th.StringType),
        th.Property("description", th.StringType),
        th.Property("percent", th.StringType),
        th.Property("cdate", th.DateTimeType),
        th.Property("mdate", th.DateTimeType),
        th.Property("nextdate", th.DateTimeType),
        th.Property("nexttaskid", th.StringType),
        th.Property("value", th.StringType),
        th.Property("currency", th.StringType),
        th.Property("winProbability", th.IntegerType),
        th.Property("winProbabilityMdate", th.DateTimeType),
        th.Property("status", th.StringType),
        th.Property("activitycount", th.StringType),
        th.Property("nextdealid", th.StringType),
        th.Property("edate", th.StringType),
        th.Property("id", th.StringType),
        th.Property("isDisabled", th.BooleanType),
        th.Property("account", th.StringType),
        th.Property("customerAccount", th.StringType),
        th.Property("hash", th.StringType),
        th.Property("nextTask", th.StringType),
        th.Property("profile_id", th.StringType),
    ).to_dict()


class ContactsStream(ActiveCampaignStream):
    """Define custom stream."""

    name = "active_campaign_contacts"
    path = "/contacts"
    primary_keys = ["id"]
    records_jsonpath = "$.contacts[*]"
    replication_key = None
    schema = th.PropertiesList(
        th.Property("cdate", th.DateTimeType),
        th.Property("email", th.StringType),
        th.Property("phone", th.StringType),
        th.Property("firstName", th.StringType),
        th.Property("lastName", th.StringType),
        th.Property("orgid", th.StringType),
        th.Property("segmentio_id", th.StringType),
        th.Property("bounced_hard", th.StringType),
        th.Property("bounced_soft", th.StringType),
        th.Property("bounced_date", th.StringType),
        th.Property("ip", th.StringType),
        th.Property("ua", th.StringType),
        th.Property("hash", th.StringType),
        th.Property("socialdata_lastcheck", th.StringType),
        th.Property("email_local", th.StringType),
        th.Property("email_domain", th.StringType),
        th.Property("sentcnt", th.StringType),
        th.Property("rating_tstamp", th.StringType),
        th.Property("gravatar", th.StringType),
        th.Property("deleted", th.StringType),
        th.Property("adate", th.DateTimeType),
        th.Property("udate", th.DateTimeType),
        th.Property("edate", th.StringType),
        th.Property("scoreValues", th.ArrayType(th.StringType)),
        th.Property("accountContacts", th.ArrayType(th.StringType)),
        th.Property("id", th.StringType),
        th.Property("organization", th.StringType),
        th.Property("profile_id", th.StringType),
    ).to_dict()


class TagsStream(ActiveCampaignStream):
    """Define custom stream."""

    name = "active_campaign_tags"
    path = "/tags"
    primary_keys = ["id"]
    records_jsonpath = "$.tags[*]"
    replication_key = None
    schema = th.PropertiesList(
        th.Property("tagType", th.StringType),
        th.Property("tag", th.StringType),
        th.Property("description", th.StringType),
        th.Property("cdate", th.DateTimeType),
        th.Property("id", th.StringType),
        th.Property("subscriber_count", th.StringType),
        th.Property("profile_id", th.StringType),
    ).to_dict()


class CustomersStream(ActiveCampaignStream):
    """Define custom stream."""

    name = "active_campaign_customers"
    path = "/ecomCustomers"
    primary_keys = ["id"]
    records_jsonpath = "$.ecomCustomers[*]"
    replication_key = None
    schema = th.PropertiesList(
        th.Property("connectionid", th.StringType),
        th.Property("externalid", th.StringType),
        th.Property("email", th.StringType),
        th.Property("totalRevenue", th.StringType),
        th.Property("totalOrders", th.StringType),
        th.Property("totalProducts", th.StringType),
        th.Property("avgRevenuePerOrder", th.StringType),
        th.Property("avgProductCategory", th.StringType),
        th.Property("tstamp", th.DateTimeType),
        th.Property("id", th.StringType),
        th.Property("connection", th.StringType),
        th.Property("profile_id", th.StringType),
    ).to_dict()
