#!/usr/bin/env python
"""reducer.py"""
from operator import itemgetter
import sys
current_word = None
current_count = 0
word = None
# input comes from STDIN
for line in sys.stdin:
    line = line.strip()
    word, count = line.split('\t', 1) # parse the input from mapper.py
    try:
        count = int(count) # convert count (currently a string) to int
    except ValueError:
        # count was not a number, so silently ignore/discard this line
        continue
    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_word == word:
        current_count += count
    else:
        if current_word:
            # write result to STDOUT
            print '%s\t%s' % (current_word, current_count)
    current_count = count
    current_word = word
    # Do not forget to output the last word if needed!
if current_word == word:
    print '%s\t%s' % (current_word, current_count)
