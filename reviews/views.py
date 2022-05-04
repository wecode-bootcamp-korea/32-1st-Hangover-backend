import json

from django.views import View
from django.http  import JsonResponse

from core.utils     import login_decorator
from reviews.models import Review

class ReviewView(View):
    @login_decorator
    def delete(self, request):
        try:
            review_id = request.GET.get('review_id')

            review = Review.objects.get(id = review_id)

            if not request.user.id == review.user.id:
                return JsonResponse({"message": "FORBIDDEN"}, status = 403)
                
            review.delete()
            return JsonResponse({"message": "Review was deleted"}, status = 204)
        
        except Review.DoesNotExist:
            return JsonResponse({"message" : "INVALID_REVIEW"}, status=401)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)