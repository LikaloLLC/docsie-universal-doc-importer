# Generated by Django 2.2.2 on 2021-09-14 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectorToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(max_length=30, verbose_name='provider')),
                ('token', models.TextField(help_text='"oauth_token" (OAuth1) or access token (OAuth2)', verbose_name='token')),
                ('token_secret', models.TextField(blank=True, help_text='"oauth_token_secret" (OAuth1) or refresh token (OAuth2)', verbose_name='token secret')),
                ('expires_at', models.DateTimeField(blank=True, null=True, verbose_name='expires at')),
            ],
        ),
    ]
