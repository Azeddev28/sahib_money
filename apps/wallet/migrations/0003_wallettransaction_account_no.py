# Generated by Django 3.2 on 2022-05-30 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_alter_wallet_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallettransaction',
            name='account_no',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
