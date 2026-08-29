from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthenticationFlowTests(TestCase):
    def setUp(self):
        self.password = "a-secure-test-password"
        self.user = User.objects.create_user(
            username="bahar",
            email="bahar@example.com",
            password=self.password,
        )

    def test_guest_navigation_shows_login_and_signup(self):
        response = self.client.get(reverse("pages:home"))

        self.assertContains(response, 'href="%s">Login' % reverse("login"))
        self.assertContains(response, 'href="%s">Sign up' % reverse("register"))
        self.assertNotContains(response, ">Logout</button>")

    def test_user_can_login_with_email_and_is_redirected_home(self):
        response = self.client.post(
            reverse("login"),
            {"username": self.user.email, "password": self.password},
        )

        self.assertRedirects(response, reverse("pages:home"))

    def test_authenticated_navigation_uses_post_logout_form(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("pages:home"))

        self.assertContains(response, 'method="post" action="%s"' % reverse("logout"))
        self.assertContains(response, ">Logout</button>")
        self.assertNotContains(response, 'href="%s">Login' % reverse("login"))

    def test_logout_rejects_get_and_post_logs_user_out(self):
        self.client.force_login(self.user)

        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        response = self.client.post(reverse("logout"), follow=True)

        self.assertRedirects(response, reverse("pages:home"))
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertContains(response, "You have been logged out successfully.")
