from datetime import timedelta

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

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
            status=Post.Status.PUBLISHED,
        )
        self.detail_url = reverse("blog:detail", args=[self.post.slug])

    def test_post_without_image_can_be_viewed(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.post_title)

    def test_missing_post_returns_404(self):
        response = self.client.get(reverse("blog:detail", args=["missing-post"]))

        self.assertEqual(response.status_code, 404)

    def test_guest_sees_name_and_comment_fields(self):
        response = self.client.get(self.detail_url)

        self.assertContains(response, 'class="comment-name-input"')
        self.assertContains(response, 'class="comment-input"')

    def test_guest_can_add_comment(self):
        response = self.client.post(
            self.detail_url,
            {"name": "A reader", "body": "A guest comment"},
        )

        self.assertRedirects(response, self.detail_url)
        comment = Comment.objects.get()
        self.assertEqual(comment.post, self.post)
        self.assertIsNone(comment.author)
        self.assertEqual(comment.name, "A reader")
        self.assertEqual(comment.body, "A guest comment")

    def test_guest_without_name_is_saved_as_anonymous(self):
        response = self.client.post(
            self.detail_url,
            {"name": "", "body": "An anonymous comment"},
        )

        self.assertRedirects(response, self.detail_url)
        comment = Comment.objects.get()
        self.assertIsNone(comment.author)
        self.assertEqual(comment.name, "Anonymous")

    def test_authenticated_user_can_add_comment(self):
        self.client.force_login(self.user)

        response = self.client.post(self.detail_url, {"body": "A useful comment"})

        self.assertRedirects(response, self.detail_url)
        comment = Comment.objects.get()
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.name, self.user.username)
        self.assertEqual(comment.body, "A useful comment")

    def test_authenticated_user_does_not_see_name_field(self):
        self.client.force_login(self.user)

        response = self.client.get(self.detail_url)

        self.assertNotContains(response, 'class="comment-name-input"')
        self.assertContains(response, 'class="comment-input"')

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


class CommentManagementTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username="author",
            email="author@example.com",
            password="a-secure-test-password",
        )
        self.other_user = User.objects.create_user(
            username="reader",
            email="reader@example.com",
            password="a-secure-test-password",
        )
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="a-secure-test-password",
        )
        self.post = Post.objects.create(
            post_title="Comments under management",
            post_preview="A preview",
            content="The post body",
            status=Post.Status.PUBLISHED,
        )
        self.author_comment = Comment.objects.create(
            post=self.post,
            author=self.author,
            name=self.author.username,
            body="Author comment",
        )
        self.other_comment = Comment.objects.create(
            post=self.post,
            author=self.other_user,
            name=self.other_user.username,
            body="Other comment",
        )
        self.anonymous_comment = Comment.objects.create(
            post=self.post,
            name="Anonymous",
            body="Anonymous comment",
        )

    def test_guest_sees_all_comments_immediately(self):
        response = self.client.get(self.post.get_absolute_url())

        self.assertContains(response, self.author_comment.body)
        self.assertContains(response, self.other_comment.body)
        self.assertContains(response, self.anonymous_comment.body)

    def test_author_can_edit_comment_and_change_is_immediately_visible(self):
        self.client.force_login(self.author)
        edit_url = reverse("blog:comment-edit", args=[self.author_comment.pk])

        response = self.client.post(edit_url, {"body": "Updated comment"})

        self.assertRedirects(response, self.post.get_absolute_url())
        self.author_comment.refresh_from_db()
        self.assertEqual(self.author_comment.body, "Updated comment")
        self.assertIsNotNone(self.author_comment.edited_at)

        self.client.logout()
        detail_response = self.client.get(self.post.get_absolute_url())
        self.assertContains(detail_response, "Updated comment")

    def test_user_cannot_edit_another_users_comment(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse("blog:comment-edit", args=[self.author_comment.pk]),
            {"body": "Unauthorized edit"},
        )

        self.assertEqual(response.status_code, 404)
        self.author_comment.refresh_from_db()
        self.assertEqual(self.author_comment.body, "Author comment")

    def test_guest_edit_redirects_to_login(self):
        edit_url = reverse("blog:comment-edit", args=[self.author_comment.pk])

        response = self.client.get(edit_url)

        self.assertRedirects(
            response,
            "%s?next=%s" % (reverse("login"), edit_url),
            fetch_redirect_response=False,
        )

    def test_author_can_delete_own_comment(self):
        self.client.force_login(self.author)
        delete_url = reverse("blog:comment-delete", args=[self.author_comment.pk])

        response = self.client.post(delete_url)

        self.assertRedirects(response, self.post.get_absolute_url())
        self.assertFalse(Comment.objects.filter(pk=self.author_comment.pk).exists())

    def test_user_cannot_delete_another_users_comment(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse("blog:comment-delete", args=[self.author_comment.pk])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Comment.objects.filter(pk=self.author_comment.pk).exists())

    def test_staff_can_delete_any_comment(self):
        self.client.force_login(self.admin_user)

        response = self.client.post(
            reverse("blog:comment-delete", args=[self.author_comment.pk])
        )

        self.assertRedirects(response, self.post.get_absolute_url())
        self.assertFalse(Comment.objects.filter(pk=self.author_comment.pk).exists())

    def test_delete_rejects_get_requests(self):
        self.client.force_login(self.author)

        response = self.client.get(
            reverse("blog:comment-delete", args=[self.author_comment.pk])
        )

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Comment.objects.filter(pk=self.author_comment.pk).exists())


