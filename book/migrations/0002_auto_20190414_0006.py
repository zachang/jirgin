# Generated by Django 2.1.7 on 2019-04-14 00:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("book", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="flight",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="books",
                to="flight.Flight",
            ),
        ),
        migrations.AlterField(
            model_name="book",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="books",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
