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