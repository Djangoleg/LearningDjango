from django.test import TestCase
from django.test.client import Client

from geekshop import settings
from users.models import User
from django.core.management import call_command


class TestUserManagement(TestCase):
    status_code_success = 200
    status_code_redirect = 302

    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

        self.superuser = User.objects.create_superuser('django2', 'django2@geekshop.local', 'GeekBrains122@')

        self.user_with__first_name = User.objects.create_user('tarantino', 'tarantino@geekshop.local', 'GeekBrains122@',
                                             first_name='Квентин')

        # self.user_with__first_name = User.objects.create_user('umaturman', 'umaturman@geekshop.local', 'geekbrains',
        #                                                       first_name='Ума')

    def test_user_login(self):
        # главная без логина
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['title'], 'GeekShop')
        self.assertNotContains(response, 'Пользователь', status_code=self.status_code_success)
        # self.assertNotIn('Пользователь', response.content.decode())

        # данные пользователя
        self.client.login(username='tarantino', password='GeekBrains122@')

        # логинимся
        response = self.client.get('/users/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user_with__first_name)
        self.assertEqual(response.status_code, self.status_code_success)

        # главная после логина
        response = self.client.get('/')
        self.assertContains(response, self.user_with__first_name.username, status_code=self.status_code_success)
        self.assertEqual(response.context['user'], self.user_with__first_name)
        # self.assertIn('Пользователь', response.content.decode())

    def test_user_register(self):
        # логин без данных пользователя
        response = self.client.get('/users/register/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'Geekshop - Регистрация')
        self.assertTrue(response.context['user'].is_anonymous)

        new_user_data = {
            'username': 'samuel',
            'first_name': 'Сэмюэл',
            'last_name': 'Джексон',
            'password1': 'geekBrains12@',
            'password2': 'geekBrains12@',
            'email': 'sumuel@geekshop.local',
            'age': '21'}

        response = self.client.post('/users/register/', data=new_user_data)
        self.assertEqual(response.status_code, self.status_code_redirect)
        # ==================================================================
        new_user = User.objects.get(username=new_user_data['username'])

        activation_url = f"{settings.DOMAIN_NAME}/users/verify/{new_user_data['email']}/{new_user.activation_key}/"

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, self.status_code_success)

        # данные нового пользователя
        self.client.login(username=new_user_data['username'], password=new_user_data['password1'])

        # логинимся
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, self.status_code_success)
        self.assertFalse(response.context['user'].is_anonymous)

        # проверяем главную страницу
        response = self.client.get('/')
        self.assertContains(response, text=new_user_data['username'], status_code=self.status_code_success)

    def tearDown(self):
        call_command('sqlsequencereset', 'products', 'users', 'orders', 'baskets')
