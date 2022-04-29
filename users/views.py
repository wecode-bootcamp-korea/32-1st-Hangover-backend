import bcrypt
import jwt

from django.http            import JsonResponse
from django.views           import View

from users.models           import User
from my_settings            import ALGORITHM, SECRET_KEY
from datetime               import datetime, timedelta

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            email          = data['email']
            user           = User.objects.get(email=email)
            password = data['password']

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):

                current_time          = datetime.utcnow()
                expiration_time       = timedelta(weeks=3)
                token_expiration_time = current_time+expiration_time
                payload = {
                    'id' : user.id,
                    'exp' : datetime.utcnow() + timedelta(weeks=3)
                }
                jwt_access_token = jwt.encode(payload, SECRET_KEY, ALGORITHM)

                return JsonResponse({'messasge':'SUCCESS','JWT_TOKEN':jwt_access_token}, status=200)
            return JsonResponse({"message":"INVALID_USER"},status=401)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status=400)
        except User.DoesNotExist:
            return JsonResponse({"message":"INVALID_USER"},status=401)