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

## 4. Login & Logout Navbar

- **Decision:** Show `Clients` link, username, and `Logout` only if the user is authenticated.
- **Reasoning:** Improves UX by showing relevant navigation based on authentication.
- **Alternative:** Could show `Clients` link always but block access at the view level. Rejected because it’s less user-friendly.

## 5. Django Auth Views

- **Decision:** Use Django built-in `LoginView` and `LogoutView`.
- **Reasoning:** Avoids reinventing authentication, works with existing `LoginRequiredMixin`.

## 6. Authentication Tests

**Decision:** Added automated tests for login/logout functionality and access control for client views.

**Reasoning:**

- Ensure that unauthenticated users cannot access the client list.
- Confirm that login and logout behave as expected.
- Verify that the navbar correctly displays login/logout links based on authentication state.

## 7. Create new client functionality

**Decision: ** Implemented client creation using a custom ClientCreateView with a ClientForm and AddressFormSet.
** Reasoning: ** Allows simultaneous creation of a client and their associated addresses in a single request.

## 8. Search

**Decision: ** Implemented client search using HTMX for dynamic, partial page updates.
**Reasoning: ** Provides a smoother user experience by updating only the client table without a full page reload.
**Implementation Detail: **

- Used hx-get, hx-trigger, and hx-target for real-time search.
- Server detects HX-Request header and returns a partial template (client_table.html).

## 9. Client Relationships

** Decision: ** Introduced a Relationship model to represent relationships between clients (e.g., husband, wife, parent, child).
** Reasoning: ** Validation depends on client_from, which is injected at runtime and not available during model instantiation.
