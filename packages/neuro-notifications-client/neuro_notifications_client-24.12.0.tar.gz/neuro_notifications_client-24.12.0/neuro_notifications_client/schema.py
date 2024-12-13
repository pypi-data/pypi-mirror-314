from __future__ import annotations

from datetime import timezone
from enum import Enum
from typing import Any, Optional

from marshmallow import EXCLUDE, Schema, fields, post_load, validate

from .notifications import (
    AlertManagerNotification,
    CreditsWillRunOutSoon,
    OrgCreditsWillRunOutSoon,
    OrgBalanceTopUp,
    JobCannotStartLackResources,
    JobCannotStartNoCredits,
    JobCannotStartQuotaReached,
    JobTransition,
    QuotaResourceType,
    QuotaWillBeReachedSoon,
    Welcome,
    Invite,
)


class StringEnum(fields.String):
    def __init__(self, enum: type[Enum], *args: Any, **kwargs: Any) -> None:
        super().__init__(
            *args, validate=validate.OneOf([item.value for item in enum]), **kwargs
        )
        self.enum = enum

    def _deserialize(self, *args: Any, **kwargs: Any) -> Enum:
        res: str = super()._deserialize(*args, **kwargs)
        return self.enum(res)

    def _serialize(
        self, value: Optional[Enum], *args: Any, **kwargs: Any
    ) -> Optional[str]:
        if value is None:
            return None
        return super()._serialize(value.value, *args, **kwargs)


class JobCannotStartLackResourcesSchema(Schema):
    job_id = fields.String(required=True)

    @post_load
    def make_notification(
        self, data: Any, **kwargs: Any
    ) -> JobCannotStartLackResources:
        return JobCannotStartLackResources(**data)


class JobTransitionSchema(Schema):
    job_id = fields.String(required=True)
    status = fields.String(required=True)
    transition_time = fields.AwareDateTime(required=True, default_timezone=timezone.utc)
    reason = fields.String(required=False, allow_none=True)
    description = fields.String(required=False, allow_none=True)
    exit_code = fields.Integer(required=False, allow_none=True)
    prev_status = fields.String(required=False, allow_none=True)
    prev_transition_time = fields.AwareDateTime(
        required=False, allow_none=True, default_timezone=timezone.utc
    )

    @post_load
    def make_notification(self, data: Any, **kwargs: Any) -> JobTransition:
        return JobTransition(**data)


class JobCannotStartNoCreditsSchema(Schema):
    user_id = fields.String(required=True)
    cluster_name = fields.String(required=True)

    @post_load
    def make_notification(self, data: Any, **kwargs: Any) -> JobCannotStartNoCredits:
        return JobCannotStartNoCredits(**data)


class CreditsWillRunOutSoonSchema(Schema):
    user_id = fields.String(required=True)
    cluster_name = fields.String(required=True)
    credits = fields.Decimal(required=True, as_string=True)

    @post_load
    def make_notification(self, data: Any, **kwargs: Any) -> CreditsWillRunOutSoon:
        return CreditsWillRunOutSoon(**data)


class OrgCreditsWillRunOutSoonSchema(Schema):
    org_name = fields.String(required=True)
    credits = fields.Decimal(required=True, as_string=True)

    @post_load
    def make_notification(self, data: Any, **kwargs: Any) -> OrgCreditsWillRunOutSoon:
        return OrgCreditsWillRunOutSoon(**data)


class OrgBalanceTopUpSchema(Schema):
    org_name = fields.String(required=True)

    @post_load
    def make_notification(self, data: Any, **kwargs: Any) -> OrgBalanceTopUp:
        return OrgBalanceTopUp(**data)


class JobCannotStartQuotaReachedSchema(Schema):
    user_id = fields.String(required=True)
    cluster_name = fields.String(required=True)
    resource = StringEnum(enum=QuotaResourceType, required=True)
    quota = fields.Float(required=True)

    @post_load
    def make_notification(self, data: Any, **kwargs: Any) -> JobCannotStartQuotaReached:
        return JobCannotStartQuotaReached(**data)


class QuotaWillBeReachedSoonSchema(Schema):
    user_id = fields.String(required=True)
    cluster_name = fields.String(required=True)
    resource = StringEnum(enum=QuotaResourceType, required=True)
    used = fields.Float(required=True)
    quota = fields.Float(required=True)

    @post_load
    def make_notification(self, data: Any, **kwargs: Any) -> QuotaWillBeReachedSoon:
        data["resource"] = QuotaResourceType(data["resource"])
        return QuotaWillBeReachedSoon(**data)


class WelcomeSchema(Schema):
    user_id = fields.String(required=True)
    email = fields.Email(required=True)

    @post_load
    def make_notification(self, data: Any, **kwargs: Any) -> Welcome:
        return Welcome(**data)


class InviteSchema(Schema):
    org_name = fields.String(required=True)
    email = fields.Email(required=True)
    console_url = fields.String(required=True)

    @post_load
    def make_notification(self, data: Any, **kwargs: Any) -> Invite:
        return Invite(**data)


class AlertManagerNotificationSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    class AlertSchema(Schema):
        class Meta:
            unknown = EXCLUDE

        status = fields.Enum(
            AlertManagerNotification.Status, by_value=True, required=True
        )
        labels = fields.Dict(keys=fields.String(), values=fields.String())
        annotations = fields.Dict(keys=fields.String(), values=fields.String())

        @post_load
        def make_alert(
            self, data: Any, **kwargs: Any
        ) -> AlertManagerNotification.Alert:
            return AlertManagerNotification.Alert(**data)

    version = fields.String(validate=validate.Equal("4"), required=True)
    group_key = fields.String(data_key="groupKey")
    status = fields.Enum(AlertManagerNotification.Status, by_value=True, required=True)
    group_labels = fields.Dict(
        keys=fields.String(), values=fields.String(), data_key="groupLabels"
    )
    common_labels = fields.Dict(
        keys=fields.String(), values=fields.String(), data_key="commonLabels"
    )
    common_annotations = fields.Dict(
        keys=fields.String(), values=fields.String(), data_key="commonAnnotations"
    )
    alerts = fields.List(fields.Nested(AlertSchema), validate=validate.Length(min=1))

    @post_load
    def make_notification(self, data: Any, **kwargs: Any) -> AlertManagerNotification:
        return AlertManagerNotification(**data)


SLUG_TO_SCHEMA = {
    Invite.slug(): InviteSchema,
    Welcome.slug(): WelcomeSchema,
    JobCannotStartLackResources.slug(): JobCannotStartLackResourcesSchema,
    JobTransition.slug(): JobTransitionSchema,
    JobCannotStartNoCredits.slug(): JobCannotStartNoCreditsSchema,
    CreditsWillRunOutSoon.slug(): CreditsWillRunOutSoonSchema,
    OrgCreditsWillRunOutSoon.slug(): OrgCreditsWillRunOutSoonSchema,
    OrgBalanceTopUp.slug(): OrgBalanceTopUpSchema,
    QuotaWillBeReachedSoon.slug(): QuotaWillBeReachedSoonSchema,
    JobCannotStartQuotaReached.slug(): JobCannotStartQuotaReachedSchema,
    AlertManagerNotification.slug(): AlertManagerNotificationSchema,
}
