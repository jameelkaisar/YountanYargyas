from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.contenttypes.models import ContentType
import os

from dotenv import load_dotenv
from os import getenv

class Command(BaseCommand):
    help = "Migrate to New Database."

    def handle(self, *args, **options):
        try:
            # Loading backup_file_path from .tmp file
            with open(".tmp", "r") as file:
                backup_file_path = file.read()

            # Restoring Backup to New Database
            call_command("makemigrations")
            call_command("migrate")
            call_command("migrate", run_syncdb=True)
            ContentType.objects.all().delete()
            call_command("loaddata_utf8", backup_file_path)

            # Deleting .tmp file
            os.remove(".tmp")
        except Exception as err:
            self.stdout.write("")
            if hasattr(err, '__iter__'):
                for e in err:
                    self.stdout.write(f"{err.__class__.__name__}: {str(e)}")
            else:
                self.stdout.write(f"{err.__class__.__name__}: {str(err)}")