class PublishingWorkflowTests(TestCase):
    def create_post(self, **overrides):
        values = {
            "post_title": "A publishing workflow post",
            "post_preview": "A short preview",
            "content": "The full post body",
        }
        values.update(overrides)
        return Post.objects.create(**values)

    def test_new_post_defaults_to_draft_and_generates_slug(self):
        post = self.create_post()

        self.assertEqual(post.status, Post.Status.DRAFT)
        self.assertEqual(post.slug, "a-publishing-workflow-post")
        self.assertIsNone(post.published_at)
        self.assertFalse(post.is_public)

    def test_duplicate_titles_receive_unique_slugs(self):
        first_post = self.create_post(post_title="Repeated title")
        second_post = self.create_post(post_title="Repeated title")

        self.assertEqual(first_post.slug, "repeated-title")
        self.assertEqual(second_post.slug, "repeated-title-2")

    def test_unicode_title_generates_unicode_slug(self):
        post = self.create_post(
            post_title="یادگیری جنگو",
            status=Post.Status.PUBLISHED,
        )

        self.assertEqual(post.slug, "یادگیری-جنگو")
        self.assertEqual(self.client.get(post.get_absolute_url()).status_code, 200)

    def test_slug_remains_stable_when_title_changes(self):
        post = self.create_post()
        original_slug = post.slug

        post.post_title = "A completely different title"
        post.save()

        self.assertEqual(post.slug, original_slug)

    def test_publishing_without_date_sets_current_time(self):
        before_publish = timezone.now()

        post = self.create_post(status=Post.Status.PUBLISHED)

        self.assertGreaterEqual(post.published_at, before_publish)
        self.assertLessEqual(post.published_at, timezone.now())
        self.assertTrue(post.is_public)

    def test_scheduled_post_is_not_public_before_publish_time(self):
        post = self.create_post(
            status=Post.Status.PUBLISHED,
            published_at=timezone.now() + timedelta(days=1),
        )

        self.assertFalse(post.is_public)
        self.assertFalse(Post.objects.published().filter(pk=post.pk).exists())

    def test_moving_post_to_draft_clears_publish_time(self):
        post = self.create_post(status=Post.Status.PUBLISHED)
        self.assertIsNotNone(post.published_at)

        post.status = Post.Status.DRAFT
        post.save(update_fields=("status",))

        self.assertIsNone(post.published_at)
        self.assertFalse(post.is_public)

    def test_public_list_only_contains_published_posts(self):
        draft = self.create_post(post_title="Hidden draft")
        published = self.create_post(
            post_title="Visible post",
            status=Post.Status.PUBLISHED,
        )
        self.create_post(
            post_title="Scheduled post",
            status=Post.Status.PUBLISHED,
            published_at=timezone.now() + timedelta(days=1),
        )

        response = self.client.get(reverse("blog:posts"))

        self.assertContains(response, published.post_title)
        self.assertNotContains(response, draft.post_title)
        self.assertNotContains(response, "Scheduled post")

    def test_public_posts_are_ordered_by_newest_publication(self):
        older_post = self.create_post(
            post_title="Older post",
            status=Post.Status.PUBLISHED,
            published_at=timezone.now() - timedelta(days=2),
        )
        newer_post = self.create_post(
            post_title="Newer post",
            status=Post.Status.PUBLISHED,
            published_at=timezone.now() - timedelta(days=1),
        )

        response = self.client.get(reverse("blog:posts"))

        self.assertEqual(list(response.context["posts_list"]), [newer_post, older_post])

    def test_public_cannot_open_draft_detail(self):
        draft = self.create_post()

        response = self.client.get(draft.get_absolute_url())

        self.assertEqual(response.status_code, 404)

    def test_staff_can_preview_draft_detail(self):
        draft = self.create_post()
        admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="a-secure-test-password",
        )
        self.client.force_login(admin_user)

        response = self.client.get(draft.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Staff preview")

    def test_legacy_numeric_url_redirects_to_slug_url(self):
        post = self.create_post(status=Post.Status.PUBLISHED)
        legacy_url = reverse("blog:legacy-detail", args=[post.pk])

        response = self.client.get(legacy_url)

        self.assertRedirects(
            response,
            post.get_absolute_url(),
            status_code=301,
            fetch_redirect_response=False,
        )


class AdminPostPanelTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="a-secure-test-password",
        )
        self.add_post_url = reverse("admin:blog_post_add")

    def test_admin_can_open_add_post_panel(self):
        self.client.force_login(self.admin_user)

        response = self.client.get(self.add_post_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add post")
        self.assertContains(response, 'name="post_title"')
        self.assertContains(response, 'name="slug"')
        self.assertContains(response, 'name="post_preview"')
        self.assertContains(response, 'name="content"')
        self.assertContains(response, 'name="status"')

    def test_admin_can_publish_post_from_panel(self):
        self.client.force_login(self.admin_user)

        response = self.client.post(
            self.add_post_url,
            {
                "post_title": "Published from the admin",
                "slug": "",
                "post_preview": "A preview created in the admin panel.",
                "content": "The full post content.",
                "status": Post.Status.PUBLISHED,
                "_save": "Save",
            },
        )

        self.assertRedirects(response, reverse("admin:blog_post_changelist"))
        post = Post.objects.get(post_title="Published from the admin")
        self.assertTrue(post.is_public)
        self.assertTrue(Post.objects.published().filter(pk=post.pk).exists())

    def test_admin_actions_publish_and_unpublish_post(self):
        post = Post.objects.create(
            post_title="Action-controlled post",
            post_preview="A preview",
            content="The post body",
        )
        changelist_url = reverse("admin:blog_post_changelist")
        self.client.force_login(self.admin_user)

        response = self.client.post(
            changelist_url,
            {
                "action": "publish_now",
                "_selected_action": [str(post.pk)],
            },
        )

        self.assertRedirects(response, changelist_url)
        post.refresh_from_db()
        self.assertTrue(post.is_public)

        response = self.client.post(
            changelist_url,
            {
                "action": "move_to_draft",
                "_selected_action": [str(post.pk)],
            },
        )

        self.assertRedirects(response, changelist_url)
        post.refresh_from_db()
        self.assertEqual(post.status, Post.Status.DRAFT)
        self.assertIsNone(post.published_at)
