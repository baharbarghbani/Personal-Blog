import datetime

from django.db import migrations, models
from django.utils.text import slugify


def populate_publishing_fields(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    used_slugs = set()

    for post in Post.objects.order_by("pk").iterator():
        base_slug = slugify(post.post_title, allow_unicode=True)[:120] or "post"
        candidate = base_slug
        counter = 2

        while candidate in used_slugs:
            suffix = f"-{counter}"
            candidate = f"{base_slug[:120 - len(suffix)]}{suffix}"
            counter += 1

        used_slugs.add(candidate)
        post.slug = candidate
        post.status = "published"
        post.published_at = datetime.datetime.combine(
            post.date_posted,
            datetime.time.min,
            tzinfo=datetime.timezone.utc,
        )
        post.save(update_fields=("slug", "status", "published_at"))


def clear_publishing_fields(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    Post.objects.update(slug=None, status="draft", published_at=None)


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0008_alter_comment_body_alter_comment_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="slug",
            field=models.SlugField(
                allow_unicode=True,
                blank=True,
                db_index=False,
                help_text=(
                    "Used in the public URL. Leave blank to generate it from the title."
                ),
                max_length=120,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="status",
            field=models.CharField(
                choices=[("draft", "Draft"), ("published", "Published")],
                db_index=True,
                default="draft",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="published_at",
            field=models.DateTimeField(
                blank=True,
                db_index=True,
                help_text=(
                    "Leave blank to publish immediately, or choose a future time to schedule."
                ),
                null=True,
            ),
        ),
        migrations.RunPython(
            populate_publishing_fields,
            clear_publishing_fields,
        ),
        migrations.AlterField(
            model_name="post",
            name="slug",
            field=models.SlugField(
                allow_unicode=True,
                blank=True,
                help_text=(
                    "Used in the public URL. Leave blank to generate it from the title."
                ),
                max_length=120,
                unique=True,
            ),
        ),
        migrations.AlterModelOptions(
            name="post",
            options={"ordering": ("-published_at", "-date_posted", "-id")},
        ),
    ]
