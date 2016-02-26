from django.core.management.base import BaseCommand, CommandError
from bnlipsum.lyrics.lipsum import generate
from os import sys


class Command(BaseCommand):
    can_import_settings = True

    def add_arguments(self, parser):
        parser.add_argument('--words', type=int, default=50)
        parser.add_argument('--paragraphs', type=int, default=1)
        parser.add_argument(
            '--ignore-chorus', dest='ignore_chorus',
            type=bool, default=False
        )

    def handle(self, *args, **options):
        sys.stdout.write(
            generate(
                words=options['words'],
                paragraphs=options['paragraphs'],
                ignore_chorus=options['ignore_chorus']
            )
        )

        sys.stdout.write('\n\n')
