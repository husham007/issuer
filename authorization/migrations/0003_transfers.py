# Generated by Django 2.1.2 on 2018-10-21 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0002_authorization_presentment_card_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_id', models.CharField(max_length=15)),
                ('transaction_id', models.CharField(max_length=15)),
                ('account_name', models.CharField(max_length=20)),
                ('entry_type', models.CharField(max_length=15)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(max_length=3)),
            ],
        ),
    ]
