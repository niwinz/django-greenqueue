# -*- coding: utf-8 -*-

import sys, os
sys.path.insert(0, "..")

#test_settings = {
#    'DATABASES':{
#        'default': {
#            'ENGINE': 'django.db.backends.sqlite3',
#        }
#    },
#    'ROOT_URLCONF': 'test_app.urls',
#    'INSTALLED_APPS': [
#        'superview',
#        'test_app',
#    ],
#    'SV_CSS_MENU_ACTIVE':'selected',
#}

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

if __name__ == '__main__':
    test_args = sys.argv[1:]

    #if not settings.configured:
    #    settings.configure(**test_settings)

    if not test_args:
        test_args = ['greenqueue']
    
    from django.test.simple import DjangoTestSuiteRunner
    runner = DjangoTestSuiteRunner(verbosity=2, interactive=True, failfast=False)
    failures = runner.run_tests(test_args)
    sys.exit(failures)
