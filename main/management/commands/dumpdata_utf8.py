# Reference: https://github.com/panhaoyu/django-dump-load-utf8

from django.core.management.commands import dumpdata

class Command(dumpdata.Command):
    def execute(self, *args, **options):
        try:
            if path := options.get('output'):
                options['output'] = None
                with open(path, mode="w", encoding="utf-8") as f:
                    self.stdout = f
                    result = super(Command, self).execute(*args, **options)
            else:
                result = super(Command, self).execute(*args, **options)
            return result
        except Exception as err:
            print("")
            if hasattr(err, '__iter__'):
                for e in err:
                    print(f"{err.__class__.__name__}: {str(e)}")
            else:
                print(f"{err.__class__.__name__}: {str(err)}")
