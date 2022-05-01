import json, bcrypt

from django.core.exceptions import ValidationError
from django.http            import HttpResponse
from django.views           import View

from users.validation import validate_email, existing_email, validate_password
from users.models     import User

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            email     = data['email']
            firstname = data['firstname']
            lastname  = data['lastname']
            password  = data['password']

            validate_email(email)
            existing_email(email)
            validate_password(password)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_password = hashed_password.decode('utf-8')

            User.object.create(
                email     = email,
                firstname = firstname,
                lastname  = lastname,
                password  = decoded_hashed_password,
            )
            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ValidationError as error:
            return JsonResponse({'message' : error.message}, status=error.code)