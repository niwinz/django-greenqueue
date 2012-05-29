# This is an example test settings file for use with the Django test suite.
#
# The 'sqlite3' backend requires only the ENGINE setting (an in-
# memory database will be used). All other backends will require a
# NAME and potentially authentication information. See the
# following section in the docs for more information:
#
# https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/unit-tests/
#
# The different databases that Django supports behave differently in certain
# situations, so it is recommended to run the test suite against as many
# database backends as possible.  You may want to create a separate settings
# file for each of the backends you test against.

DATABASES = {
    'default': {
        'NAME': 'test.db',
        'ENGINE': 'django.db.backends.sqlite3'
    },
}

SECRET_KEY = "django_tests_secret_key"
# To speed up tests under SQLite we use the MD5 hasher as the default one. 
# This should not be needed under other databases, as the relative speedup
# is only marginal there.
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

INSTALLED_APPS = [
    'greenqueue',
]

GREENQUEUE_TASK_MODULES = ['greenqueue.tests.async_tasks']

GREENQUEUE_BACKEND = 'greenqueue.backends.zeromq.ZMQService'
