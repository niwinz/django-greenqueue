# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from optparse import make_option

import logging
import zmq
import sys
import os

log = logging.getLogger('greenqueue')

from greenqueue import settings as gq_settings
from greenqueue.shortcuts import load_backend_class

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--socket', action="store", dest="socket", default=gq_settings.GREENQUEUE_BIND_ADDRESS,
            help="Tells greenqueue server to use this zmq push socket path instead a default."),
    )

    help = "Starts a greenqueue worker."
    args = "[]"

    def handle(self, *args, **options):
        gq_settings.GREENQUEUE_BIND_ADDRESS = options['socket']
        
        service_handler = load_backend_class().instance()
        verbosity = int(options.get('verbosity'))

        if verbosity > 1:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)
        
        try:
            service_handler.start()
        except KeyboardInterrupt:
            pass
