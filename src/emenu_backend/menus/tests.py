from django.contrib.auth import get_user_model
from .models import Menu
from .views import MenuViewSet, DishViewSet
from rest_framework.test import (APITestCase,
                                 APIRequestFactory,
                                 force_authenticate)


class MenuTests(APITestCase):
    fixtures = ['menus_initial_data', 'users_initial_data']

    def test_show_empty_menus_for_registered_users(self):
        """
        Check if registered user can view menus without any dishes
        """
        factory = APIRequestFactory()

        # Get existing user from fixtures
        User = get_user_model()
        user = User.objects.get(email='bob@emenu.com')

        # Create menu without any dishes
        menu = Menu.objects.create(name="Empty menu", description="empty")
        menu.save()

        # Authenticate our test user
        request = factory.get('/menus/')
        force_authenticate(request, user=user)

        # Send request
        view = MenuViewSet.as_view({'get': 'list'})
        response = view(request)

        # Count empty menus
        count = 0

        # We should find one empty menu
        for menu in response.data:
            if len(menu['dishes']) < 1:
                count += 1
                self.assertEqual(len(menu['dishes']), 0)

        # Fail if there is no empty menus
        self.assertGreaterEqual(count, 1)

    def test_do_not_show_empty_menus_for_anonymous_users(self):
        """
        Check if anonymous user see only non-empty menus
        """
        factory = APIRequestFactory()

        # Create menu without any dishes
        menu = Menu.objects.create(name="Empty menu", description="empty")
        menu.save()

        request = factory.get('/menus/')

        # Send request
        view = MenuViewSet.as_view({'get': 'list'})
        response = view(request)

        count = 0

        # We shouldn't find any empty menu
        for menu in response.data:
            if len(menu['dishes']) < 1:
                count += 1

        # Expect that no empty menus were found
        self.assertEqual(count, 0)

    def test_do_not_show_empty_menu_details_to_anonymous_user(self):
        """
        Ensure that anonymous user can't see empty menu details
        """
        factory = APIRequestFactory()

        # Create menu without any dishes
        menu = Menu.objects.create(name="Empty menu", description="empty")
        menu.save()

        request = factory.get('/menus/Empty menu/')

        # Send request
        view = MenuViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk='Empty menu')

        self.assertEqual(response.status_code, 404)

    def test_create_menu_with_dishes_in_single_POST_request(self):
        """
        Test the overridden create() function in Menu serializer
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

        # Check if all 5 dishes are present inside a menu
        self.assertEqual(len(response.data['dishes']), 5)

    def test_check_if_menu_was_updated_after_adding_new_dish(self):
        """
        Menu 'updated' field should also update when new dish is added
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

        # Get menu data
        request = factory.get('/menus/')
        force_authenticate(request, user=user)
        view = MenuViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk='Empty menu')

        menu_update_time = response.data['updated']
        dish_update_time = dish_response.data['updated']

        # Menu update time and dish creation time should be the same
        self.assertEqual(menu_update_time, dish_update_time)

    def test_check_if_menu_was_updated_after_updating_its_dish(self):
        """
        Menu's 'updated' field should also update when its dish is updated
        """
        factory = APIRequestFactory()

        # Get existing user from fixtures
        User = get_user_model()
        user = User.objects.get(email='bob@emenu.com')

        # Change dish name from Margherita to Fungi
        request_body = {
                        'name': 'Fungi',
                        'description': 'update field',
                        'menu': 'Italian Menu'
                       }
        update_dish_request = factory.put('/dishes/7/', request_body, format='json')
        dish_view = DishViewSet.as_view({'put': 'update'})

        force_authenticate(update_dish_request, user=user)
        dish_response = dish_view(update_dish_request, pk=7)

        # Get existing menu from fixtures
        request = factory.get('/menus/')
        force_authenticate(request, user=user)
        view = MenuViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk='Italian Menu')

        menu_update_time = response.data['updated']
        dish_update_time = dish_response.data['updated']

        # Menu update time and dish creation time should be the same
        self.assertEqual(menu_update_time, dish_update_time)
