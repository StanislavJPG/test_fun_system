from django.contrib.auth import logout
from django.contrib.auth.models import AnonymousUser
from django.template.base import Token
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import RefreshToken


# class NoTokenFoundException(Exception):
#     ...
#
#
# class TokenMiddleware(MiddlewareMixin):
#     @staticmethod
#     def process_request(request):
#         refresh = RefreshToken.for_user(request.user)
#         request.META['HTTP_AUTHORIZATION'] = f'Bearer {str(refresh.access_token)}'


# {"username": "Stanislav", "email": "email@email", "password": "stas"}
