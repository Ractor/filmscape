# Generated by Django 4.1.7 on 2023-03-10 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('shortName', models.CharField(blank=True, max_length=255)),
                ('iconUri', models.URLField()),
                ('manifestUri', models.URLField()),
                ('source', models.SlugField()),
                ('focus', models.BooleanField()),
                ('disabled', models.BooleanField()),
                ('description', models.TextField(null=True)),
                ('isFeatured', models.BooleanField()),
                ('licenseServers', models.JSONField()),
                ('licenseRequestHeaders', models.JSONField()),
                ('adTagUri', models.URLField(max_length=2048, null=True)),
                ('imaVideoId', models.SlugField(null=True)),
                ('imaContentSrcId', models.PositiveIntegerField(null=True)),
                ('storedProgress', models.PositiveIntegerField(null=True)),
                ('storedContent', models.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Features',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.SlugField()),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='filmscape.video')),
            ],
            options={
                'unique_together': {('video', 'feature')},
            },
        ),
        migrations.CreateModel(
            name='ExtraText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uri', models.URLField()),
                ('language', models.CharField(max_length=2)),
                ('kind', models.CharField(max_length=20)),
                ('mime', models.CharField(max_length=20)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extraText', to='filmscape.video')),
            ],
            options={
                'unique_together': {('video', 'uri')},
            },
        ),
        migrations.CreateModel(
            name='Drm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drm', models.SlugField()),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drm', to='filmscape.video')),
            ],
            options={
                'unique_together': {('video', 'drm')},
            },
        ),
    ]