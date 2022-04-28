from django.db   import models
from core.models import TimeStampedModel

class Product(TimeStampedModel):
    name               = models.CharField(max_length=500)
    category           = models.ForeignKey('Category', on_delete=models.CASCADE)
    country            = models.ForeignKey('Country', on_delete=models.CASCADE)
    alcohol_percentage = models.DecimalField(max_digits=3, decimal_places=1)
    price              = models.DecimalField(max_digits=10, decimal_places=3)
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
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'categories'

class Country(TimeStampedModel):
    origin = models.CharField(max_length=100)

    class Meta:
        db_table = 'countries'

class FoodPairing(TimeStampedModel):
    food_category = models.CharField(max_length=100)

    class Meta:
        db_table = 'food_pairings'

class ProductFoodPairing(TimeStampedModel):
    product     = models.ForeignKey('Product', on_delete=models.CASCADE)
    foodpairing = models.ForeignKey('FoodPairing', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_food_pairings'