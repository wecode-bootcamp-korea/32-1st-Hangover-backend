from django.views     import View
from django.models.db import Avg
from django.http      import JsonResponse

from products.models import Product
from reviews.models  import Review

"""
목적: 상품의 상세 정보를 데이터베이스에서 가져오는 api

필요한 정보: 제품의 고유번호

보내줘야 하는 정보: 이름, 가격, 원산지, 도수, 푸드 페어링, 특성, 리뷰 수, 평점
"""



class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects\
                             .annotate(avg_rating=Avg('reviews__rating__score'))\
                             .get(id=product_id)

            product_detail = {
                'name'               : product.name,
                'price'              : product.price,
                'country'            : product.country.origin,
                'alcohol_percentage' : product.alcohol_percentage,
                'food_category'      : [food.food_category for food in product.food_category.all()],
                'property'           : product.property,
                'reviews'            : product.reviews.all().count(),
                'ave_rating'         : product.avg_rating
            }
            return JsonResponse({'product_detail' : product_detail}, status = 200)

        except Product.DoesNotExist:
            return JsonResponse({'message': 'NO_PRODUCT'}, status=404)