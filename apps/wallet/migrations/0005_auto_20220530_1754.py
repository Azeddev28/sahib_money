# Generated by Django 3.2 on 2022-05-30 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0004_alter_wallet_total_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallettransaction',
            name='from_wallet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_from_wallet', to='wallet.wallet'),
        ),
        migrations.AlterField(
            model_name='wallettransaction',
            name='to_wallet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_to_wallet', to='wallet.wallet'),
        ),
    ]
