# Generated by Django 2.1.7 on 2019-04-23 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("authentication", "0004_auto_20190421_2331")]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="image",
            field=models.ImageField(blank=True, upload_to="images/"),
        )
    ]
