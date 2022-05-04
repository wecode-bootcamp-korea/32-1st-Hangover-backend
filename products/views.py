import random

from django.db.models import Avg, Count,Q,F,Max
from django.http      import JsonResponse
from django.views     import View

from products.models  import Product, ImageUrl, Category, Country, FoodPairing ,ProductFoodPairing
from reviews.models   import Review

class ProductListView(View):
    def get(self,request):
        
        try:
            page         = int(request.GET.get('page',1))
            limit        = int(request.GET.get('limit',12))
            category     = request.GET.getlist('category')
            country      = request.GET.getlist('country')
            price        = int(request.GET.get('price',"100 만원이하")[:-5])*10000
            rating       = int(request.GET.get('rating',0))
            food_pairing = request.GET.getlist('food_pairing')
            sorting      = request.GET.get('sorting','high_rating')

            sorting_dict = {
                "high_price"    : "-price", #높은 가격부터(내림차순)
                "low_price"     : "price", 
                "high_rating"   : "-avg_rating", #높은 점수부터(내림차순)
                "low_rating"    : "avg_rating",
                "many_review"   : "-review_counts", #리뷰가 많은 것 부터
                "little_review" : "review_counts",
                "random"        : "?", #랜덤방식추출(무작위 추출)
            }
       
            q = Q() 
            
            if category:
                q &= Q(category__name__in=category)
            
            if country:
                q &= Q(country__origin__in=country)
            
            if price:
                q &= Q(price__lte=price)
            
            if rating:
                q &= Q(avg_rating__gte=rating)
            
            if food_pairing:
                q &= Q(productfoodpairing__foodpairing__food_category__in=food_pairing)

            
            products_list = Product.objects\
                 .annotate(avg_rating=Avg('reviews__rating__score'))\
                 .annotate(review_counts=Count('reviews'))\
                 .filter(q)\
                 .order_by(sorting_dict[sorting])


            # sorting = ['-avg_rating','-price'] if sorting == "-avg_rating" else [sorting,'-avg_rating']
            ####return####
            result      = []
            total_count = products_list.count()
            
            for product in products_list[(page-1)*limit:page*limit]:
                review = None
                
                if product.reviews.exists():
                    reviewlike_dict = {
                        review.id : review.reviewlike_set.count() 
                        for review in product.reviews.all()
                    }
                    likemost_review_id = max(reviewlike_dict,key=reviewlike_dict.get)

                    review = Review.objects.get(id=likemost_review_id)

                result.append({
                    'id'           :product.id,
                    'price'        :product.price,
                    'name'         :product.name,
                    'country'      :product.country.origin,
                    'category'     :product.category.name,
                    'image_url'    :product.imageurl_set.first().image_url,
                    'created_at'   :product.created_at,
                    'rating'       :product.avg_rating, 
                    'review'       :{
                        'id'         :review.user.id,
                        'username'   :review.user.firstname + review.user.lastname,
                        'created_at' :review.content,
                        'rating'     :review.rating.score
                    } if not review else None
                })
            return JsonResponse({"total_count":total_count,"result":result}, status=200)

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