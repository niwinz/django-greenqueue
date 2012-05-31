=================
django-greenqueue
=================

greenqueue is an asynchronous task queue/job queue based based on distributed message passing. It is focused on real-time task execution
and have a simplest configuration.

Unlike celery, by default do not require any kind of broker, working with queues on tcp/ip, 
thanks to zeromq and is fully integrated with django.

But if you need persistence in the messages, as can also use RabbitMQ as message broker.

This not supports scheduling with eta or countdown. This is a simple asynchronous queue/job queue based.

**NOTE**: This project was initially developed within Greenmine_.

.. _Greenmine: https://github.com/niwibe/Green-Mine

Features
--------

* Simple task declaration
* Simple configuration and 100% django integrated.
* Backend for testing mode.
* Workos on zeromq push/pull transport mode.
* RabbitMQ backend support.

Work in progress
----------------

* Tasks by class.
* Process pooling.


How to use it?
==============

First step, create a module which will define the tasks. I recommend it in the file ``async_tasks.py`` placed in the 
root of your django app.

This is a sample example of task::

    from greenqueue.core import Library
    register = Library()
    
    @register.task(name='sum')
    def sum(x,y):
        return x+y 


**NOTE:** By default, **greenqueue** uses a **sync** backend (no need any worker, all runs on same thread; usefull for test), if need
, you can run all tasks on separate worker with zeromq backend. 


Backends
--------

Currently, three backends are available:

* ``greenqueue.backends.sync.SyncService`` - Synchronous backend, no worker need.
* ``greenqueue.backends.zeromq.ZMQService`` - Asynchronous backend with zeromq transport.
* ``greenqueue.backends.zeromq_gevent.ZMQService`` - Same as above, but spawn tasks in gevent pool. (beta)
* ``greenqueue.backends.rabbitmq.RabbitMQService`` - Asynchronous backend with RabbitMQ broker.


Settings
--------

``GREENQUEUE_BIND_ADDRESS``

    This a zeromq socket path. Default: ``ipc:///tmp/greenqueue.sock``. Is used with zeromq backend for send tasks
    to the workers. Not needed with sync backend.

``GREENQUEUE_TASK_MODULES``
    
    This a a list of modules on you have defined tasks. Need for automatic registring. Default: empty list.

``GREENQUEUE_BACKEND``
    
    Task dispatches and service backend. By default is set ``greenqueue.backends.sync.SyncService``, this is usefull
    for tests, because this does not need any worker.

    For use zeromq and separate worker for task, set this attr to ``greenqueue.backends.zeromq.ZMQService`` or 
    ``greenqueue.backends.zeromq_gevent.ZMQService``

``GREENQUEUE_BACKEND_POOLSIZE``

    Set a process pool size. At the momment, this settings property is used only with ``zeromq_gevent.ZMQService``
    backend.


RabbitMQ Settings
^^^^^^^^^^^^^^^^^

``GREENQUEUE_RABBITMQ_USERNAME``

    A RabbitMQ username. This is optional settings.

``GREENQUEUE_RABBITMQ_PASSWORD``
    
    A RabbitMQ password. Same as username, is an optional settings.

``GREENQUEUE_RABBITMQ_HOSTNAME``
    
    A RabbitMQ hostname, by default is ``localhost``. This settings is only mandatory if your rabbitmq server is on another server.

``GREENQUEUE_RABBITMQ_PORT``

    A RabbitMQ port, by default is ``5672``. This setting is only mandatory if your rabbitmq server listen in other port.

``GREENQUEUE_RABBITMQ_VHOST``
    
    A RabbitMQ virtual_host, by default is ``/``.

``GREENQUEUE_RABBITMQ_QUEUE``

    A RabbitMQ queue name used for queuing messages. By default is ``greenqueue``.

``GREENQUEUE_RABBITMQ_ROUTING_KEY``
    
    A RabbitMQ routing key, by default is same as that ``GREENQUEUE_RABBITMQ_QUEUE``

``GREENQUEUE_RABBITMQ_EXCHANGE``

    A RabbitMQ exchange, by default is an empty string.


Run a worker
------------

**NOTE**: at the moment only can run one worker. In the near future, be possible to run multiple processes 
and possibly combined with gevent.

Example::
    
    python manage.py run_greenqueue


Run or Send tasks to worker
---------------------------

In greenmine, each function/task is identified by a name. And to call a function, or in other words: to submit a job, 
you need to know the name of the task. Example::
    
    from greenqueue import send_task
    
    aresult = send_task('sum', args=[2,3])
    result = aresult.wait()


How to install?
---------------

At the moment, greenmine is not available on pypi. 
Pull git repository and install this manually::
    
    git clone git://github.com/niwibe/django-greenqueue.git
    cd django-greenqueue
    python setup.py install

License
-------

BSD License. You can see full license text on LICENSE file.

