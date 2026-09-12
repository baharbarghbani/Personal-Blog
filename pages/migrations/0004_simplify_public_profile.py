from django.db import migrations, models


def simplify_public_profile(apps, schema_editor):
    """Hide the title and apply Bahar's corrected academic details."""

    Profile = apps.get_model("pages", "Profile")
    profile = Profile.objects.order_by("pk").first()
    if not profile:
        return

    profile.professional_title = ""
    profile.education_details = (
        profile.education_details.replace("July 2028", "July 2027")
        .replace("Major GPA: 18.89/20", "Major GPA: 19.13/20")
    )
    profile.about = (
        profile.about.replace("July 2028", "July 2027")
        .replace("major GPA is 18.89/20", "major GPA is 19.13/20")
    )
    profile.save(
        update_fields=("professional_title", "education_details", "about")
    )


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0003_experience_alter_profile_professional_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="professional_title",
            field=models.CharField(blank=True, default="", max_length=180),
        ),
        migrations.RunPython(
            simplify_public_profile,
            migrations.RunPython.noop,
        ),
    ]
