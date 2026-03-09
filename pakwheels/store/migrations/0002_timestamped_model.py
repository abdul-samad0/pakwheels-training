# Generated for TimeStampedModel (django_extensions)

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="category",
            name="modified",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="product",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="modified",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="productimage",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="productimage",
            name="modified",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="favorite",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="favorite",
            name="modified",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="like",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="like",
            name="modified",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="rating",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="rating",
            name="modified",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.RemoveIndex(
            model_name="product",
            name="store_produ_created_5555f3_idx",
        ),
        migrations.RemoveField(
            model_name="product",
            name="created_at",
        ),
        migrations.AlterModelOptions(
            model_name="product",
            options={"ordering": ["-created"]},
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(fields=["created"], name="store_produ_created_idx"),
        ),
    ]
