from products.models  import Product, ImageUrl, Category, Country, FoodPairing ,ProductFoodPairing
from django.db.models import Avg, Count,Q,F

from django.http      import JsonResponse
from django.views     import View

import random

class ProductListView(View):
    def get(self,request):

        search  = request.GET.get('search')
        page    = int(request.GET.get('page',1))
        limit   = int(request.GET.get('limit',12))
        sorting = request.GET.get('sorting',['-avg_rating','-price'])

        #FIXME : SORT : RANDOM을 추가해야함. but how?
        if sorting != ['-avg_rating','-price']:
            sorting  = ['-avg_rating','-price'] if sorting == '-avg_rating' else [sorting,'-avg_rating']



        #FIXME : SEARCH부분을 아래의 필드명 변경과 일관되도록 수정해야 함
        
        products_list = Product.objects.all().annotate(
            avg_rating            = Avg('_Review__rating__score'),
            alcohol_type          = F('category_id__name'),
            origin_country        = F('country_id__origin'),
            image_url             = F('imageurl__image_url'),
            pairing_food_category = F('productfoodpairing__foodpairing__food_category'),
                #테이블접근(테이블명의 소문자!or related_name) > 접근한 테이블의 필드명(그리고 이 필드가 foreignkey임) > 그 필드가 클래스라고 생각하고 그 필드의 필드명 
            review_counts         = Count('_Review')).order_by(*sorting)#언팩킹임. 되게 유용한 방식임 꼭기억!!!!!!!!!!!

        if search:
            if search in Category.objects.all().values_list('name',flat = True):
                products_list = products_list.filter(alcohol_type=search)
                filter = 'Category'

            if search in Country.objects.all().values_list('origin',flat = True):
                products_list = products_list.filter(origin_country=search)
                filter = 'Country'

            if search in FoodPairing.objects.all().values_list('food_category',flat = True):
                products_list = products_list.filter(pairing_food_category=search)
                filter = 'Foodpairing'
            else:
                products_list = products_list.filter(name__icontains=search)
            
            if not products_list:
                message = "no_searched_products"
                recommended_words = {
                    "Category"    : random.choice(Category.objects.all().values_list('name',flat = True)),
                    "Country"     : random.choice(Country.objects.all().values_list('origin',flat = True)),
                    "Foodpairing" : random.choice(FoodPairing.objects.all().values_list('food_category',flat = True))
                    }
                return JsonResponse({"message":message,"recommended_words":recommended_words}, status=200)

        #search가 아닐 경우
        else:
            
            # category     = request.GET.get('category')
            #get으로하면, category키로 여러개가 들어올 경우 마지막 것만 들어옴
            category     = request.GET.getlist('category')
            country      = request.GET.getlist('country')
            price        = int(request.GET.get('price',1000000))
            rating       = int(request.GET.get('rating',0))
            food_pairing = request.GET.getlist('food_pairing')



            q = Q() 
            if category:
                q &= Q(alcohol_type__in=category)
            if country:
                q &= Q(origin_country__in=country)
            if price:
                q &= Q(price__lte=price)
            if rating:
                q &= Q(avg_rating__gte=rating)
            if food_pairing:
                q &= Q(pairing_food_category=food_pairing)

            products_list = products_list.filter(q)


        #return 영역
        result = []
        for product in products_list:
            result.append({
                'id'           :product.id,
                'price'        :product.price,
                'name'         :product.name,
                'country'      :product.origin_country,
                'category'     :product.alcohol_type,
                'image_url'    :product.image_url,
                'created_at'   :product.created_at,
                'rating'       :product.avg_rating, #FIXME:float > round를 먹여야 함. 근데 정리가 안됨
                'review_counts':product.review_counts
            })#FIXME : 가장 좋아요를 많이 받은 리뷰를 가져오고 싶다.. 근데 어떻게? >values_list?


        all_page,_ = divmod(len(products_list),limit)
        result = result[page*limit-1:] if page == all_page else result[(page-1)*limit:page*limit]
                             
        #FIXME : search의 경우 Filter를 추가해야함
        return JsonResponse({"current_page":page,"all_page":all_page,"result":result}, status=200)