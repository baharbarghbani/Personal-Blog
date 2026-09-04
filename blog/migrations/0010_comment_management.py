from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def approve_existing_comments(apps, schema_editor):
    Comment = apps.get_model("blog", "Comment")
    Comment.objects.update(is_approved=True)


def mark_existing_comments_pending(apps, schema_editor):
    Comment = apps.get_model("blog", "Comment")
    Comment.objects.update(is_approved=False)


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog", "0009_post_publishing_workflow"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="blog_comments",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="edited_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="comment",
            name="is_approved",
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.RunPython(
            approve_existing_comments,
            mark_existing_comments_pending,
        ),
        migrations.AlterModelOptions(
            name="comment",
            options={"ordering": ("date_added", "id")},
        ),
    ]
