# Generated by Django 4.1.7 on 2023-04-29 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0021_alter_mailinglist_subscribers"),
    ]

    operations = [
        migrations.CreateModel(
            name="Video",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("file", models.FileField(upload_to="videos/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]