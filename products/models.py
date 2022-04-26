from django.db import models

from core.models import TimeStampedModel

class Product(TimeStampedModel):
    product_name       = models.CharField(max_length=500)
    category           = models.ForeignKey('Category', on_delete=models.CASCADE)
    country            = models.ForeignKey('Country', on_delete=models.CASCADE)
    alcohol_percentage = models.IntegerField()
    price              = models.DecimalField(max_digits=10, decimal_places=3)
    average_rating     = models.DecimalField(max_digits=2, decimal_places=1)
    content            = models.CharField(max_length=1000)
    food_category      = models.ManyToManyField('FoodPairing', through="ProductFoodPairing")
    property           = models.JSONField()

    class Meta:
        db_table = 'products'

class ImageUrl(TimeStampedModel):
    image_url = models.CharField(max_length=200)
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'image_url'

class Category(TimeStampedModel):
    category = models.CharField(max_length=100)

    class Meta:
        db_table = 'categories'

class Country(TimeStampedModel):
    country = models.CharField(max_length=100)

    class Meta:
        db_table = 'countries'

class FoodPairing(TimeStampedModel):
    food_category = models.CharField(max_length=100)

    class Meta:
        db_table = 'foodpairings'

class ProductFoodPairing(TimeStampedModel):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    foodpairing = models.ForeignKey('FoodPairing', on_delete=models.CASCADE)

    class Meta:
        db_table = 'productfoodpairings'