import httpx
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken


from users_actions.models import Address
from users_actions.serializers import UserSerializer

User = get_user_model()


def create_jwt_pair_for_user(user: User):
    refresh = RefreshToken.for_user(user)
    tokens = {"access": str(refresh.access_token), "refresh": str(refresh)}

    return tokens


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        user = User.objects.create_user(username=username, email=email, password=password)
        tokens = create_jwt_pair_for_user(user)
        authenticate(email=email, password=password)

        response = {"message": "Login Successful", "tokens": tokens}
        return Response(data=response, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            response = {"message": "Login Successful", "tokens": tokens}
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid email or password"})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return JsonResponse({'status': 200})


class PrivateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        refresh = RefreshToken.for_user(request.user)
        return JsonResponse({"access": str(refresh.access_token),
                             'status': 200,
                             'user': request.user.username})


class AllUsersView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        elif self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get(self, request):
        all_users_from_db = User.objects.select_related('address').order_by('id').all()
        if all_users_from_db.count() < 5:
            with httpx.Client() as client:
                response = client.get('https://jsonplaceholder.typicode.com/users')
                return JsonResponse(response.json(), safe=False)

        users_serializer = UserSerializer(all_users_from_db, many=True)
        return JsonResponse(users_serializer.data, safe=False)

    def post(self, request):
        with httpx.Client() as client:
            response = client.get('https://jsonplaceholder.typicode.com/users')
        try:
            for row in response.json():
                address = row['address']
                addresses = Address.objects.create(street=address['street'], suite=address['suite'],
                                                   city=address['city'], zipcode=address['zipcode'])
                User.objects.create(name=row['name'], username=row['username'], email=row['email'],
                                    phone=row['phone'], website=row['website'], address=addresses)
            return JsonResponse({'status': status.HTTP_200_OK})
        except IntegrityError:
            return JsonResponse({'status': status.HTTP_409_CONFLICT})


class UserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id: int):
        try:
            user = User.objects.select_related('address').get(pk=user_id)
            user_serializer = UserSerializer(user)
            return JsonResponse(user_serializer.data, safe=False)
        except ObjectDoesNotExist:
            res = serializers.ValidationError({'message': 'User does not exist'})
            res.status_code = status.HTTP_404_NOT_FOUND
            raise res

    def delete(self, request, user_id: int):
        try:
            User.objects.get(pk=user_id).delete()
            return JsonResponse({'status': status.HTTP_200_OK})
        except ObjectDoesNotExist:
            res = serializers.ValidationError({'message': 'User does not exist'})
            res.status_code = status.HTTP_404_NOT_FOUND
            raise res
