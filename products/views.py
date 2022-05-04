import random

from django.db.models import Avg, Q
from django.http      import JsonResponse
from django.views     import View

from products.models  import Product, Category, Country, FoodPairing

class ProductSearchView(View):
    def get(self,request):

        search = request.GET.get('search')
        limit  = int(request.GET.get('limit',10))

        keyword_list = {
            "Category"    : Category.objects.all().values_list('name',flat = True),
            "Country"     : Country.objects.all().values_list('origin',flat = True),
            "Foodpairing" : FoodPairing.objects.all().values_list('food_category',flat = True),
        }
        
        for key,values in keyword_list.items():
            for word in values:
                if search in word:
                    filter,matched_keyword = key,word

        products_list = Product.objects.all().annotate(avg_rating= Avg('reviews__rating__score')).order_by('-avg_rating')

        if filter in globals():
            Q_filter = {
                'Category'        : Q(category_id__name=matched_keyword),
                'Country'         : Q(country_id__origin=matched_keyword),
                'Foodpairing'     : Q(productfoodpairing__foodpairing__food_category=matched_keyword),
            }
            products_list = products_list.filter(Q_filter[filter])
        else:
            products_list          = products_list.filter(name__icontains=search)
            filter,matched_keyword = None,None

        if products_list:
            result = [{
                'id'           :product.id,
                'price'        :product.price,
                'name'         :product.name,
                'country'      :product.country.origin,
                'category'     :product.category.name,
                'image_url'    :product.imageurl_set.first().image_url,
                'created_at'   :product.created_at,
                'rating'       :product.avg_rating, 
            } for product in products_list][:limit]

            return JsonResponse({"response":[{"filter":filter,"matched_keyword":matched_keyword,"result":result}]}, status=200)

        else:
            message = "no_searched_products"
            recommended_words = {
                "Category"    : random.choice(Category.objects.all().values_list('name', flat = True)),
                "Country"     : random.choice(Country.objects.all().values_list('origin', flat = True)),
                "Foodpairing" : random.choice(FoodPairing.objects.all().values_list('food_category', flat = True))
                }
            return JsonResponse({"response":[message,recommended_words]}, status=200)


class ProductDetailView(View):
    def get(self, request, product_id):
        try:

            product = Product.objects\
                .annotate(avg_rating = Avg('reviews__rating__score'))\
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