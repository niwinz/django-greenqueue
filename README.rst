=================
django-greenqueue
=================

greenqueue is an asynchronous task queue/job queue based on distributed message passing. It is focused on real-time task execution
and have a simplest configuration.

Unlike celery, is fully integrated with django. By default do not require any kind of broker, working with queues on tcp/ip, 
thanks to zeromq. But in the future is intended to implement a backend so you can use with RabbitMQ.

This not supports scheduling with eta or countdown. This simple asynchronous queue/job queue based.

**NOTE**: This project was initially developed within Greenmine_.

.. _Greenmine: https://github.com/niwibe/Green-Mine

Features
--------

* Simple task declaration
* Simple configuration and 100% django integrated.
* Backend for testing mode.
* Workos on zeromq push/pull transport mode.

How to use?
-----------

TODO

How to install?
---------------

TODO

License
-------

TODO
