from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class PostQuerySet(models.QuerySet):
    def published(self):
        """Return posts whose publication time has arrived."""
        return self.filter(
            status=Post.Status.PUBLISHED,
            published_at__lte=timezone.now(),
        )


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft" # first value is stored in the database, second value is human-readable
        PUBLISHED = "published", "Published"

    post_title = models.CharField(max_length=100, default="Post")
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        allow_unicode=True,
        help_text="Used in the public URL. Leave blank to generate it from the title.",
    )
    post_preview = models.CharField(max_length=500, default="Preview")
    content = models.TextField(default="Content")
    date_posted = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )
    published_at = models.DateTimeField(
        blank=True,
        null=True,
        db_index=True,
        help_text="Leave blank to publish immediately, or choose a future time to schedule.",
    )

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ("-published_at", "-date_posted", "-id")

    def __str__(self):
        return self.post_title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})

    @property
    def is_public(self):
        return (
            self.status == self.Status.PUBLISHED
            and self.published_at is not None
            and self.published_at <= timezone.now()
        )

    @property
    def is_scheduled(self):
        return (
            self.status == self.Status.PUBLISHED
            and self.published_at is not None
            and self.published_at > timezone.now()
        )

    def save(self, *args, **kwargs):
        changed_fields = set()

        if not self.slug:
            self.slug = self._generate_unique_slug()
            changed_fields.add("slug")

        if self.status == self.Status.PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()
            changed_fields.add("published_at")
        elif self.status == self.Status.DRAFT:
            self.published_at = None
            changed_fields.add("published_at")

        if kwargs.get("update_fields") is not None:
            kwargs["update_fields"] = set(kwargs["update_fields"]) | changed_fields

        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        max_length = self._meta.get_field("slug").max_length
        base_slug = slugify(self.post_title, allow_unicode=True) or "post"
        base_slug = base_slug[:max_length]
        candidate = base_slug
        counter = 2
        posts = type(self).objects.all()

        if self.pk:
            posts = posts.exclude(pk=self.pk)

        while posts.filter(slug=candidate).exists():
            suffix = f"-{counter}"
            candidate = f"{base_slug[:max_length - len(suffix)]}{suffix}"
            counter += 1

        return candidate


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=50, default="Anonymous")
    body = models.TextField(default="Comment")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.post.post_title, self.name)
