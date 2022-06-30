from django.core.management.base import BaseCommand
from django.core.management import call_command
import socket

class Command(BaseCommand):
    help = "Run the app over LAN."

    def add_arguments(self, parser):
        parser.add_argument('--port', default=8000)
        parser.add_argument('--insecure', default=None, action='store_true')

    def handle(self, *args, **options):
        try:
            host_name = socket.gethostname()
            host_addr = socket.gethostbyname(host_name + ".local")
            self.stdout.write(f"Server Address: {host_addr}:{options['port']}")
            if options['insecure'] is None:
                call_command("runserver", f"0.0.0.0:{options['port']}")
            else:
                call_command("runserver", f"0.0.0.0:{options['port']}", "--insecure")
        except Exception as err:
            self.stdout.write("")
            if hasattr(err, '__iter__'):
                for e in err:
                    self.stdout.write(f"{err.__class__.__name__}: {str(e)}")
            else:
                self.stdout.write(f"{err.__class__.__name__}: {str(err)}")
