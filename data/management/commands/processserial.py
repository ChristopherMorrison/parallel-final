import os
from timeit import default_timer as timer

from django.core.management.base import BaseCommand, CommandError
from data.models import BinaryFile


class Command(BaseCommand):
    help = 'Process all samples serially'

    def add_arguments(self, parser):
        parser.add_argument('--rounds', default=1, type=int)
        return

    def handle(self, *args, **options):
        time_deltas = []
        data = BinaryFile.objects.all()
        _ = [x.check_vulnerable() for x in data]
        for round in range(options['rounds']):
            self.stdout.write(self.style.SUCCESS(f'[*] Begining Processing For Round {round}'))
            start = timer()
            _ = [x.check_vulnerable() for x in data]
            stop = timer()
            time_deltas.append(stop - start)
            self.stdout.write(self.style.SUCCESS(f'[*] Finished round in {stop-start} s'))
        avg_delta_time = sum(time_deltas) / len(time_deltas)
        self.stdout.write(self.style.SUCCESS(f'[*] Finished in {avg_delta_time} s average on serial processing'))

