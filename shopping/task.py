from celery import shared_task
from django.utils import timezone
from datetime import timedelta


@shared_task
def clear_expired_cart_items():
    three_days_ago = timezone.now() - timedelta(days=3)
    expired_items = CartItem.objects.filter(added_time__lt=three_days_ago)

    for item in expired_items:
        with transaction.atomic():
            product = Product.objects.select_for_update().get(id=item.product.id)
            product.pre_sold_qty -= item.quantity
            product.save()
            item.delete()
