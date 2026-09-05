from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def unique_slug(instance, title):
    slug_field = instance._meta.get_field("slug")
    base_slug = slugify(title, allow_unicode=True) or "entry"
    base_slug = base_slug[: slug_field.max_length]
    candidate = base_slug
    suffix = 2

    queryset = type(instance).objects.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    while queryset.filter(slug=candidate).exists():
        suffix_text = f"-{suffix}"
        candidate = f"{base_slug[: slug_field.max_length - len(suffix_text)]}{suffix_text}"
        suffix += 1

    return candidate


class Profile(models.Model):
    full_name = models.CharField(max_length=120, default="Bahar Barghbani")
    professional_title = models.CharField(max_length=180, blank=True)
    major = models.CharField(max_length=180, blank=True)
    institution = models.CharField(max_length=180, blank=True)
    location = models.CharField(max_length=120, blank=True)
    short_bio = models.TextField(
        blank=True,
        help_text="Two or three sentences for the homepage introduction.",
    )
    about = models.TextField(
        blank=True,
        help_text="Your longer academic and professional story.",
    )
    research_interests = models.TextField(
        blank=True,
        help_text="Enter one research interest per line.",
    )
    personal_note = models.TextField(
        blank=True,
        help_text="A short personal detail, such as hobbies or what motivates you.",
    )
    email = models.EmailField(blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    scholar_url = models.URLField("Google Scholar URL", blank=True)
    orcid_url = models.URLField("ORCID URL", blank=True)
    cv = models.FileField(
        upload_to="cv/",
        blank=True,
        validators=[FileExtensionValidator(["pdf"])],
        help_text="Upload your current CV as a PDF.",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Academic profile"
        verbose_name_plural = "Academic profile"

    def __str__(self):
        return self.full_name

    def clean(self):
        super().clean()
        if Profile.objects.exclude(pk=self.pk).exists():
            raise ValidationError("Only one academic profile can be created.")

    @property
    def interest_list(self):
        return [interest.strip() for interest in self.research_interests.splitlines() if interest.strip()]


class Research(models.Model):
    class Status(models.TextChoices):
        ONGOING = "ongoing", "Ongoing"
        PREPRINT = "preprint", "Preprint"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True, blank=True, allow_unicode=True)
    field = models.CharField(
        max_length=160,
        blank=True,
        help_text="The research area or discipline.",
    )
    summary = models.TextField(help_text="A short explanation for research cards.")
    abstract = models.TextField(
        blank=True,
        help_text="A longer description shown on the research detail page.",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ONGOING,
    )
    venue = models.CharField(
        max_length=220,
        blank=True,
        help_text="Journal, conference, lab, or institution.",
    )
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    collaborators = models.CharField(max_length=300, blank=True)
    publication_url = models.URLField(blank=True)
    code_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("display_order", "-year", "title")
        verbose_name_plural = "Research"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("pages:research-detail", args=[self.slug])


class Project(models.Model):
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True, blank=True, allow_unicode=True)
    summary = models.TextField(help_text="A short explanation for project cards.")
    description = models.TextField(
        blank=True,
        help_text="The problem, your approach, and the outcome.",
    )
    technologies = models.CharField(
        max_length=300,
        blank=True,
        help_text="Comma-separated tools or technologies.",
    )
    image = models.ImageField(upload_to="project_images/", blank=True)
    repository_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("display_order", "-created_at", "title")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("pages:project-detail", args=[self.slug])

    @property
    def technology_list(self):
        return [technology.strip() for technology in self.technologies.split(",") if technology.strip()]
