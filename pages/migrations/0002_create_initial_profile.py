from django.db import migrations


def create_initial_profile(apps, schema_editor):
    Profile = apps.get_model("pages", "Profile")
    Profile.objects.get_or_create(
        full_name="Bahar Barghbani",
        defaults={
            "short_bio": (
                "This website brings together my research, projects, writing, "
                "and the ideas I am exploring."
            ),
            "about": (
                "This website began as my first Django project and is growing "
                "into a home for my academic work, software projects, and writing."
            ),
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_initial_profile, migrations.RunPython.noop),
    ]
