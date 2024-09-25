from django.core.management.base import BaseCommand
from activity.models import Seat


class Command(BaseCommand):
    help = '將所有 Seat 的 status 欄位更新為 "on_sell"'

    def handle(self, *args, **kwargs):
        # 將所有 Seat 的 status 欄位更新為 'on_sell'
        seats_updated = Seat.objects.update(status='on_sell')

        # 打印更新的座位數量
        self.stdout.write(self.style.SUCCESS(f'成功更新 {seats_updated} 個座位的狀態為 "on_sell"'))
