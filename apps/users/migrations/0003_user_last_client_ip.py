# Generated by Django 3.2 on 2022-08-10 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_merchantaccount_redirect_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_client_ip',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
