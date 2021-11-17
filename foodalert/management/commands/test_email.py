from django.core.management.base import BaseCommand, CommandError
# from foodalert.sender import Sender

class Command(BaseCommand):
    help = 'Tests email sending time and function when there are many recipients'

    def add_arguments(self, parser):
        parser.add_argument(
            '--domain',
            type=str,
            nargs='?',
            default='example.com',
            const='example.com',
            help='Domain used to create fake email addresses (e.g. if --domain=example.com then emails will end in @example.com)',
        )

        parser.add_argument(
            'num',
            nargs='?',
            type=int,
            default=1000,
            const=1000,
            help='Number of fake email addresses to create and send email to',
        )


    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(options))