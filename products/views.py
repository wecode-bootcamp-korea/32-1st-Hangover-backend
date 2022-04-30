from django.views     import View
from django.http      import JsonResponse

from products.models  import Product
from reviews.models   import Review

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            foods= Product.objects.get(id=product_id).productfoodpairing_set.all()
            foods_list = []
            for food in foods:
                foods_list.append(
                    food.foodpairing.food_category
                    )

            product_detail = {
                'name'               : product.name,
                'price'              : product.price,
                'country'            : product.country.origin,
                'alcohol_percentage' : product.alcohol_percentage,
                'food_category'      : foods_list,
                'property'           : product.property,
                'reviews'            : Review.objects.filter(product_id=product_id).count()
            }

            return JsonResponse({'product_detail' : product_detail}, status = 200)

        except Product.DoesNotExist:
            return JsonResponse({'message': 'NO_PRODUCT'}, status=404)