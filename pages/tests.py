from datetime import date
from tempfile import TemporaryDirectory

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Experience, Profile, Project, Research

class CVPortfolioContentTests(TestCase):
    def test_profile_contains_cv_positioning_and_contact_details(self):
        profile = Profile.objects.get(full_name="Bahar Barghbani")

        self.assertEqual(
            profile.professional_title,
            "Computer Engineering · Computer Systems & Architecture",
        )
        self.assertEqual(profile.institution, "Sharif University of Technology")
        self.assertIn("18.58/20", profile.about)
        self.assertIn("National Physics Olympiad", profile.about)
        self.assertIn("Overall GPA: 18.58/20", profile.education_detail_list)
        self.assertTrue(any("top 0.4%" in award for award in profile.award_list))
        self.assertIn("English: Professional proficiency", profile.language_list)
        self.assertEqual(profile.email, "bahar.brqbni@gmail.com")

    def test_cv_research_projects_and_experience_are_seeded(self):
        self.assertTrue(
            Research.objects.filter(
                slug="instruction-prefetching-and-processor-performance"
            ).exists()
        )
        job_scheduler = Project.objects.get(
            slug="job-shop-scheduling-with-graph-neural-networks"
        )
        self.assertEqual(
            job_scheduler.repository_url,
            "https://github.com/radalj/Job-Scheduler",
        )
        self.assertEqual(job_scheduler.date_label, "February 2026")
        sabanci = Experience.objects.get(
            role="Research Intern",
            organization="Sabanci University",
        )
        self.assertEqual(sabanci.date_label, "Summer 2026 - Present")
        self.assertTrue(sabanci.featured)


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
        self.experience = Experience.objects.create(
            role="Research Assistant",
            organization="Example Systems Lab",
            kind=Experience.Kind.RESEARCH,
            start_date=date(2025, 6, 1),
            summary="Evaluated architectural tradeoffs in memory systems.",
            highlights="Built a reproducible simulator workflow\nPresented findings to the lab",
            featured=True,
        )
        self.hidden_experience = Experience.objects.create(
            role="Private role draft",
            organization="Example Organization",
            kind=Experience.Kind.INTERNSHIP,
            summary="This role is not ready to share.",
            is_visible=False,
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
        self.assertContains(response, self.experience.role)
        self.assertNotContains(response, self.hidden_research.title)
        self.assertNotContains(response, self.hidden_project.title)
        self.assertNotContains(response, self.hidden_experience.role)
        self.assertNotContains(response, "Recent writing")

    def test_portrait_is_a_compact_shared_header_avatar(self):
        homepage = self.client.get(reverse("pages:home"))
        about_page = self.client.get(reverse("pages:about"))

        self.assertContains(homepage, 'class="site-avatar"')
        self.assertContains(homepage, "laptop-me.")
        self.assertNotContains(homepage, 'class="hero-portrait"')
        self.assertNotContains(about_page, 'class="about-photo"')

    def test_public_navigation_has_academic_order_without_account_links(self):
        self.profile.professional_title = (
            "Computer Engineering · Computer Systems & Architecture"
        )
        self.profile.save()

        response = self.client.get(reverse("pages:home"))
        content = response.content.decode()

        labels = [
            ">Research<",
            ">Projects<",
            ">Experience<",
            ">CV<",
            ">About<",
            ">Contact<",
        ]
        positions = [content.index(label) for label in labels]
        self.assertEqual(positions, sorted(positions))
        self.assertNotContains(response, ">Login<")
        self.assertNotContains(response, ">Sign up<")
        self.assertNotContains(response, ">Writing<")
        self.assertContains(
            response,
            "Computer Engineering · Computer Systems &amp; Architecture",
        )

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

    def test_experience_page_only_shows_visible_entries(self):
        response = self.client.get(reverse("pages:experience"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.experience.role)
        self.assertContains(response, self.experience.organization)
        self.assertContains(response, "Built a reproducible simulator workflow")
        self.assertNotContains(response, self.hidden_experience.role)

    def test_contact_page_shows_professional_contact_links(self):
        response = self.client.get(reverse("pages:contact"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "bahar.brqbni@gmail.com")
        self.assertContains(response, "https://www.linkedin.com/in/baharbarghbani")
        self.assertContains(response, "https://github.com/baharbarghbani")
        self.assertNotContains(response, "<form")
        self.assertNotContains(response, "Send message")

    def test_contact_page_rejects_form_submissions(self):
        response = self.client.post(
            reverse("pages:contact"),
            {
                "username": "A Reader",
                "email": "reader@example.com",
                "subject": "A question",
                "message": "This should not be processed.",
            },
        )

        self.assertEqual(response.status_code, 405)

    def test_about_page_shows_structured_academic_qualifications(self):
        response = self.client.get(reverse("pages:about"))

        self.assertContains(response, "Education and qualifications")
        self.assertContains(response, "Overall GPA: 18.58/20")
        self.assertContains(response, "Technical skills")
        self.assertContains(response, "English: Professional proficiency")

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

    def test_bundled_cv_is_available_without_an_admin_upload(self):
        response = self.client.get(reverse("pages:cv-download"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("attachment", response.headers["Content-Disposition"])
        self.assertIn("Bahar-Barghbani-CV.pdf", response.headers["Content-Disposition"])
        self.assertTrue(b"".join(response.streaming_content).startswith(b"%PDF"))

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
        experience_response = self.client.get(reverse("admin:pages_experience_add"))

        self.assertEqual(profile_response.status_code, 200)
        self.assertContains(profile_response, self.profile.full_name)
        self.assertEqual(research_response.status_code, 200)
        self.assertEqual(project_response.status_code, 200)
        self.assertEqual(experience_response.status_code, 200)
