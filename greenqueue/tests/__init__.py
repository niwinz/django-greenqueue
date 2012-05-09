# -*- coding: utf-8 -*-

from django.test import TestCase
from greenqueue import settings, send_task

class TestAsyncMethods(TestCase):
    @classmethod
    def setUpClass(cls):
        settings.GREENQUEUE_BACKEND = 'greenqueue.backends.sync.SyncService'
        settings.GREENQUEUE_TASK_MODULES = [
            'greenqueue.tests.async_modules',
        ]

    @classmethod
    def tearDownClass(cls):
        settings.GREENQUEUE_BACKEND = 'greenqueue.backends.zeromq.ZMQService'
        settings.GREENQUEUE_TASK_MODULES = []

    def test_send_task(self):
        ares = send_task('sum', args=[1,2])

        from greenqueue.result import AsyncResult
        self.assertIsInstance(ares, AsyncResult)
        self.assertFalse(ares.is_ready())

    def test_send_task_wait(self):
        ares = send_task('sum', args=[1,2])

        result = ares.wait()
        self.assertEqual(result, 3)

    def test_send_task_check(self):
        ares = send_task('sum', args=[1,2])

        result = ares.check()
        self.assertEqual(result, 3)

    def test_send_task_kwargs(self):
        ares = send_task('sum', kwargs={'x':1, 'y':2})

        from greenqueue.result import AsyncResult
        self.assertIsInstance(ares, AsyncResult)
        self.assertFalse(ares.is_ready())
