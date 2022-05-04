import json

from django.views    import View
from django.http     import JsonResponse

from core.utils     import login_decorator
from reviews.models  import Review, ReviewLike

class ReviewView(View):

    @login_decorator
    def post(self, request):
        data       = json.loads(request.body)

        user       = request.user
        product_id = data.get('product_id')
        content    = data.get('content')
        rating     = data.get('rating')

        if not (rating or content):
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        review = Review.objects.create(
            user       = user,
            product_id = product_id,
            rating_id  = rating,
            content    = content
        )

        return JsonResponse({'message': 'SUCCESS'}, status=201)