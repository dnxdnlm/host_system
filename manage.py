#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from base.settings import BASE_DIR
from utils.logger import set_logger


def main():
    log_dir = os.path.join(BASE_DIR, 'log')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    set_logger('./log/info_srv.log', 'debug')
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
