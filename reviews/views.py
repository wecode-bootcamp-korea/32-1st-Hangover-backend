import json

from django.views    import View
from django.http     import JsonResponse

from core.utils      import login_decorator
from reviews.models  import Review, ReviewLike

class ReviewLikeView(View):
    @login_decorator
    def post(self, request):
        data      = json.loads(request.body)
        user_id   = request.user.id
        review_id = data.get('review_id', None)

        # KEY_ERROR check
        if not review_id:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        # valid review check
        if not Review.objects.filter(id=review_id).exists():
            return JsonResponse({'message': 'INVALID_REVIEW'}, status=400)
        
        review = Review.objects.get(id=review_id)

        if ReviewLike.objects.filter(user_id=user_id, review_id=review_id):
            ReviewLike.objects.filter(user_id=user_id, review_id=review_id).delete()
        
        else:
            ReviewLike.objects.create(user_id=user_id, review_id=review_id)
        
        #해당 review의 좋아요 수 구하기
        like_count = ReviewLike.objects.filter(review_id=review_id).count()
        return JsonResponse({'like_count': like_count}, status=200) 