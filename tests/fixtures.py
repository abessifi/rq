# -*- coding: utf-8 -*-
"""
This file contains all jobs that are used in tests.  Each of these test
fixtures has a slighty different characteristics.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import time
from os import environ
from subprocess import Popen, PIPE

from rq import Connection, get_current_job
from rq.decorators import job


def say_hello(name=None):
    """A job with a single argument and a return value."""
    if name is None:
        name = 'Stranger'
    return 'Hi there, %s!' % (name,)

def check_redis_version():
    """Check if Redis version is >= 2.8.6. Othewise some tests may fail"""
    version = environ.get('REDIS_VERSION')
    if version and version < "2.8.6": return True
    proc = Popen("redis-cli --version", stdout=PIPE, shell=True)
    version = proc.communicate()[0].split()[1]
    if version.decode() < "2.8.6": return True
    return False

def do_nothing():
    """The best job in the world."""
    pass


def div_by_zero(x):
    """Prepare for a division-by-zero exception."""
    return x / 0


def some_calculation(x, y, z=1):
    """Some arbitrary calculation with three numbers.  Choose z smartly if you
    want a division by zero exception.
    """
    return x * y / z


def create_file(path):
    """Creates a file at the given path.  Actually, leaves evidence that the
    job ran."""
    with open(path, 'w') as f:
        f.write('Just a sentinel.')


def create_file_after_timeout(path, timeout):
    time.sleep(timeout)
    create_file(path)


def access_self():
    job = get_current_job()
    return job.id


def echo(*args, **kwargs):
    return (args, kwargs)


class Number(object):
    def __init__(self, value):
        self.value = value

    @classmethod
    def divide(cls, x, y):
        return x * y

    def div(self, y):
        return self.value / y


with Connection():
    @job(queue='default')
    def decorated_job(x, y):
        return x + y


def long_running_job():
    time.sleep(10)
