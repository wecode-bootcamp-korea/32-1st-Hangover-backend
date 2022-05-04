import bcrypt, jwt
import json
from json.decoder           import JSONDecodeError

from django.http            import JsonResponse
from django.core.exceptions import ValidationError
from django.views           import View

from my_settings            import ALGORITHM, SECRET_KEY
from datetime               import datetime, timedelta

from core.utils             import login_decorator
from users.validation       import validate_email, existing_email, validate_password
from users.models           import User, Cart
from products.models        import Product

class CartView(View):

    @login_decorator
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user       = request.user
            product_id = data['product_id']
            count      = data['count']

            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'message': 'PRODUCT_DOES_NOT_EXIST'}, status=400)
            
            if Cart.objects.filter(user_id=user.id).exists():
                cart = Cart.objects.get(user_id=user.id)
            else:
                cart = Cart.objects.create(user_id=user.id)
            
            cart, created = Cart.objects.get_or_create(
                user_id    = user.id,
                product_id = product_id,
                count      = count
            )
            if not created:
                cart.save()

            return JsonResponse({'message': 'SUCCESS'}, status=201) 
        
        except Cart.DoesNotExist:
            return JsonResponse({'message': 'CART_DOES_NOT_EXIST'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)