from django.shortcuts import render
from products.models import Product, ImageUrl, Category, Country, FoodPairing 
from django.db.models import Q

from django.http            import JsonResponse
from django.views           import View

# Create your views here.
class ProductListView(View):
    def get(self,request):
        
        print(request.GET)
        #Check:objects.all 적용 ㄱㅊ?        
        category     = request.Get.get('category')
        price        = request.Get.get('price',[0,1000000])
        rating       = request.Get.get('rating',0)
        country      = request.Get.get('country')
        food_pairing = request.Get.get('food_pairing')

        #무한스크롤?
        pagination   = request.Get.get('pagination',1)      
        limit        = request.Get.get('limit',12)

        #기본적으로 orderby문을 통해서 평점순 > 가격순으로 먼저 정렬
        sort         = request.Get.get('sort')
        request      = request.Get.get('request')
        search       = request.Get.get('search')
        
        print(search)
        print(type(search))

        return JsonResponse({'messasge':'성공!'}, status=200)

        #searchlist > 
        # if search:
        #     if search
        #     category_list = [

        #     ]
        #     category_list = Category.objects.all().values('name') + Country.objects.all().values('origin') + FoodPairing.objects.all().values('food_category')


        


        


        







