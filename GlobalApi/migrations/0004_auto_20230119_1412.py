# Generated by Django 3.2.1 on 2023-01-19 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GlobalApi', '0003_auto_20230118_1425'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_active',
        ),
        migrations.AddField(
            model_name='order',
            name='order_state',
            field=models.CharField(default='I', max_length=10),
        ),
    ]
