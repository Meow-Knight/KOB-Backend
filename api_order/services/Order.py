from django.db import transaction

from api_order import constants
from api_account.constants.Data import RoleData
from api_order.models import OrderStatus
from api_order.serializers import ProgressSerializer


class OrderService:

    @classmethod
    @transaction.atomic
    def add_progress_order(cls, order, order_status):
        progress = {"order_status": order_status.id, "order": order.id}
        progress = ProgressSerializer(data=progress)
        if progress.is_valid(raise_exception=True):
            progress.save()

    @classmethod
    @transaction.atomic
    def my_switcher(cls, key_change, order_status, role):
        if constants.OrderStatus.CONFIRMED.value.get("name") == key_change and role != RoleData.CUSTOMER.value.get("name"):
            if order_status == constants.OrderStatus.PENDING.value.get("name"):
                new_status = OrderStatus.objects.filter(name=constants.OrderStatus.CONFIRMED.value.get("name"))
                if new_status.exists():
                    return new_status.first()
        elif constants.OrderStatus.DELIVERING.value.get("name") == key_change and role != RoleData.CUSTOMER.value.get("name"):
            if order_status == constants.OrderStatus.CONFIRMED.value.get("name") \
                    or order_status == constants.OrderStatus.NOTRECEIVED.value.get("name"):
                new_status = OrderStatus.objects.filter(name=constants.OrderStatus.DELIVERING.value.get("name"))
                if new_status.exists():
                    return new_status.first()
        elif constants.OrderStatus.DELIVERED.value.get("name") == key_change and role != RoleData.CUSTOMER.value.get("name"):
            if order_status == constants.OrderStatus.DELIVERING.value.get("name"):
                new_status = OrderStatus.objects.filter(name=constants.OrderStatus.DELIVERED.value.get("name"))
                if new_status.exists():
                    return new_status.first()
        elif constants.OrderStatus.COMPLETED.value.get("name") == key_change and role == RoleData.CUSTOMER.value.get("name"):
            if order_status == constants.OrderStatus.DELIVERED.value.get("name"):
                new_status = OrderStatus.objects.filter(name=constants.OrderStatus.COMPLETED.value.get("name"))
                if new_status.exists():
                    return new_status.first()
        elif constants.OrderStatus.NOTRECEIVED.value.get("name") == key_change and role == RoleData.CUSTOMER.value.get("name"):
            if order_status == constants.OrderStatus.DELIVERED.value.get("name"):
                new_status = OrderStatus.objects.filter(name=constants.OrderStatus.NOTRECEIVED.value.get("name"))
                if new_status.exists():
                    return new_status.first()

    @classmethod
    @transaction.atomic
    def change_order_status(cls, order, key_change, role):
        res = {"success": False, "id": order.id}
        order_status = order.order_status.name
        new_status = cls.my_switcher(key_change, order_status, role)
        if new_status is not None:
            order.order_status = new_status
            order.save()
            cls.add_progress_order(order, new_status)
            res['success'] = True
        return res

    @classmethod
    @transaction.atomic
    def cancel_order(cls, order):
        if order.exists():
            order = order.first()
            res = {"success": False, "id": order.id}
            order_status = order.order_status.name
            if constants.OrderStatus.PENDING.value.get('name') == order_status:
                new_status = OrderStatus.objects.filter(name=constants.OrderStatus.CANCELED.value.get('name'))
                if new_status.exists():
                    order.order_status = new_status.first()
                    order.save()
                    cls.add_progress_order(order, new_status.first())
                    res['success'] = True
            return res
