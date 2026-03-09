# Generated for TimeStampedModel (django_extensions)

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="profile",
            name="modified",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
