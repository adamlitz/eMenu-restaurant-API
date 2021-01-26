from django.contrib import admin
from .models import Menu, Dish


class MenuAdmin(admin.ModelAdmin):
    pass


class DishAdmin(admin.ModelAdmin):
    pass


admin.site.register(Menu, MenuAdmin)
admin.site.register(Dish, DishAdmin)
