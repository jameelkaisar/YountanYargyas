from django.core.management.base import BaseCommand
from django.core.management import call_command
from socket import gethostname, gethostbyname

class Command(BaseCommand):
    help = "Run the app over LAN."

    def add_arguments(self, parser):
        parser.add_argument('--port', default=8000)

    def handle(self, *args, **options):
        try:
            host_name = gethostname()
            host_addr = gethostbyname(host_name + ".local")
            self.stdout.write(f"Server Address: {host_addr}:{options['port']}")
            call_command("runserver", f"0.0.0.0:{options['port']}", insecure=True)
        except Exception as err:
            self.stdout.write("")
            if hasattr(err, '__iter__'):
                for e in err:
                    self.stdout.write(f"{err.__class__.__name__}: {str(e)}")
            else:
                self.stdout.write(f"{err.__class__.__name__}: {str(err)}")
