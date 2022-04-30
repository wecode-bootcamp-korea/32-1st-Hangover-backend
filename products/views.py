from django.views     import View
from django.http      import JsonResponse

from products.models  import Product
from reviews.models   import Review

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product    = Product.objects.get(id=product_id)

            food_list         = product.productfoodpairing_set.all()
            food_pairing_list = []
            for food in food_list:
                food_pairing_list.append(
                    food.foodpairing.food_category
                    )

            average_rating      = product._Review.all()
            average_rating_list = []
            for average in average_rating:
                average_rating_list.append(
                    float(average.rating.score)
                )

            product_detail = {
                'name'               : product.name,
                'price'              : product.price,
                'country'            : product.country.origin,
                'alcohol_percentage' : product.alcohol_percentage,
                'food_category'      : food_pairing_list,
                'property'           : product.property,
                'reviews'            : Review.objects.filter(product_id=product_id).count(),
                'ave_rating'         : sum(average_rating_list)/len(average_rating_list)
            }
            return JsonResponse({'product_detail' : product_detail}, status = 200)

        except Product.DoesNotExist:
            return JsonResponse({'message': 'NO_PRODUCT'}, status=404)