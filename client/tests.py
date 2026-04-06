from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import IntegrityError,transaction

from .models import Client, Relationship
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

class ClientModelTest(TestCase):
    def test_valid_sa_id(self):
        client = Client(first_name="Jonas",last_name="Khoza",id_number="8001015009087")
        self.assertTrue(client.is_valid_sa_id())
    def test_invalid_sa_id_format(self):
        client = Client(first_name="Jonas",last_name="Khoza",id_number="12345")
        self.assertFalse(client.is_valid_sa_id())

    def test_clean_valid_id(self):
        client = Client(first_name="Jonas",last_name="Khoza",id_number="8001015009087")
        try:
            client.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly!")

class RelationshipModelTest(TestCase):

    def setUp(self):
        self.john = Client.objects.create(
            first_name="John",
            last_name="Doe",
            id_number="9001015009087"
        )
        self.jane = Client.objects.create(
            first_name="Jane",
            last_name="Doe",
            id_number="9001010009088"
        )

    def test_inverse_relationship_created(self):
        Relationship.objects.create(
            client_from=self.john,
            client_to=self.jane,
            relationship_type="husband"
        )

        # Check original
        self.assertTrue(
            Relationship.objects.filter(
                client_from=self.john,
                client_to=self.jane,
                relationship_type="husband"
            ).exists()
        )

        # Check inverse
        self.assertTrue(
            Relationship.objects.filter(
                client_from=self.jane,
                client_to=self.john,
                relationship_type="wife"
            ).exists()
        )

    def test_no_duplicate_inverse_created(self):
    
        Relationship.objects.create(
            client_from=self.john,
            client_to=self.jane,
            relationship_type="husband"
        )

        
        with self.assertRaises(IntegrityError):
            with transaction.atomic():  # This protects the rest of the test
                Relationship.objects.create(
                    client_from=self.john,
                    client_to=self.jane,
                    relationship_type="husband"
                )

        
        count = Relationship.objects.filter(
            client_from=self.jane,
            client_to=self.john
        ).count()
        self.assertEqual(count, 1)

    
