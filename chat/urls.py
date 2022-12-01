from django.urls import path, re_path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path('login_user/', views.login_view, name='login_view'),
    path('logout_user/', views.logout_view, name='logout_view'),
    path('contacts/', views.contacts, name='contacts'),
    path('chat_room/<int:contact_id>/<int:user_id>/', views.chat_room, name='chat_room')
]