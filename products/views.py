import random

from django.db.models import Avg
from django.http      import JsonResponse
from django.views     import View

from products.models  import Product, Category, Country, FoodPairing

class ProductSearchView(View):
    def get(self,request):

        search = request.GET.get('search')
        limit  = int(request.GET.get('limit',10))

        products_list = Product.objects.all().annotate(avg_rating= Avg('_Review__rating__score')).order_by('-avg_rating')

        if search in Category.objects.all().values_list('name',flat = True):
            products_list = products_list.filter(category_id__name=search)
            filter = f'Category : {search}'

        elif search in Country.objects.all().values_list('origin',flat = True):
            products_list = products_list.filter(country_id__origin=search)
            filter = f'Country : {search}'

        elif search in FoodPairing.objects.all().values_list('food_category',flat = True):
            products_list = products_list.filter(productfoodpairing__foodpairing__food_category=search)
            filter = f'Foodpairing : {search}'
        
        else:
            products_list = products_list.filter(name__icontains=search)
            filter = None

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
            } for product in products_list]    

            return JsonResponse({"filter":filter,"result":result}, status=200)

        else:
            message = "no_searched_products"
            recommended_words = {
                "Category"    : random.choice(Category.objects.all().values_list('name', flat = True)),
                "Country"     : random.choice(Country.objects.all().values_list('origin', flat = True)),
                "Foodpairing" : random.choice(FoodPairing.objects.all().values_list('food_category', flat = True))
                }
            return JsonResponse({"message":message,"recommended_words":recommended_words}, status=200)