from unittest.mock import patch

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="website@example.com",
    CONTACT_RECEIVER_EMAIL="owner@example.com",
    CONTACT_EMAIL_SUBJECT_PREFIX="[Personal Blog]",
)
class ContactEmailTests(TestCase):
    def setUp(self):
        self.contact_url = reverse("pages:contact")
        self.valid_data = {
            "username": "A Reader",
            "subject": "A question",
            "email": "reader@example.com",
            "message": "Thanks for the helpful article.",
        }

    def test_contact_page_displays_form(self):
        response = self.client.get(self.contact_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="subject"')
        self.assertContains(response, 'name="message"')

    def test_valid_submission_sends_email_and_redirects(self):
        response = self.client.post(self.contact_url, self.valid_data)

        self.assertRedirects(response, reverse("pages:thank-you"))
        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox[0]
        self.assertEqual(email.subject, "[Personal Blog] A question")
        self.assertEqual(email.from_email, "website@example.com")
        self.assertEqual(email.to, ["owner@example.com"])
        self.assertEqual(email.reply_to, ["reader@example.com"])
        self.assertIn("Name: A Reader", email.body)
        self.assertIn("Thanks for the helpful article.", email.body)

    def test_invalid_submission_does_not_send_email(self):
        invalid_data = self.valid_data | {"email": "not-an-email"}

        response = self.client.post(self.contact_url, invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid email address.")
        self.assertEqual(len(mail.outbox), 0)

    def test_delivery_failure_keeps_form_and_shows_error(self):
        with self.assertLogs("pages.views", level="ERROR"):
            with patch(
                "pages.views.send_contact_email",
                side_effect=OSError("SMTP unavailable"),
            ):
                response = self.client.post(self.contact_url, self.valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "We could not send your message right now")
        self.assertContains(response, self.valid_data["message"])
        self.assertEqual(len(mail.outbox), 0)
