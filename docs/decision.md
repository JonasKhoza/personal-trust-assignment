## Database Readiness

Added a healthcheck to the postgresql container and configured the Django service to wait until the database is healthy before starting.

## Reasoning

Docker's default `depends_on` only ensures startup order, not readiness. This change prevents potential race-condions where Django application attempts to connect before the database is ready.
