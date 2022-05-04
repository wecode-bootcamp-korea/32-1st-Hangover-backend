import json

from django.views    import View
from django.http     import JsonResponse

from core.utils      import login_decorator
from reviews.models  import Review

class ReviewView(View):
    @login_decorator
    def patch(self, request): 
        data = json.loads(request.body)
        user = request.user

        review_id = data['review_id']

        review = Review.objects.get(
            id = review_id
            )

        if review.user != request.user:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)

        review.content = data.get('content', review.content)
        review.save()

        return JsonResponse({'message': 'SUCCESS'}, status=204)