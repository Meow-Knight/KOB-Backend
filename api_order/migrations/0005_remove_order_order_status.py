# Generated by Django 3.2.8 on 2022-02-26 03:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_order', '0004_migrate_progress_order_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_status',
        ),
    ]
