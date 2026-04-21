from dataclasses import dataclass

from django.core.cache import cache

from .models import ServiceProbe
from .tasks import ping


STARTER_PROBE_SLUG = "starter-demo"
STARTER_CACHE_KEY = "starter:service-status"


@dataclass(frozen=True)
class StarterSnapshot:
    probe_id: int
    probe_created: bool
    probe_count: int
    cache_key: str
    cache_value: str
    redis_ok: bool


def get_starter_snapshot() -> StarterSnapshot:
    probe, created = ServiceProbe.objects.get_or_create(
        slug=STARTER_PROBE_SLUG,
        defaults={"label": "Starter service probe"},
    )
    cache_value = f"probe:{probe.pk}"
    cache.set(STARTER_CACHE_KEY, cache_value, timeout=60)
    redis_value = cache.get(STARTER_CACHE_KEY)

    return StarterSnapshot(
        probe_id=probe.pk,
        probe_created=created,
        probe_count=ServiceProbe.objects.count(),
        cache_key=STARTER_CACHE_KEY,
        cache_value=redis_value or "",
        redis_ok=redis_value == cache_value,
    )


def run_celery_probe(timeout: int = 15) -> str:
    async_result = ping.delay()
    return async_result.get(timeout=timeout)
