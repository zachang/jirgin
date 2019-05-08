# Generated by Django 2.1.7 on 2019-03-19 22:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Flight",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("departure", models.DateField(default=datetime.date.today)),
                ("arrival", models.DateField()),
                ("fly_from", models.CharField(max_length=100)),
                ("fly_to", models.CharField(max_length=100)),
            ],
        )
    ]
