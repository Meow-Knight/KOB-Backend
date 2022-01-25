# Generated by Django 3.2.8 on 2021-12-31 03:14
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.db import migrations

from api_account.constants import UserData, RoleData


def initial_user_data(apps, schema_editor):
    account_model = apps.get_model("api_account", "Account")
    role_model = apps.get_model("api_account", "Role")

    user_role = role_model.objects.filter(id=RoleData.CUSTOMER.value.get('id')).first()

    accounts = []
    for user in UserData.users:
        accounts.append(account_model(id=user['id'],
                                      first_name=user['first_name'], last_name=user['last_name'],
                                      is_staff=False,
                                      username=user['email'].split('@')[0],
                                      avatar=user.get('avatar', 'https://res.cloudinary.com/ddqzgiilu/image/upload/v1640923830/SGroup/KOB/abstract-user-flat-3_mk2mve.png'),
                                      email=user['email'],
                                      address=user['address'],
                                      phone=user['phone'],
                                      age=user['age'],
                                      password=BaseUserManager().make_random_password(),
                                      role=user_role))

    account_model.objects.bulk_create(accounts)


class Migration(migrations.Migration):
    dependencies = [
        ('api_account', '0003_migrate_admin'),
    ]

    operations = [
        migrations.RunPython(initial_user_data, migrations.RunPython.noop)
    ]