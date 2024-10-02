from django.urls import path
from .views import CreateUserView, UserProfileView

app_name = 'user_service'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]
