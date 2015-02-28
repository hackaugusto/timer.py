# -*- coding: utf8 -*-
'''Wrapper around the timerfd interface to create a pollable timer.'''
import unittest
import ctypes
import sys
from ctypes.util import find_library

cint = ctypes.c_int
clong = ctypes.c_long


def clib(function, arguments_types, return_type):
    clib = ctypes.CDLL(find_library('c'))

    func = getattr(clib, function)
    func.argtypes = arguments_types
    func.restype = return_type

    return func


class timespec(ctypes.Structure):
    # <bits/types.h>
    # typedef long int __time_t;
    # typedef long int __syscall_slong_t;
    #
    # <time.h>
    # typedef __time_t time_t;
    # struct timespec
    # {
    #     __time_t tv_sec;
    #     __syscall_slong_t tv_nsec;
    # };
    _fields_ = [
        ('tv_sec', clong),
        ('tv_nsec', clong),
    ]


class itimerspec(ctypes.Structure):
    # struct itimerspec
    # {
    #     struct timespec it_interval;
    #     struct timespec it_value;
    # };
    _fields_ = [
        ('it_interval', timespec),
        ('it_value', timespec),
    ]


# int timerfd_create(int, int);
create = clib('timerfd_create', [cint, cint], cint)
# int timerfd_settime(int, int, const struct itimerspec, struct itimerspec);
settime = clib('timerfd_settime', [cint, cint, ctypes.POINTER(itimerspec), ctypes.POINTER(itimerspec)], cint)
# int timerfd_gettime(int, struct itimerspec*);
gettime = clib('timerfd_gettime', [cint, cint, ctypes.POINTER(itimerspec)], cint)

# <bis/time.h>
CLOCK_REALTIME = 0      # Identifier for system-wide realtime clock.
CLOCK_MONOTONIC = 1     # Monotonic system-wide clock.

# <bits/timerfd.h>
TFD_CLOEXEC = 524288    # int('02000000', 8)
TFD_NONBLOCK = 2048     # int('00004000', 8)

NULL_SPEC = ctypes.POINTER(itimerspec)()


class Timer(object):
    def __init__(self, interval_ms, clock_type=CLOCK_MONOTONIC, flags=TFD_CLOEXEC + TFD_NONBLOCK):
        self._fileno = create(cint(clock_type), cint(flags))

        miliseconds = interval_ms % 1000
        seconds = interval_ms / 1000
        nanoseconds = miliseconds * 1000000

        repeat = timespec(seconds, nanoseconds)
        first = timespec(seconds, nanoseconds)

        spec = itimerspec(repeat, first)

        settime(self._fileno, 0, spec, NULL_SPEC)

    def fileno(self):
        return self._fileno


class TimerTestCase(unittest.TestCase):
    def test_pass(self):
        pass


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true', default=False, help='flag to run the tests')
    parser.add_argument('--failfast', action='store_true', default=False, help='unittest failfast')
    args = parser.parse_args()

    if args.test:
        import doctest

        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TimerTestCase)
        result = unittest.TextTestRunner(failfast=args.failfast).run(suite)

        if result.errors or result.failures:
            sys.exit(len(result.errors) + len(result.failures))

        (failures, total) = doctest.testmod()

        if failures:
            sys.exit(failures)
