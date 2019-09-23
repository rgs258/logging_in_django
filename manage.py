#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import logging
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

    # An example of configuring logging through the API, this sets a format on a new formatter and assigns it as default
    logging._defaultFormatter = logging.Formatter('%(asctime)s %(levelname)-8s %(name)s.%(funcName)s: %(message)s')

    # This exception hook assignment shows how an uncaught exception below is handled by the excepthook. Comment this
    #  line to see how the default exception handler sends the message to sys.stderr
    sys.excepthook = lambda type, value, traceback: \
        logging.getLogger('*excepthook*').critical(f'Uncaught Exception!', exc_info=(type, value, traceback))

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:

        # Django ships with a perfect example of raising an exception. The exception hook configured above
        # shows how an uncaught exception is handled by the excepthook
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
