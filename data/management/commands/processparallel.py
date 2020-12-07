import os
from timeit import default_timer as timer

from django.core.management.base import BaseCommand, CommandError
from data.models import BinaryFile
from data import tasks


class Command(BaseCommand):
    help = 'Process all samples in parallel tasks'

    def add_arguments(self, parser):
        parser.add_argument('--block-size', default=1, type=int)
        parser.add_argument('--method', choices=['passID', 'passObject'], default='passObject')
        return

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Begining Processing:'))
        result_queue = []
        if options['method'] == 'passID':
            models = BinaryFile.objects.all()
            index = 0
            count = models.count()
            self.stdout.write(self.style.SUCCESS(f'{count} Samples to Process'))
            first_idx = models.first().id
            start = timer()
            while index < count:
                if index > count: # a simple bounds check without padding
                    index = count
                result_queue.append(
                    tasks.evaluate_vuln_by_id_range.apply_async(args=(
                        first_idx+index,
                        first_idx+index+options['block_size'],
                    ))
                )
                index += options['block_size']

        else:
            models = BinaryFile.objects.all()
            index = 0
            count = models.count()
            self.stdout.write(self.style.SUCCESS(f'{count} Samples to Process'))
            start = timer()
            while index < count:
                if index > count: # a simple bounds check without padding
                    index = count
                result_queue.append(
                    tasks.evaluate_vuln_by_model.apply_async(args=(
                        models[index:index+options['block_size']],
                    ))
                )
                index += options['block_size']

        for task in result_queue:
            task.wait() # This will add a bit of overhead
        stop = timer()

        self.stdout.write(self.style.SUCCESS(f'End of Processing, finished in {stop-start} s'))

        return