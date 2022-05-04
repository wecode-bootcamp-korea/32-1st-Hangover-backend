import json

from django.views import View
from django.http  import JsonResponse

from core.utils     import login_decorator
from reviews.models import Review

class ReviewView(View):
    @login_decorator
    def post(self, request):
        try:
            data       = json.loads(request.body)

            user       = request.user
            product_id = data['product_id']
            content    = data['content']
            rating     = data['rating']

            review = Review.objects.create(
                user       = user,
                product_id = product_id,
                rating_id  = rating,
                content    = content
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    def get(self, request):
        try:
            product_id = request.GET.get('product_id')
            reviews = Review.objects.filter(id=product_id)

            review_list = [{
                "firstname"  : review.user.firstname,
                "lastname"   : review.user.lastname,
                "user_id"    : review.user.id,
                "content"    : review.content,
                "rating"     : review.rating.score,
                "created_at" : review.created_at,
                "review_id"  : review.id
            } for review in reviews]
            return JsonResponse({'Reviews':review_list}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    @login_decorator
    def patch(self, request): 
        try:
            data = json.loads(request.body)
            user = request.user

            review_id = data['review_id']

            review = Review.objects.get(id = review_id)

            if review.user != request.user:
                return JsonResponse({'message': 'INVALID_USER'}, status=401)

            review.content = data.get('content', review.content)
            review.save()
            return JsonResponse({'message': 'SUCCESS'}, status=204)

        except Review.DoesNotExist:
            return JsonResponse({"message" : "INVALID_REVIEW"}, status=401)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    @login_decorator
    def delete(self, request):
        try:
            review_id = request.GET.get('review_id')

            review = Review.objects.get(id = review_id)

            if request.user.id != review.user.id:
                return JsonResponse({'message': 'INVALID_USER'}, status=401)
                
            review.delete()
            return JsonResponse({"message": "Review was deleted"}, status = 204)
        
        except Review.DoesNotExist:
            return JsonResponse({"message" : "INVALID_REVIEW"}, status=401)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)