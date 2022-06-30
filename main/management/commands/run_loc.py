from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Run the app locally."

    def add_arguments(self, parser):
        parser.add_argument('--port', default=8000)
        parser.add_argument('--insecure', default=None, action='store_true')

    def handle(self, *args, **options):
        try:
            self.stdout.write(f"Server Address: 127.0.0.1:{options['port']}")
            if options['insecure'] is None:
                call_command("runserver", f"127.0.0.1:{options['port']}")
            else:
                call_command("runserver", f"127.0.0.1:{options['port']}", "--insecure")
        except Exception as err:
            self.stdout.write("")
            if hasattr(err, '__iter__'):
                for e in err:
                    self.stdout.write(f"{err.__class__.__name__}: {str(e)}")
            else:
                self.stdout.write(f"{err.__class__.__name__}: {str(err)}")
