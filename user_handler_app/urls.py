from django.urls import path
from . import views

urlpatterns = [
    path('user_detail/', views.UserInfoApiView.as_view(), name='user_info')
]
