from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Comment, Post


class CommentFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="bahar",
            email="bahar@example.com",
            password="a-secure-test-password",
        )
        self.post = Post.objects.create(
            post_title="A post without an image",
            post_preview="A short preview",
            content="The post body",
        )
        self.detail_url = reverse("blog:detail", args=[self.post.pk])

    def test_post_without_image_can_be_viewed(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.post_title)

    def test_missing_post_returns_404(self):
        response = self.client.get(reverse("blog:detail", args=[999999]))

        self.assertEqual(response.status_code, 404)

    def test_guest_is_prompted_to_log_in(self):
        response = self.client.get(self.detail_url)
        login_url = "%s?next=%s" % (reverse("login"), self.detail_url)

        self.assertContains(response, 'href="%s"' % login_url)
        self.assertNotContains(response, 'class="comment-input"')

    def test_guest_post_redirects_to_login_without_creating_comment(self):
        response = self.client.post(self.detail_url, {"body": "A comment"})

        self.assertRedirects(
            response,
            "%s?next=%s" % (reverse("login"), self.detail_url),
            fetch_redirect_response=False,
        )
        self.assertFalse(Comment.objects.exists())

    def test_authenticated_user_can_add_comment(self):
        self.client.force_login(self.user)

        response = self.client.post(self.detail_url, {"body": "A useful comment"})

        self.assertRedirects(response, self.detail_url)
        comment = Comment.objects.get()
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.name, self.user.username)
        self.assertEqual(comment.body, "A useful comment")

    def test_invalid_comment_is_not_saved_and_shows_error(self):
        self.client.force_login(self.user)

        response = self.client.post(self.detail_url, {"body": ""})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")
        self.assertFalse(Comment.objects.exists())

    def test_comment_longer_than_limit_is_not_saved(self):
        self.client.force_login(self.user)

        response = self.client.post(self.detail_url, {"body": "a" * 256})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ensure this value has at most 255 characters")
        self.assertFalse(Comment.objects.exists())

    def test_comment_form_accepts_csrf_protected_submission(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        response = client.get(self.detail_url)
        self.assertContains(response, 'name="csrfmiddlewaretoken"', count=2)
        csrf_token = response.cookies["csrftoken"].value

        response = client.post(
            self.detail_url,
            {"body": "CSRF protected", "csrfmiddlewaretoken": csrf_token},
        )

        self.assertRedirects(response, self.detail_url)
        self.assertTrue(Comment.objects.filter(body="CSRF protected").exists())
