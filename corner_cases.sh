#!/usr/bin/sh

#
#   Explore handling of erronous inputs
#

# Words available but none when  limited to wordle solutions


./wordle_helper.py later bbbbb noisy bgyyb

#No possible solutions dues to finger trouble
#No solutions, probable constraint conflict
#

./wordle_helper.py later bbbbb later bgyyb

#Length checks 

./wordle_helper.py later bbbb
./wordle_helper.py ater bbbby
