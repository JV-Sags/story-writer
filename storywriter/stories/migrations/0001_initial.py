# Generated by Django 5.1.6 on 2025-03-01 05:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('is_published', models.BooleanField(default=False)),
                ('likes', models.IntegerField(default=0)),
                ('bookmarks', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characters', to='stories.story')),
            ],
        ),
        migrations.CreateModel(
            name='StorySettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(max_length=50)),
                ('visibility', models.CharField(choices=[('public', 'Public'), ('private', 'Private')], max_length=10)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], max_length=10)),
                ('story', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to='stories.story')),
            ],
        ),
    ]
