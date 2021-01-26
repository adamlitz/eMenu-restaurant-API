from .tasks import look_for_dish_updates
from .email_sender import send_email
from django.contrib.auth import get_user_model
from menus.models import Menu, Dish
from menus.views import MenuViewSet, DishViewSet
from rest_framework.test import (APITestCase,
                                 APIRequestFactory,
                                 force_authenticate)


class EmailTest(APITestCase):
    fixtures = ['menus_initial_data', 'users_initial_data']

    def test_look_for_dish_updates(self):
        """
        Test detecting update/creation of dish
        """
        factory = APIRequestFactory()

        # Get existing user from fixtures
        User = get_user_model()
        user = User.objects.get(email='bob@emenu.com')

        # Create some dishes
        dishes = [
            {'name': 'dish_1', 'description': 'dish_1'},
            {'name': 'dish_2', 'description': 'dish_2'},
            {'name': 'dish_3', 'description': 'dish_3'},
            {'name': 'dish_4', 'description': 'dish_4'},
            {'name': 'dish_5', 'description': 'dish_5'}
        ]

        request_body = {
            'name': 'Menu with dishes',
            'description': 'test',
            'dishes': dishes
        }

        # Create menu with dishes
        request = factory.post('/menus/', request_body, format='json')

        view = MenuViewSet.as_view({'post': 'create'})
        force_authenticate(request, user=user)
        response = view(request)

        self.assertNotEqual(look_for_dish_updates(), 'No new dishes')

    def test_send_email(self):
        """
        Test email sending
        """
        factory = APIRequestFactory()

        # Get existing user from fixtures
        User = get_user_model()
        user = User.objects.get(email='bob@emenu.com')

        # Create menu without any dishes
        menu = Menu.objects.create(name="Empty menu", description="empty")
        menu.save()

        request_body = {
            'name': 'Test dish',
            'description': 'test',
            'menu': 'Empty menu'
        }

        # Create dish
        create_dish_request = factory.post('/dishes/', request_body, format='json')
        dish_view = DishViewSet.as_view({'post': 'create'})
        force_authenticate(create_dish_request, user=user)
        dish_response = dish_view(create_dish_request)

        # Get menu with dishes
        request = factory.get('/menus/')
        force_authenticate(request, user=user)
        view = MenuViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk='Empty menu')

        dish = Dish.objects.get(name='Test dish')

        self.assertEqual(send_email(updated_dishes=[dish],
                                    created_dishes=[dish]),
                         'Emails have been sent')
