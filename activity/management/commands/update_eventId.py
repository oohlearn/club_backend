from django.core.management.base import BaseCommand
from activity.models import SeatForNumberRow  # 替換 'your_app' 為你的應用名稱

class Command(BaseCommand):
    help = '更新所有座位的event_id'

    def handle(self, *args, **options):
        seats = SeatForNumberRow.objects.all()
        updated_count = 0

        for seat in seats:
            if not seat.event_id:
                seat.event_id = seat.zone.event.id
                updated_count += 1

            seat.save()

        self.stdout.write(self.style.SUCCESS(f'成功更新了 {updated_count} 個座位'))