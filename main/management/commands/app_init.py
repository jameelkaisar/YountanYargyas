from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
from django.core.management.utils import get_random_secret_key
from django.core.management import call_command
from django.contrib.auth.password_validation import validate_password

class Command(BaseCommand):
    help = "Initialize the app. Create superuser, teacher group, monitor group."

    def add_arguments(self, parser):
        parser.add_argument('--username', default=None)
        parser.add_argument('--password', default=None)

    def handle(self, *args, **options):
        try:
            self.stdout.write("\nGenerating \"SECRET_KEY\"...")
            with open(".env", "w") as file:
                file.write(f"SECRET_KEY={get_random_secret_key()}\n")

            self.stdout.write("Command \"makemigrations\":")
            call_command("makemigrations")

            self.stdout.write("\nCommand \"migrate\":")
            call_command("migrate")

            self.stdout.write("\nCreating \"teacher\" Group...")
            Group.objects.get_or_create(name='teacher')

            self.stdout.write("\nCreating \"monitor\" Group...")
            Group.objects.get_or_create(name='monitor')

            self.stdout.write("\nCreating Superuser...")

            if options['username'] is not None:
                username = options['username']
            else:
                username = input("\nEnter Username: ").strip()
            User.username_validator(username)

            if options['password'] is not None:
                password = options['password']
            else:
                while True:
                    password = input("\nEnter Password: ").strip()
                    password_confirm = input("Enter Password Again: ").strip()
                    if password == password_confirm:
                        break
                    else:
                        self.stdout.write("The two passwords did not match!")

            validate_password(password)

            User.objects.create_superuser(username=username, password=password)
        except Exception as err:
            self.stdout.write("")
            if hasattr(err, '__iter__'):
                for e in err:
                    self.stdout.write(f"{err.__class__.__name__}: {str(e)}")
            else:
                self.stdout.write(f"{err.__class__.__name__}: {str(err)}")
