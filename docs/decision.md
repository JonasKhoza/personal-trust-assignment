# Decisions

## 1. Database Readiness

Added a healthcheck to the postgresql container and configured the Django service to wait until the database is healthy before starting.

## Reasoning

Docker's default `depends_on` only ensures startup order, not readiness. This change prevents potential race-condions where Django application attempts to connect before the database is ready.

## 2. Protecting Client Views

- **Decision: ** Added `LoggingRequiredMixin` to `ClientList` & `ClientDetailView` to ensure only authenticated users can access sensitive client data.

## 3. Navbar Visibility

- **Decision: ** Added a conditonal check at `base.html` to conditionally render Clients nav item
- **Reasoning: ** Improves UI/UX by hiding options that unauthemticated users cannot access.
