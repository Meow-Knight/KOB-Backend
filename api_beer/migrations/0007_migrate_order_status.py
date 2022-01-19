# Generated by Django 3.2.8 on 2022-01-14 02:17

from django.db import migrations


def initial_data(apps, schema_editor):
    order_status_model = apps.get_model("api_beer", "OrderStatus")

    order_status = [
        order_status_model(name="PENDING"),
        order_status_model(name="CONFIRMED"),
        order_status_model(name="DELIVERING"),
        order_status_model(name="DELIVERED"),
        order_status_model(name="COMPLETED"),
        order_status_model(name="CANCELED"),
        order_status_model(name="NOT RECEIVED")

    ]

    order_status_model.objects.bulk_create(order_status)


class Migration(migrations.Migration):

    dependencies = [
        ('api_beer', '0006_auto_20220114_0917'),
    ]

    operations = [
        migrations.RunPython(initial_data, migrations.RunPython.noop)
    ]
