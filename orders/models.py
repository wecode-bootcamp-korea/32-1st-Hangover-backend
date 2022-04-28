from django.db       import models
from core.models     import TimeStampedModel
from users.models    import User
from products.models import Product

class Order(TimeStampedModel):
    order_number = models.CharField(max_length=100)
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    status       = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'

class OrderItem(TimeStampedModel):
    order             = models.ForeignKey('Order', on_delete=models.CASCADE)
    quantity          = models.PositiveIntegerField()
    product           = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_item_status = models.ForeignKey('OrderItemStatus', on_delete=models.CASCADE)
    shipment          = models.ForeignKey('OrderShipment', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'order_items'

class OrderStatus(models.Model):
    status = models.CharField(max_length=50)

    class Meta:
        db_table ='order_statuses'

class OrderItemStatus(models.Model):
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'order_item_statuses'

class OrderShipment(models.Model):
    tracking_number  = models.CharField(max_length=200)
    delivery_company = models.CharField(max_length=200)

    class Meta:
        db_table = 'order_shipments'