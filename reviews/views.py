import json

from django.views    import View
from django.http     import JsonResponse

from core.utils     import login_decorator
from reviews.models  import Review, ReviewLike

class ReviewView(View):
    def get(self, request):
        data = json.loads(request.body)

        product_id = data.get('product_id')
        reviews = Review.objects.filter(id=product_id).all()

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