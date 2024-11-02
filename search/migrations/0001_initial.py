# Generated by Django 5.1.2 on 2024-11-02 21:20

import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('workshop', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TemporaryUser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserSearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('radius', models.IntegerField(default=500, validators=[django.core.validators.MinValueValidator(500), django.core.validators.MaxValueValidator(500000)])),
                ('declined', models.ManyToManyField(blank=True, related_name='declined', to='workshop.workshop')),
                ('favorites', models.ManyToManyField(blank=True, related_name='favorites', to='workshop.workshop')),
                ('temporary_user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='search.temporaryuser')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SearchFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_accepted', models.BooleanField()),
                ('workshop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.workshop')),
                ('search', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.usersearch')),
            ],
        ),
    ]