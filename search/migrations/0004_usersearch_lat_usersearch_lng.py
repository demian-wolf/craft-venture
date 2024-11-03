# Generated by Django 5.1.2 on 2024-11-03 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_remove_usersearch_declined_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersearch',
            name='lat',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usersearch',
            name='lng',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9),
            preserve_default=False,
        ),
    ]