# Remove username column: custom User uses email as USERNAME_FIELD (username = None).
# The initial migration created the table with username NOT NULL; the model no longer has it.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_timestamped_model"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="username",
        ),
    ]
