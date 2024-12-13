from datetime import datetime
from decimal import Decimal

import pytest

from neuro_notifications_client import (
    Client,
    JobCannotStartLackResources,
    JobCannotStartQuotaReached,
    JobTransition,
    QuotaWillBeReachedSoon,
)
from neuro_notifications_client.notifications import (
    AlertManagerNotification,
    JobNotification,
    QuotaResourceType,
    Welcome,
    Invite, OrgCreditsWillRunOutSoon, OrgBalanceTopUp,
)

# TODO: make this tests more meaningful:
# at the moment they just test that no exception was raised


@pytest.mark.parametrize(
    "notification",
    [
        JobTransition(
            "job-new-transition",
            status="PENDING",
            transition_time=datetime(year=2019, month=6, day=7),
        ),
        JobTransition(
            "job-started",
            status="RUNNING",
            transition_time=datetime(year=2019, month=6, day=8),
            prev_status="PENDING",
            prev_transition_time=datetime(year=2019, month=6, day=7),
        ),
        JobTransition(
            "job-failed-exit",
            status="FAILED",
            transition_time=datetime(year=2019, month=6, day=9),
            prev_status="RUNNING",
            prev_transition_time=datetime(year=2019, month=6, day=8),
            reason="Exited with code -10",
            exit_code=-10,
        ),
        JobTransition(
            "job-failed-image",
            status="FAILED",
            transition_time=datetime(year=2019, month=6, day=10),
            prev_status="PENDING",
            prev_transition_time=datetime(year=2019, month=6, day=9),
            reason="ImagePullBackOff",
            description="Cannot pull image some:tag",
        ),
        JobTransition(
            "job-finished",
            status="SUCCEEDED",
            transition_time=datetime(year=2019, month=6, day=11),
            prev_status="RUNNING",
            prev_transition_time=datetime(year=2019, month=6, day=10),
            exit_code=0,
        ),
    ],
)
async def test_job_transition_notifications(
    client: Client,
    notification: JobNotification,
) -> None:
    # Should not raise anything
    await client.notify(notification)
    await client.close()


@pytest.mark.parametrize(
    "notification", [JobCannotStartLackResources("job-lack-resources")]
)
async def test_job_notifications(
    client: Client,
    notification: JobNotification,
) -> None:
    # Should not raise anything
    await client.notify(notification)
    await client.close()


@pytest.mark.parametrize(
    "notification",
    [
        JobCannotStartQuotaReached(
            user_id="job-quota-reached",
            resource=QuotaResourceType.NON_GPU,
            quota=2.1,
            cluster_name="test",
        )
    ],
)
async def test_user_notifications(
    client: Client,
    notification: JobNotification,
) -> None:
    # Should not raise anything
    await client.notify(notification)
    await client.close()


@pytest.mark.parametrize(
    "notification",
    [
        QuotaWillBeReachedSoon(
            "job-quota-reached",
            resource=QuotaResourceType.NON_GPU,
            used=1,
            quota=2,
            cluster_name="default",
        ),
        QuotaWillBeReachedSoon(
            "job-quota-reached",
            resource=QuotaResourceType.GPU,
            used=2,
            quota=3,
            cluster_name="default",
        ),
    ],
)
async def test_quota_will_be_reached_soon_notifications(
    client: Client,
    notification: QuotaWillBeReachedSoon,
) -> None:
    # Should not raise anything
    await client.notify(notification)
    await client.close()


async def test_welcome_notification(client: Client) -> None:
    # Should not raise anything
    await client.notify(Welcome(user_id="bob", email="bob@neu.ro"))
    await client.close()


async def test_invite_notification(client: Client) -> None:
    # Should not raise anything
    await client.notify(
        Invite(org_name="test", email="bob@neu.ro", console_url="test-url")
    )
    await client.close()


async def test_alert_manager_notification(client: Client) -> None:
    # Should not raise anything
    await client.notify(
        AlertManagerNotification(
            version="4",
            group_key='{}:{alertname="TraefikDown"}',
            status=AlertManagerNotification.Status.FIRING,
            group_labels={"alertname": "TraefikDown"},
            common_labels={
                "alertname": "TraefikDown",
                "cluster": "default",
                "context": "traefik",
                "severity": "critical",
            },
            common_annotations={"summary": "Traefik Down"},
            alerts=[
                AlertManagerNotification.Alert(
                    status=AlertManagerNotification.Status.FIRING,
                    labels={
                        "alertname": "TraefikDown",
                        "cluster": "default",
                        "severity": "critical",
                    },
                    annotations={"summary": "Traefik Down"},
                ),
            ],
        )
    )
    await client.close()


@pytest.mark.parametrize(
    "notification",
    [
        OrgCreditsWillRunOutSoon(
            org_name="org",
            credits=Decimal("-111.11"),
        ),
        OrgCreditsWillRunOutSoon(
            org_name="org",
            credits=Decimal("0"),
        ),
        OrgCreditsWillRunOutSoon(
            org_name="org",
            credits=Decimal("222.22"),
        ),
    ],
)
async def test_org_credits_will_run_out_soon_notifications(
    client: Client,
    notification: OrgCreditsWillRunOutSoon,
) -> None:
    # Should not raise anything
    await client.notify(notification)
    await client.close()


@pytest.mark.parametrize(
    "notification", [OrgBalanceTopUp(org_name="org")],
)
async def test_org_balance_top_up_notifications(
    client: Client,
    notification: OrgBalanceTopUp,
) -> None:
    # Should not raise anything
    await client.notify(notification)
    await client.close()


async def test_unknown_notifications(
    client: Client,
    unknown_notification: JobNotification,
) -> None:
    with pytest.raises(ValueError):
        await client.notify(unknown_notification)
        await client.close()
