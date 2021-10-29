# Reference: https://github.com/panhaoyu/django-dump-load-utf8

from django.core.management.commands import loaddata

class Command(loaddata.Command):
    def loaddata(self, fixture_labels):
        try:
            super(Command, self).loaddata(fixture_labels)

            def open_with_utf8(*args, **kwargs):
                kwargs.setdefault('encoding', 'utf-8')
                return open(*args, **kwargs)

            self.compression_formats[None] = open_with_utf8
        except Exception as err:
            print("")
            if hasattr(err, '__iter__'):
                for e in err:
                    print(f"{err.__class__.__name__}: {str(e)}")
            else:
                print(f"{err.__class__.__name__}: {str(err)}")
