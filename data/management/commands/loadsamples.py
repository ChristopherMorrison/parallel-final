import os

from django.core.management.base import BaseCommand, CommandError
from data.models import BinaryFile


class Command(BaseCommand):
    help = 'Loads binary files from a dir for processing'

    def add_arguments(self, parser):
        parser.add_argument('sample_dir')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Begining Import:'))
        for _file in os.listdir(options['sample_dir']):
            BinaryFile.objects.create(data=options['sample_dir']+_file)
            self.stdout.write(self.style.SUCCESS(f'Loaded {_file}'))
