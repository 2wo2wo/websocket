from django.urls import path, re_path, include

from . import views, views_api

url_apis = [
    path('user_contacts/', views_api.ContactApi.as_view()),
    path('api-auth/', include('rest_framework.urls')),
]


urlpatterns = [
    path("", views.index, name="index"),
    path('login_user/', views.login_view, name='login_view'),
    path('logout_user/', views.logout_view, name='logout_view'),
    path('contacts/', views.contacts, name='contacts'),
    path('chat_room/<int:contact_id>/<int:user_id>/', views.chat_room, name='chat_room'),
    path('registration/', views.register, name='registration'),
    path('contact-add/', views.contact_add, name='contact_add'),
    path('accounts/', include('allauth.urls')),
    path('searchbar/', views.contact_add_page, name="searchbar"),
    path('add_friend/<int:user_id>/', views.friend_add_function, name="add_friend"),
    path('api/v1/', include(url_apis))
]
