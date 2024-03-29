from django.urls import path,  include, re_path

from django.views.generic import RedirectView

from . import views, views_api

from .oauth_social import GoogleLogin
from .swagger import swagger_urls

from user_handler_app import urls

url_apis = [
    path('user_contacts/', views_api.ContactApi.as_view(), name='contact_api'),
    path('search_user/', views_api.ContactSearchApi.as_view(), name='search_user'),
    path('user_add/', views_api.AddUserContactApi.as_view(), name='user_add'),
    path('social_auth/google', GoogleLogin.as_view(), name='google_authentication'),
    path('registration/', views_api.RegistrationAPIView.as_view()),
    path('verification/', views_api.EmailVerificationAPIView.as_view()),
    path('', include(swagger_urls)),
    path('', include(urls.urlpatterns)),
    path('username_reset/', views_api.UsernameIconAPIView.as_view(), name='username-reset'),
    path('chat_room/<int:contact_id>/', views_api.GetUniqueRoomAPIView.as_view(), name='chat_room'),
    path('history/', views_api.UserMessagesHistory.as_view(), name='history'),
    path('contact/<int:contact_id>/', views_api.MessageBetweenUsers.as_view(), name='chat_contact')
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

    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
    path('api/v1/', include(url_apis))
]
