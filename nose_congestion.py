# encoding: utf-8
from __future__ import absolute_import, print_function

import operator
from functools import wraps
from inspect import ismodule, getargspec
from time import time
from functools import partial

from nose.plugins import Plugin

def isclassmethod(f):
    """
    Basic check for classmethod in python 2.7. For python 3 we don't care,
    because no special handling is required to decorate  setup_class
    unboundmethods.
    """
    if hasattr(f, '__self__') and isinstance(f.__self__, type):
        return True
    return False

# @TODO: Remove hard coded formatting and allow TIMED_METHODS to drive the
# columns to display

class CongestionPlugin(Plugin):
    """Measure total test execution time"""
    name = 'congestion'

    TIMED_METHODS = ('setUp', 'tearDown', 'setup_class', 'teardown_class')

    def __init__(self):
        super(CongestionPlugin, self).__init__()
        self.start_times = {}
        self.elapsed_times = {}
        self.timed_tests = {}

    @staticmethod
    def name_for_obj(i):
        if ismodule(i):
            return i.__name__
        else:
            return "%s.%s" % (i.__module__, i.__name__)

    def record_elapsed_decorator(self, f, ctx, key_name):
        @wraps(f)
        def wrapped(*args, **kwargs):
            start_time = time()
            # Workaround, because nosetests manupulates the function args when
            # calling this method.  We have to put the cls as the 1st argument
            # to call the classmethod, but then pop of when we do tthe
            # underlying method call.  To see why his is needed look at: nose/util.py:471
            if isclassmethod(f):
                args = tuple(list(args)[1:])

            try:
                return f(*args, **kwargs)
            finally:
                ctx[key_name] = time() - start_time

        if isclassmethod(f):
            return partial(wrapped, f.__self__)
        else:
            return wrapped

    def startContext(self, context):
        # Initialise zeroed context timing dict
        ctx = {k: 0 for k in self.TIMED_METHODS}
        ctx['total'] = 0
        ctx_name = self.name_for_obj(context)
        self.elapsed_times[ctx_name] = ctx

        for method_name in self.TIMED_METHODS:
            if hasattr(context, method_name):
                old_f = getattr(context, method_name)
                new_f = self.record_elapsed_decorator(old_f, ctx, method_name)
                setattr(context, method_name, new_f)

        self.start_times[context] = time()

    def stopContext(self, context):
        end_time = time()

        elapsed = end_time - self.start_times.pop(context)
        ctx_name = self.name_for_obj(context)
        self.elapsed_times[ctx_name]['total'] = elapsed

    def startTest(self, test):
        self._timer = time()

    def _register_time(self, test):
        self.timed_tests[test.id()] = self._timeTaken()

    def _timeTaken(self):
        if hasattr(self, '_timer'):
            return time() - self._timer
        else:
            # Test died before it ran (probably error in setup()) or
            # success/failure added before test started probably due to custom
            # TestResult munging.
            return 0.0

    def addError(self, test, err, capt=None):
        self._register_time(test)

    def addFailure(self, test, err, capt=None, tb_info=None):
        self._register_time(test)

    def addSuccess(self, test, capt=None):
        self._register_time(test)

    def report(self, stream):
        print("%-43s %10s %10s %10s %10s" % ('Location', 'Total', 'setup_class', 'teardown_class' 'setUp', 'tearDown'),
              file=stream)
        print('-' * 70, file=stream)

        fmt = "{0:43s} {total:>10.3f} {setup_class:>10.3f} {teardown_class:>10.3f} {setUp:>10.3f} {tearDown:>10.3f}"
        for context_name in sorted(self.elapsed_times.keys()):
            times = self.elapsed_times[context_name]
            print(fmt.format(context_name, **times), file=stream)

        print(file=stream)
        print("%7s  %-60s" % ('Total', 'Location'), file=stream)
        print('-' * 70, file=stream)

        fmt = "{0[1]:>7.3f}  {0[0]:60s}"

        for timed in sorted(self.timed_tests.items(),
                            key=operator.itemgetter(1), reverse=True):
            print(fmt.format(timed), file=stream)
