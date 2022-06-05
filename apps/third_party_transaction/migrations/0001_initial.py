# Generated by Django 3.2 on 2022-06-06 16:05

from django.conf import settings
import django.core.management.utils
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import hashid_field.field


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MerchantAccount',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('merchant_app_key', hashid_field.field.BigHashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=20, prefix='', primary_key=True, serialize=False)),
                ('merchant_secret_key', models.CharField(default=django.core.management.utils.get_random_secret_key, max_length=64)),
                ('merchant_account_name', models.CharField(max_length=64)),
                ('account_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='merchant_account', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ThirdPartyTransaction',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wallet.transaction')),
                ('type', models.IntegerField(choices=[(4, 'Third Party Withdraw'), (3, 'Third Party Deposit')])),
                ('transaction_status', models.IntegerField(choices=[(0, 'Unverified'), (1, 'Verified'), (2, 'Cancelled')], default=0)),
                ('payment_status', models.IntegerField(choices=[(0, 'Waiting for Approval'), (1, 'Approved'), (2, 'Declined')], default=0)),
                ('merchant_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merchant_transactions', to='third_party_transaction.merchantaccount')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
            bases=('wallet.transaction',),
        ),
        migrations.CreateModel(
            name='TransactionOTP',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('otp', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=15, prefix='', primary_key=True, serialize=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='otps', to='third_party_transaction.thirdpartytransaction')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
