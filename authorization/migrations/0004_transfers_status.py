# Generated by Django 2.1.2 on 2018-10-21 11:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0003_transfers'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfers',
            name='status',
            field=models.CharField(default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
    ]
