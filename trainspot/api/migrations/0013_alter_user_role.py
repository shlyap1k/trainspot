# Generated by Django 4.1.7 on 2023-03-13 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0012_lesson_end_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[
                    ("client", "Client"),
                    ("manager", "Manager"),
                    ("admin", "Admin"),
                    ("trainer", "Trainer"),
                ],
                null=True,
            ),
        ),
    ]
