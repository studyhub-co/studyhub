import time

from django.core.management.base import BaseCommand
from ...models import MaterialProblemType
from studio.tasks import build_sandbox


class Command(BaseCommand):
    help = 'build all problem types'

    def handle(self, *args, **options):
        for pt in MaterialProblemType.objects.all():
            build_sandbox.delay(str(pt.uuid))
            # not good, but fastest, pause for 5 min
            time.sleep(5*60)
            # TODO: queue should be configured on the celery side

