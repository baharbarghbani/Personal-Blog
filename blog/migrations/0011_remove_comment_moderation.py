from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0010_comment_management"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="is_approved",
        ),
    ]
