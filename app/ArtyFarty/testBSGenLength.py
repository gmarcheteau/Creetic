#!/usr/bin/env python
from __future__ import division
from bsgenerator_en import generatePhrase, generatePhrase_short
import numpy as np
import re


lengths = []

for i in range(0,1000):
  phrase = generatePhrase()
  lengths.append(len(phrase))
  print phrase

#print lengths
print "mean: %d" %np.mean(lengths)
print "min: %d" %np.min(lengths)
print "max: %d" %np.max(lengths)

undercap = sum(1 if l<114 else 0 for l in lengths)
print "%d out of %d phrases under 113 characters" %(undercap, len(lengths))
print "percentage: {:.0%}".format(undercap/len(lengths))
