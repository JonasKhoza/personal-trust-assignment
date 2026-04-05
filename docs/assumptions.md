# Assumptions

1. Users logging into the admin interface are considered authenticated and have access to the Client list.
2. All client sensitive pages should be protected with authentication.
3. The login page is either the Django admin login (`/admin/login/`) or a custom login page implemented later.
4. Navbar visibility logic only needs to reflect authenticated state. Authorization levels (staff vs normal users) are not handled yet.
5. Sessions remain active until the user explicitly logs out.
