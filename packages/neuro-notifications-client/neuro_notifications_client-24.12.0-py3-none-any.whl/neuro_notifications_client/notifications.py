from __future__ import annotations

import abc
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional


class Notification(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def slug(cls) -> str:
        pass


@dataclass
class Welcome(Notification):
    user_id: str
    email: str

    @classmethod
    def slug(cls) -> str:
        return "welcome"


@dataclass
class Invite(Notification):
    org_name: str
    email: str
    console_url: str

    @classmethod
    def slug(cls) -> str:
        return "invite"


@dataclass
class JobNotification(Notification, abc.ABC):
    job_id: str


@dataclass
class JobCannotStartLackResources(JobNotification):
    @classmethod
    def slug(cls) -> str:
        return "job-cannot-start-lack-resources"


@dataclass
class JobTransition(JobNotification):
    job_id: str
    status: str
    transition_time: datetime
    reason: Optional[str] = None
    description: Optional[str] = None
    exit_code: Optional[int] = None
    prev_status: Optional[str] = None
    prev_transition_time: Optional[datetime] = None

    @classmethod
    def slug(cls) -> str:
        return "job-transition"


class QuotaResourceType(str, Enum):
    NON_GPU = "non_gpu"
    GPU = "gpu"


@dataclass
class JobCannotStartQuotaReached(Notification):
    user_id: str
    resource: QuotaResourceType
    quota: float
    cluster_name: str

    @classmethod
    def slug(cls) -> str:
        return "job-cannot-start-quota-reached"


@dataclass
class QuotaWillBeReachedSoon(Notification):
    user_id: str
    resource: QuotaResourceType
    used: float
    quota: float
    cluster_name: str

    @classmethod
    def slug(cls) -> str:
        return "quota-will-be-reached-soon"


@dataclass
class JobCannotStartNoCredits(Notification):
    user_id: str
    cluster_name: Optional[str] = None

    @classmethod
    def slug(cls) -> str:
        return "job-cannot-start-no-credits"


@dataclass
class CreditsWillRunOutSoon(Notification):
    user_id: str
    cluster_name: str
    credits: Decimal

    @classmethod
    def slug(cls) -> str:
        return "credits-will-run-out-soon"


@dataclass
class OrgCreditsWillRunOutSoon(Notification):
    org_name: str
    credits: Decimal

    @classmethod
    def slug(cls) -> str:
        return "org-credits-will-run-out-soon"


@dataclass
class OrgBalanceTopUp(Notification):
    org_name: str

    @classmethod
    def slug(cls) -> str:
        return "org-balance-top-up"


@dataclass
class AlertManagerNotification(Notification):
    class Status(str, Enum):
        RESOLVED = "resolved"
        FIRING = "firing"

    @dataclass
    class Alert:
        status: AlertManagerNotification.Status
        labels: dict[str, str]
        annotations: dict[str, str]

    version: str
    group_key: str
    status: Status
    group_labels: dict[str, str]
    common_labels: dict[str, str]
    common_annotations: dict[str, str]
    alerts: list[Alert]

    @classmethod
    def slug(cls) -> str:
        return "alert-manager-notification"
