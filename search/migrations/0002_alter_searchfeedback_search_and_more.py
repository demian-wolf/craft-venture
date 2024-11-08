# Generated by Django 5.1.2 on 2024-11-02 22:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
        ('workshop', '0002_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchfeedback',
            name='search',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='search.usersearch'),
        ),
        migrations.AlterField(
            model_name='searchfeedback',
            name='workshop',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='workshop.workshop'),
        ),
    ]
