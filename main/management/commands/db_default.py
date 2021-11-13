from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from pathlib import Path

from dotenv import load_dotenv
from os import getenv

class Command(BaseCommand):
    help = "Change Database to SQLite (dafault)."

    def handle(self, *args, **options):
        try:
            # Taking Backup of Existing Database
            backup_time = timezone.now().strftime('%Y-%m-%d_%H-%M-%S')
            backup_file_name = "database_backup_" + backup_time + ".json"
            backup_file_path = "backup/partial/" + backup_file_name
            Path("backup/partial/").mkdir(parents=True, exist_ok=True)
            call_command("dumpdata_utf8", output=backup_file_path)

            # Changing Database to SQLite
            load_dotenv()
            SECRET_KEY = str(getenv('SECRET_KEY'))
            with open(".env", "w") as file:
                file.write(f"SECRET_KEY={SECRET_KEY}\nDATABASE_CODE=0\n")

            # Restoring Backup to New Database
            call_command("migrate", run_syncdb=True)
            ContentType.objects.all().delete()
            call_command("loaddata_utf8", backup_file_path)
        except Exception as err:
            self.stdout.write("")
            if hasattr(err, '__iter__'):
                for e in err:
                    self.stdout.write(f"{err.__class__.__name__}: {str(e)}")
            else:
                self.stdout.write(f"{err.__class__.__name__}: {str(err)}")
