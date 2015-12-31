import gevent
from gevent import monkey
monkey.patch_all()

import urllib2

def foo():
    print('Running in foo')
    f = urllib2.urlopen('http://www.python.org/')
    print('Explicit context switch to foo again')

def bar():
    print('Explicit context to bar')
    f = urllib2.urlopen('http://www.python.org/')
    print('Implicit context switch back to bar')

gevent.joinall([
    gevent.spawn(foo),
    gevent.spawn(bar),
])
