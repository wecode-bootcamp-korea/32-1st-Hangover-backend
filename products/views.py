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
                    print(category)
                    q &= Q(category_id__name__in=category)
                    print(q)
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
                review = None
                if product.reviews.exists:
                    reviewlike_dict = {
                        review.id:review.reviewlike_set.count() for review in Review.objects.filter(product_id=product.id)
                    }
                    likemost_review_id = max(reviewlike_dict,key=reviewlike_dict.get)

                    review = Review.objects.get(id=likemost_review_id)

                    review = {
                    'id'         :review.user.id,
                    'username'   :review.user.firstname + review.user.lastname,
                    'created_at' :review.content,
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