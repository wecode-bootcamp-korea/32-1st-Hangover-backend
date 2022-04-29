import bcrypt
import jwt

from datetime               import datetime, timedelta
from django.http            import JsonResponse
from django.views           import View
from users.models           import User
from my_settings            import ALGORITHM, SECRET_KEY

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            email          = data['email']
            user           = User.objects.get(email=email)
            user_saved_pwd = user.password
            password       = data['password']

            if not bcrypt.checkpw(password.encode('utf-8'), user_saved_pwd.encode('utf-8')):

                current_time          = datetime.utcnow()
                expiration_time       = timedelta(weeks=3)
                token_expiration_time = current_time+expiration_time
                jwt_access_token      = jwt.encode({'id':user.id, 'exp':token_expiration_time}, SECRET_KEY, ALGORITHM)

                return JsonResponse({'messasge':'SUCCESS','JWT_TOKEN':jwt_access_token}, status=200)
            return JsonResponse({"message":"INCORRECT_PASSWORD"},status=401)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status=400)
        except User.DoesNotExist:
            return JsonResponse({"message":"NOT_REGISTERED_EMAIL"},status=401)