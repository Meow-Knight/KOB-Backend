# Generated by Django 3.2.8 on 2021-12-31 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_beer', '0004_migrate_beer_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
