#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

before = time.time()
i = 0
a = 0
while i<10000000000:
    i = i + 1
    a = a + i

print time.time() - before
print i
