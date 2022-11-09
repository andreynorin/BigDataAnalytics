#!/usr/bin/env python
"""mapper.py"""
import sys
import re
# input comes from STDIN (standard input)
for line in sys.stdin:
    line = line.strip()
    line = re.sub(r'[^ w s]','', line ))   # Remove punctuation
    line = re.sub(r d+]','', line)         # Remove numbers
    # split the line into words
    words = line.split()
    # increase counters
    for word in words:
    # tab delimited the word count is always 1
        print '%s t%s' % (word, 1)