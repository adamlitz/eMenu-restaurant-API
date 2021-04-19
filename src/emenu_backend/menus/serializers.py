from rest_framework import serializers
from .models import Menu, Dish


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'

    def create(self, validated_data):
        """
        Override create function to update menu when its dish is created
        """
        menu_data = validated_data.pop('menu')
        dish = Dish.objects.create(menu=menu_data, **validated_data)

        # Force related menu to update
        menu_data.save()

        return dish

    def update(self, instance, validated_data):
        """
        Override update function to update menu when its dish is updated
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Force related menu to update
        instance.menu.save()

        return instance


class DishMenuSerializer(serializers.ModelSerializer):
    """
    Serializer used inside MenuViewSet to show all dishes
    related to a given menu without unnecessary information
    """
    class Meta:
        model = Dish
        fields = ['name']


class PartialDishInfoSerializer(serializers.ModelSerializer):
    """
    Serializer used in public API to show dishes details related to a given menu
    """
    class Meta:
        model = Dish
        fields = ['name', 'description', 'is_vegetarian', 'image', 'menu', 'price']


class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer for a preview of dishes from the MenuView level
    """
    dishes = DishMenuSerializer(many=True, required=False)

    class Meta:
        model = Menu
        fields = ['name', 'dishes', 'description', 'image']

    def create(self, validated_data):
        """
        Allow to add and create dishes at menu creation
        """
        # Check if user wants to add new dish at the menu creation
        # If not, return new menu without dishes
        try:
            dishes_data = validated_data.pop('dishes')
        except KeyError:
            menu = Menu.objects.create(**validated_data)
            return menu

        menu = Menu.objects.create(**validated_data)

        for dish_data in dishes_data:
            Dish.objects.create(menu=menu, **dish_data)

        return menu


class FullMenuInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for a FullMenuViewSet
    Includes all information about menu itself and all corresponding dishes
    """
    dishes = DishSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = '__all__'


class PartialMenuInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for a MenuViewSet for public API users
    Includes partial information about menu itself and all corresponding dishes
    """
    dishes = PartialDishInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ['name', 'dishes', 'description', 'created', 'updated']
