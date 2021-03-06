from django.db import models
from datetime import timedelta


class Menu(models.Model):
    name = models.CharField(max_length=150, primary_key=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Dish(models.Model):
    """
    Model representing a dish
    Single dish must have it's own menu
    """
    name = models.CharField(max_length=150)
    menu = models.ForeignKey(Menu, related_name='dishes', on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    preparation_time = models.DurationField(null=False, default=timedelta(minutes=0))
    is_vegetarian = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='dishes-images/', default='dish.jpg', blank=True)

    def __str__(self):
        return self.name
