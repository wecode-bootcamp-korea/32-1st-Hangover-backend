from django.db       import models
from core.models     import TimeStampedModel
from users.models    import User
from products.models import Product

class Review(TimeStampedModel):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='reviews')
    rating  = models.ForeignKey('Rating', on_delete=models.CASCADE)
    content = models.TextField(null=True)

    class Meta:
        db_table = 'reviews'

class Comment(TimeStampedModel):
    review  = models.ForeignKey('Review', on_delete=models.CASCADE)
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    
    class Meta:
        db_table = 'comments'

class ReviewLike(TimeStampedModel):
    review = models.ForeignKey('Review', on_delete=models.CASCADE)
    user   = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'review_likes'
        
        constraints = [
            models.UniqueConstraint(
                fields=["user", "review"],
                name="unique_review",
            ),
        ]

class Rating(models.Model):
    score = models.DecimalField(max_digits=2, decimal_places=1)

    class Meta:
        db_table = 'ratings'