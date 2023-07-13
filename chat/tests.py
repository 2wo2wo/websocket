from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from .views import contacts, index


class ContactPageTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(
            username='jacob',
            email='jacob123@test.com',
            password='topsecret123'
        )

    def test_details(self):
        request = self.factory.get('/login_user/')
        request.user = self.user
        response = contacts(request)
        self.assertEqual(response.status_code, 200)

    def test_homepage(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        response = index(request)
        self.assertEqual(response.status_code, 200)





