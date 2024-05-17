from django.urls import path

from .views import RegisterView, LoginView, PrivateView, LogoutView, AllUsersView, UserView

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register-view'),
    path('api/login/', LoginView.as_view(), name='login-view'),
    path('protected/', PrivateView.as_view(), name='private-view'),
    path('api/logout/', LogoutView.as_view(), name='logout-view'),
    path('users/all/', AllUsersView.as_view(), name='all_users_view'),
    path('users/<int:user_id>/', UserView.as_view(), name='user_view'),
]
