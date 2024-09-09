from django.core.management.base import BaseCommand
from activity.models import Zone

class Command(BaseCommand):
    help = 'Updates the remain field for all ZoneForNumberRow instances to match the number of related seats'

    def handle(self, *args, **kwargs):
        zones = Zone.objects.all()
        for zone in zones:
            zone.remain = zone.seat.count()  # 根据 seat 的数量更新 remain
            zone.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated remain for zone: {zone.name}'))
