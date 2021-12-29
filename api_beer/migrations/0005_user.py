# Generated by Django 3.2.8 on 2021-12-29 08:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_beer', '0004_migrate_beer_discount'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('delivery_address', models.TextField()),
                ('phone', models.CharField(max_length=20)),
                ('age', models.IntegerField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user',
                'ordering': ['last_name', 'first_name'],
            },
        ),
    ]
