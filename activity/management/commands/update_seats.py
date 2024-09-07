from django.core.management.base import BaseCommand
from activity.models import SeatForNumberRow  # 替換 'your_app' 為你的應用名稱

class Command(BaseCommand):
    help = '更新所有座位的顏色和價格'

    def handle(self, *args, **options):
        seats = SeatForNumberRow.objects.all()
        updated_count = 0

        for seat in seats:
            # 檢查並更新顏色
            if not seat.color:
                seat.color = seat.zone.color
                updated_count += 1

            # 檢查並更新價格
            if seat.price is 0:
                seat.price = seat.zone.price
                updated_count += 1

            if not seat.area:
                seat.area = seat.zone.area
                updated_count += 1

            seat.save()

        self.stdout.write(self.style.SUCCESS(f'成功更新了 {updated_count} 個座位'))