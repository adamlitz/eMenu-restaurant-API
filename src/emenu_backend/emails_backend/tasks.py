# Prevent 'django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.'
import django
django.setup()

import datetime
from celery import shared_task
from django.utils import timezone
from .email_sender import send_email
from menus.models import Dish


@shared_task
def look_for_dish_updates() -> str:
    today = datetime.datetime.now(timezone.get_current_timezone())
    today.replace(hour=0)

    yesterday = today - datetime.timedelta(days=1)
    yesterday.replace(hour=0)

    dishes = Dish.objects.filter(updated__isnull=False)
    updated_dishes = []
    created_dishes = []

    msg = ""

    for dish in dishes:
        if yesterday < dish.created < today:
            created_dishes.append(dish)

        # Do not consider created dishes as updated
        if dish not in created_dishes:
            if yesterday < dish.updated < today:
                updated_dishes.append(dish)

    if len(updated_dishes) > 1 or len(created_dishes) > 1:
        send_email(
                   updated_dishes=updated_dishes,
                   created_dishes=created_dishes
                  )
        msg = f"Sending emails with updated dishes: {updated_dishes}" \
              f" and created dishes: {created_dishes}"
    else:
        msg = "No new dishes"

    return msg
