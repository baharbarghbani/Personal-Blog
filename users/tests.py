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

    def test_guest_navigation_hides_public_account_links(self):
        response = self.client.get(reverse("pages:home"))

        self.assertNotContains(response, 'href="%s">Login' % reverse("login"))
        self.assertNotContains(response, 'href="%s">Sign up' % reverse("register"))
        self.assertNotContains(response, ">Logout</button>")
        self.assertEqual(self.client.get(reverse("login")).status_code, 200)

    def test_user_can_login_with_email_and_is_redirected_home(self):
        response = self.client.post(
            reverse("login"),
            {"username": self.user.email, "password": self.password},
        )

        self.assertRedirects(response, reverse("pages:home"))

    def test_staff_login_is_redirected_to_admin_panel(self):
        staff_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password=self.password,
        )

        response = self.client.post(
            reverse("login"),
            {"username": staff_user.email, "password": self.password},
        )

        self.assertRedirects(response, reverse("admin:index"))

    def test_staff_navigation_shows_admin_and_new_post_links(self):
        staff_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password=self.password,
        )
        self.client.force_login(staff_user)

        response = self.client.get(reverse("pages:home"))

        self.assertContains(
            response,
            'href="%s">Admin' % reverse("admin:index"),
        )
        self.assertContains(
            response,
            'href="%s">New post' % reverse("admin:blog_post_add"),
        )

    def test_regular_user_navigation_hides_admin_links(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("pages:home"))

        self.assertNotContains(response, reverse("admin:blog_post_add"))

    def test_staff_without_add_permission_does_not_see_new_post_link(self):
        staff_user = User.objects.create_user(
            username="editor",
            email="editor@example.com",
            password=self.password,
            is_staff=True,
        )
        self.client.force_login(staff_user)

        response = self.client.get(reverse("pages:home"))

        self.assertContains(response, 'href="%s">Admin' % reverse("admin:index"))
        self.assertNotContains(response, reverse("admin:blog_post_add"))

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
