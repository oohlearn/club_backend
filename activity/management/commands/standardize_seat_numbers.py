from django.core.management.base import BaseCommand
from activity.models import Seat  # 替換 'your_app' 為你的實際 app 名稱
import re

class Command(BaseCommand):
    help = '將所有現有的座位號標準化為字母後跟兩位數字的格式'

    def handle(self, *args, **options):
        seats = Seat.objects.all()
        updated_count = 0

        for seat in seats:
            original_num = seat.seat_num
            if re.match(r'^[A-Z]\d+$', original_num):
                letter = original_num[0]
                number = original_num[1:].zfill(2)
                new_num = f"{letter}{number}"
                
                if new_num != original_num:
                    seat.seat_num = new_num
                    seat.save()
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f'更新座位號: {original_num} -> {new_num}'))
            else:
                self.stdout.write(self.style.WARNING(f'跳過無效的座位號: {original_num}'))

        self.stdout.write(self.style.SUCCESS(f'成功更新 {updated_count} 個座位號'))