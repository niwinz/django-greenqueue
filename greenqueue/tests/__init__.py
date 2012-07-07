# -*- coding: utf-8 -*-

from django.test import TestCase
from django.test.utils import override_settings
from django.core import management

from greenqueue import settings, send_task
import time, os.path, os, io

@override_settings(GREENQUEUE_BACKEND='greenqueue.backends.zeromq.ZMQService',
    GREENQUEUE_WORKER_MANAGER='greenqueue.worker.process.ProcessManager')
class TestZeromqBackend(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filename = "/tmp/greequeue.touch"

        from multiprocessing import Process
        def _subfunction():
            settings.GREENQUEUE_BACKEND='greenqueue.backends.zeromq.ZMQService'
            settings.GREENQUEUE_WORKER_MANAGER='greenqueue.worker.process.ProcessManager'
            management.call_command('run_greenqueue', verbosity=3)

        cls.p = Process(target=_subfunction)
        cls.p.start()

        settings.GREENQUEUE_BACKEND='greenqueue.backends.zeromq.ZMQService'
        settings.GREENQUEUE_WORKER_MANAGER='greenqueue.worker.process.ProcessManager'

    @classmethod
    def tearDownClass(cls):
        cls.p.terminate()

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_send_task(self):
        send_task('touch', args=[1])
        time.sleep(0.5)

        self.assertTrue(os.path.exists(self.filename))
        with io.open(self.filename) as f:
            self.assertEqual(f.read().strip(), "1")

    def test_send_with_countdown(self):
        send_task('touch', args=[1], countdown=2)

        self.assertFalse(os.path.exists(self.filename))
        time.sleep(3)

        self.assertTrue(os.path.exists(self.filename))
        with io.open(self.filename) as f:
            self.assertEqual(f.read().strip(), "1")


@override_settings(GREENQUEUE_BACKEND="greenqueue.backends.sync.SyncService",
    GREENQUEUE_WORKER_MANAGER='greenqueue.worker.sync.SyncManager')
class TestAsyncMethods(TestCase):
    @classmethod
    def setUpClass(cls):
        settings.GREENQUEUE_BACKEND="greenqueue.backends.sync.SyncService"
        settings.GREENQUEUE_WORKER_MANAGER='greenqueue.worker.sync.SyncManager'
        cls.filename = "/tmp/greequeue.touch"

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_send_task(self):
        send_task('touch', args=[1])
        time.sleep(0.5)

        self.assertTrue(os.path.exists(self.filename))
        with io.open(self.filename) as f:
            self.assertEqual(f.read().strip(), "1")

    def test_send_with_countdown(self):
        send_task('touch', args=[1], countdown=2)

        self.assertTrue(os.path.exists(self.filename))
        with io.open(self.filename) as f:
            self.assertEqual(f.read().strip(), "1")
