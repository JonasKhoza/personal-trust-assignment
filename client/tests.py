from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
    
    def test_login_page_renders(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    def test_login_suceess_redirects(self):
        response = self.client.post(reverse("login"), {"username": "testuser", "password":"password123"})
        self.assertRedirects(response, reverse("client_list"))

    def test_logout_redirects_to_login(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("login"))

    def test_client_list_requires_login(self):
        response = self.client.get(reverse("client_list"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('client_list')}")

    def test_navbar_links_authenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('home'))
        self.assertContains(response, "Clients")
        self.assertContains(response, "Logout")
        self.assertContains(response, "Logged in as testuser")
        self.assertNotContains(response, "Login")

    def test_navbar_links_unauthenticated(self):
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, "Clients")
        self.assertNotContains(response, "Logout")
        self.assertContains(response, "Login")