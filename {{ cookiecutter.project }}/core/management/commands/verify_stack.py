from celery.exceptions import TimeoutError as CeleryTimeoutError
from django.core.management.base import BaseCommand, CommandError

from core.demo import get_starter_snapshot, run_celery_probe


class Command(BaseCommand):
    help = "Verify the starter stack against PostgreSQL, Redis, and Celery."

    def add_arguments(self, parser) -> None:
        parser.add_argument("--timeout", type=int, default=15)

    def handle(self, *args, **options) -> None:
        snapshot = get_starter_snapshot()
        timeout = options["timeout"]

        if not snapshot.redis_ok:
            raise CommandError("Redis probe failed to round-trip the starter cache value.")

        self.stdout.write(
            self.style.SUCCESS(
                f"PostgreSQL ready: probe #{snapshot.probe_id} stored ({snapshot.probe_count} total records)."
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Redis ready: cache key '{snapshot.cache_key}' returned '{snapshot.cache_value}'."
            )
        )

        try:
            celery_result = run_celery_probe(timeout=timeout)
        except CeleryTimeoutError as exc:
            raise CommandError(f"Celery probe timed out after {timeout} seconds.") from exc

        if celery_result != "pong":
            raise CommandError(f"Unexpected Celery probe result: {celery_result}")

        self.stdout.write(self.style.SUCCESS("Celery ready: worker executed the starter ping task."))
