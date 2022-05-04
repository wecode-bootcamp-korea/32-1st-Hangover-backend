import json

from django.views import View
from django.http  import JsonResponse

from core.utils     import login_decorator
from reviews.models import Review

class ReviewView(View):
    @login_decorator
    def delete(self, request):
        try:
            data = json.loads(request.body)
            review_id = data['review_id']

            review = Review.objects.get(
                id = review_id
            )
            if request.user.id == review.user.id:
                review.delete()

            return JsonResponse({"message": "Review was deleted"}, status = 200)
        
        except Review.DoesNotExist:
            return JsonResponse({"message" : "INVALID_REVIEW"}, status=401)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)