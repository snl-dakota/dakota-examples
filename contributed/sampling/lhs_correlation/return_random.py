#!/usr/bin/env python
import random
import sys
from io import open
with open(sys.argv[2],'wt') as F:
    F.write(u'{}'.format(random.random()))
