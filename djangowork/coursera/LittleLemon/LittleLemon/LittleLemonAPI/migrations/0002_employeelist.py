# Generated by Django 4.2.7 on 2023-11-14 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LittleLemonAPI", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmployeeList",
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
                ("name", models.CharField(max_length=255)),
                ("age", models.DecimalField(decimal_places=0, max_digits=2)),
                (
                    "job_title",
                    models.CharField(
                        choices=[
                            ("bar", "bar"),
                            ("floor", "floor"),
                            ("manager", "manager"),
                        ],
                        max_length=10,
                    ),
                ),
            ],
        ),
    ]
