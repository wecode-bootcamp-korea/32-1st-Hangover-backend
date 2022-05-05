import random

from django.db.models import Avg, Count,Q,Max
from django.http      import JsonResponse
from django.views     import View

from products.models  import Product, Category, Country, FoodPairing
from reviews.models   import Review

class ProductSearchView(View):
    """
    1. 검색어가 필터의 카테고리에 포함될 경우, 해당 카테고리에 속한 상품 리스트를 반환 
    2. 검색어가 상품명에 포함되는 상품 리스트를 반환 
    3. 일치되는 상품이 없을 경우, 추천검색어를 반환
    """
    def get(self,request):

        search = request.GET.get('search')
        limit  = int(request.GET.get('limit',10))
        print(search)
        print(type(search))
        keyword_list = {
            "Category"    : Category.objects.all().values_list('name',flat = True),
            "Country"     : Country.objects.all().values_list('origin',flat = True),
            "Foodpairing" : FoodPairing.objects.all().values_list('food_category',flat = True),
        }

        filter_dict = {}

        for key,values in keyword_list.items():
            for word in values:
                if search in word:
                    filter_dict['filter'] = key
                    matched_keyword = word
        products_list = Product.objects.all().annotate(avg_rating= Avg('reviews__rating__score')).order_by('-avg_rating')
        filter = filter_dict.get('filter')
        
        if filter:
            Q_filter = {
                'Category'        : Q(category_id__name=matched_keyword),
                'Country'         : Q(country_id__origin=matched_keyword),
                'Foodpairing'     : Q(productfoodpairing__foodpairing__food_category=matched_keyword),
            }
            products_list = products_list.filter(Q_filter[filter])

        else:
            products_list          = products_list.filter(name__icontains=search)
            filter,matched_keyword = None,None

        if products_list.exists():
            result = [{
                'id'           :product.id,
                'price'        :product.price,
                'name'         :product.name,
                'country'      :product.country.origin,
                'category'     :product.category.name,
                'image_url'    :product.imageurl_set.first().image_url,
                'created_at'   :product.created_at,
                'rating'       :product.avg_rating, 
                } for product in products_list.order_by("?")[:limit]]

            return JsonResponse({"filter":filter,"matched_keyword":matched_keyword,"result":result}, status=200)

        else:
            message = "no_searched_products"
            recommended_words = {
                "Category"    : Category.objects.all().values_list('name', flat = True).order_by('?').first(),
                "Country"     : Country.objects.all().values_list('origin', flat = True).order_by('?').first(),
                "Foodpairing" : FoodPairing.objects.all().values_list('food_category', flat = True).first()
                }
            return JsonResponse({"response":[message,recommended_words]}, status=200)


class ProductListView(View):
    def get(self,request):

        """
        ProductListView-GET : 조건에 맞는 상품 리스트를 반환

        -Pagination
            page  : 현재 페이지. default = 1
            limit : 페이지당 상품의 개수를 반환 default = 20

        -필터KEY
            rating       : 입력된 평점. 평점이상의 상품을 반환. default = 0
            price        : 입력된 가격. 가격이상의 상품을 반환. default = 1000000
            category     : 주종 ex) wine, whisky 
            country      : 원산지가 되는 국가 ex)korean
            food_pairing : 잘 어울리는 음식 ex) korean, western
            sorting      : 정렬방식. 기본 정렬은 높은 평점순 > 높은 가격순

        -정렬 방식으로 넣어줄 수 있는 값
            sorting_dict = {
                    "high_price"    : 높은 가격 순
                    "low_price"     : 낮은 가격 순
                    "high_rating"   : 높은 평점 순
                    "low_rating"    : 낮은 평점 순
                    "many_review"   : 많은 리뷰 순
                    "little_review" : 적은 리뷰 순
                    "random"        : 랜덤정렬
                }

        -반환되는 상품리스트에 포함된 정보
            'id'           :product.id,
            'price'        :product.price,
            'name'         :product.name,
            'country'      :product.country.origin,
            'category'     :product.category.name,
            'image_url'    :product.imageurl_set.first().image_url,
            'created_at'   :product.created_at,
            'rating'       :product.avg_rating, 
            'review'       :review
        *리뷰의 경우, 좋아요를 두개이상 받은 리뷰들 중에서 좋아요를 가장 많이 받은 리뷰정보를 반환
        """
        
        try:
            page         = int(request.GET.get('page',1))
            limit        = int(request.GET.get('limit',20))
            category     = request.GET.getlist('category')
            country      = request.GET.getlist('country')
            price        = int(request.GET.get('price',"100 만원이하")[:-5])*10000
            rating       = int(request.GET.get('rating',0))
            food_pairing = request.GET.getlist('food_pairing')
            sorting      = request.GET.get('sorting','high_rating')

            sorting_dict = {
                "high_price"    : "-price",
                "low_price"     : "price", 
                "high_rating"   : "-avg_rating",
                "low_rating"    : "avg_rating",
                "many_review"   : "-review_counts",
                "little_review" : "review_counts",
                "random"        : "random",
            }
            sorting = sorting_dict.get(sorting)
            
            products_list = Product.objects\
            .annotate(avg_rating    = Avg('reviews__rating__score'))\
            .annotate(review_counts = Count('reviews'))

            if sorting == "random":
                max_id = products_list.aggregate(max_id = Max('id'))['max_id']
                picked_product_id_list = []
                while len(picked_product_id_list) < 12:
                    pk=random.randint(1,max_id)
                    if pk not in picked_product_id_list and Product.objects.filter(id=pk).exists():
                        picked_product_id_list.append(pk)
                products_list=products_list.filter(id__in=picked_product_id_list)
                sorting = '-avg_rating'
                
            else:
                q = Q() 
                if category:
                    q &= Q(category_id__name__in=category)
                if country:
                    q &= Q(country_id__origin__in=country)
                if price:
                    q &= Q(price__lte=price)
                if rating:
                    q &= Q(avg_rating__gte=rating)
                if food_pairing:
                    q &= Q(productfoodpairing__foodpairing__food_category__in=food_pairing)

                products_list = products_list.filter(q)

            sorting = ['-avg_rating','-price'] if sorting[-6:] == "rating" else [sorting,'-avg_rating']
            products_list = products_list.order_by(*sorting)
            
            
            result = []
            for product in products_list[(page-1)*limit:page*limit]:
                if product.reviews.exists:
                    reviewlike_dict = {
                        review.id:review.reviewlike_set.count() for review in Review.objects.filter(product_id=product.id)
                    }

                    if max(reviewlike_dict.values()) < 2:
                        review = None
                    else:
                        likemost_review_id = max(reviewlike_dict,key=reviewlike_dict.get)
                        review = Review.objects.get(id=likemost_review_id)

                        review = {
                        'id'         :review.user.id,
                        'username'   :review.user.firstname + review.user.lastname,
                        'created_at' :review.created_at,
                        'content'    :review.content,
                        'rating'     :review.rating.score
                }
                
                result.append({
                'id'           :product.id,
                'price'        :product.price,
                'name'         :product.name,
                'country'      :product.country.origin,
                'category'     :product.category.name,
                'image_url'    :product.imageurl_set.first().image_url,
                'created_at'   :product.created_at,
                'rating'       :product.avg_rating, 
                'review'       :review
            })

            return JsonResponse({"result":result}, status=200)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)


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