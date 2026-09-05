from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from blog.models import Post

from .models import Profile, Project, Research


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


class AcademicPortfolioTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.temp_media = TemporaryDirectory()
        cls.media_override = override_settings(MEDIA_ROOT=cls.temp_media.name)
        cls.media_override.enable()

    @classmethod
    def tearDownClass(cls):
        cls.media_override.disable()
        cls.temp_media.cleanup()
        super().tearDownClass()

    def setUp(self):
        self.profile = Profile.objects.first() or Profile.objects.create()
        self.profile.professional_title = "Graduate researcher and developer"
        self.profile.major = "Example Major"
        self.profile.institution = "Example University"
        self.profile.research_interests = "Human-centered systems\nData ethics"
        self.profile.save()

        self.research = Research.objects.create(
            title="Transparent decision-support systems",
            field="Human-centered computing",
            summary="Exploring how explanations affect trust in automated decisions.",
            status=Research.Status.ONGOING,
            featured=True,
        )
        self.hidden_research = Research.objects.create(
            title="Private research draft",
            summary="This work is not ready to share.",
            is_visible=False,
        )
        self.project = Project.objects.create(
            title="Research notebook",
            summary="A tool for organizing research observations.",
            technologies="Django, PostgreSQL",
            featured=True,
        )
        self.hidden_project = Project.objects.create(
            title="Private project draft",
            summary="This project is not ready to share.",
            is_visible=False,
        )
        self.post = Post.objects.create(
            post_title="What I learned this week",
            post_preview="Notes from an ongoing learning process.",
            content="A published reflection.",
            status=Post.Status.PUBLISHED,
        )
        self.draft_post = Post.objects.create(
            post_title="Unpublished notes",
            post_preview="Not public yet.",
            content="Draft content.",
        )

    def test_homepage_introduces_profile_and_featured_work(self):
        response = self.client.get(reverse("pages:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.profile.full_name)
        self.assertContains(response, self.profile.professional_title)
        self.assertContains(response, self.profile.major)
        self.assertContains(response, "Human-centered systems")
        self.assertContains(response, self.research.title)
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.post.post_title)
        self.assertNotContains(response, self.hidden_research.title)
        self.assertNotContains(response, self.hidden_project.title)
        self.assertNotContains(response, self.draft_post.post_title)

    def test_research_pages_only_show_visible_entries(self):
        response = self.client.get(reverse("pages:research"))

        self.assertContains(response, self.research.title)
        self.assertNotContains(response, self.hidden_research.title)
        self.assertEqual(self.client.get(self.research.get_absolute_url()).status_code, 200)
        self.assertEqual(
            self.client.get(self.hidden_research.get_absolute_url()).status_code,
            404,
        )

    def test_project_pages_only_show_visible_entries(self):
        response = self.client.get(reverse("pages:projects"))

        self.assertContains(response, self.project.title)
        self.assertContains(response, "Django")
        self.assertNotContains(response, self.hidden_project.title)
        self.assertEqual(self.client.get(self.project.get_absolute_url()).status_code, 200)
        self.assertEqual(
            self.client.get(self.hidden_project.get_absolute_url()).status_code,
            404,
        )

    def test_research_and_project_slugs_are_unique_and_stable(self):
        second_research = Research.objects.create(
            title=self.research.title,
            summary="A separate research entry.",
        )
        original_project_slug = self.project.slug
        self.project.title = "A renamed research notebook"
        self.project.save()

        self.assertEqual(self.research.slug, "transparent-decision-support-systems")
        self.assertEqual(second_research.slug, "transparent-decision-support-systems-2")
        self.assertEqual(self.project.slug, original_project_slug)

    def test_only_one_academic_profile_is_valid(self):
        second_profile = Profile(full_name="Another profile")

        with self.assertRaisesMessage(
            ValidationError,
            "Only one academic profile can be created.",
        ):
            second_profile.full_clean()

    def test_uploaded_cv_can_be_downloaded(self):
        self.profile.cv.save(
            "bahar-barghbani-cv.pdf",
            ContentFile(b"%PDF-1.4\n% test CV"),
        )

        response = self.client.get(reverse("pages:cv-download"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("attachment", response.headers["Content-Disposition"])
        self.assertIn("bahar-barghbani-cv.pdf", response.headers["Content-Disposition"])
        self.assertEqual(b"".join(response.streaming_content), b"%PDF-1.4\n% test CV")

    def test_cv_route_returns_404_until_file_is_uploaded(self):
        response = self.client.get(reverse("pages:cv-download"))

        self.assertEqual(response.status_code, 404)

    def test_admin_can_manage_academic_content(self):
        admin_user = User.objects.create_superuser(
            username="portfolio-admin",
            email="admin@example.com",
            password="a-secure-test-password",
        )
        self.client.force_login(admin_user)

        profile_response = self.client.get(reverse("admin:pages_profile_changelist"))
        research_response = self.client.get(reverse("admin:pages_research_add"))
        project_response = self.client.get(reverse("admin:pages_project_add"))

        self.assertEqual(profile_response.status_code, 200)
        self.assertContains(profile_response, self.profile.full_name)
        self.assertEqual(research_response.status_code, 200)
        self.assertEqual(project_response.status_code, 200)
