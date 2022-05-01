from products.models  import Product, ImageUrl, Category, Country, FoodPairing ,ProductFoodPairing
from django.db.models import Avg, Count,Q,F

from django.http            import JsonResponse
from django.views           import View

import random

# Create your views here.
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
        products_list = products_list.annotate(
            avg_rating=Avg('_Review__rating__score'),
            alcohol_type=F('category_id__name'),
            origin_country=F('country_id__origin'),
            image_url=F('imageurl__image_url'),
            pairing_food=F('imageurl__image_url'),
            review_counts=Count('_Review')).order_by(*sorting)#언팩킹임. 되게 유용한 방식임 꼭기억!!!!!!!!!!!

        if search:
            #분기를 이렇게 만드는 수 밖에 없나? Q객체를 쓸 수는 없을까? search를 따로 떨어뜨려서 사용할 거라면 차라리 searchview를 만드는 게 낫지 않나?? 중복되는 기능 자체가 없는데?
            #더 좋은 방법이 있을까???? values_list를 쓰자 > 썻음
            if search in Category.objects.all().values_list('name',flat = True):
                products_list = Product.objects.all().filter(category__name=search)
                filter = 'Category'

            if search in Country.objects.all().values_list('origin',flat = True):
                products_list = Product.objects.all().filter(country__origin=search)
                filter = 'Country'

            if search in FoodPairing.objects.all().values_list('food_category',flat = True):
                products_list = Product.objects.all().filter(productfoodpairing__foodpairing__food_category=search)
                filter = 'Foodpairing'
                #테이블접근(테이블명의 소문자!) > 접근한 테이블의 필드명(그리고 이 필드가 foreignkey임) > 그 필드가 클래스라고 생각하고 그 필드의 필드명 
                #더 좋은 방법이 있을 거야 > related , prelatefetch?
            else:
                products_list = Product.objects.filter(name__icontains=search)
            
            #search에 잡히는 단어가 없을 경우? > 상품이없다는 메세지 +카테고리들 사이에서 랜덤으로 고른 추천검색어를 같이 줌
            if not products_list:
                message = "no_searched_products"
                recommended_words = {
                    "Category":random.choice(Category.objects.all().values_list('name',flat = True)),
                    "Country":random.choice(Country.objects.all().values_list('origin',flat = True)),
                    "Foodpairing":random.choice(FoodPairing.objects.all().values_list('food_category',flat = True))}

                return JsonResponse({"message":message,"recommended_words":recommended_words}, status=200)

        #search가 아닐 경우
        else:
            
            category     = request.GET.get('category')
            category2     = request.GET.getlist('category')
            print("1:",category)
            print("1:",category2)
            price        = request.GET.get('price',[0,1000000])
            rating       = request.GET.get('rating',0)
            country      = request.GET.get('country')
            food_pairing = request.GET.get('food_pairing')

            return JsonResponse({"test":"hi"}, status=200)
            # q = Q() #모든 filter
            # if category:
            #     Q &= Q(alcohol_type=category)
            # if category:
            #     Q &= Q(alcohol_type=category)
            # if country:
            #     Q &= Q(origin_country=country)
            # if food_pairing:
            #     Q &= Q(alcohol_type=food_pairing)



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
            })#FIXME : 가장 좋아요를 많이 받은 리뷰를 가져오고 싶다.. 근데 어떻게?


        all_page,_ = divmod(len(products_list),limit)
        result = result[page*limit-1:] if page == all_page else result[(page-1)*limit:page*limit]
                             
        #FIXME : search의 경우 Filter를 추가해야함
        return JsonResponse({"current_page":page,"all_page":all_page,"result":result}, status=200)