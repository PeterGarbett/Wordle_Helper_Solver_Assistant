
Wordle helper/assistant/solver 
which I wrote to learn Python.  I thought Python was well suited to wordle solving since it involves
character and string handling. Given this some constructs probably aren't very Pythonesque .
Python3 and Linux 


README.md                            This file

wordle-valid-words.txt              Valid words to use in Wordle        
wordle-answers-alphabetical.txt     Words that are actually known to be possible answers

wordle_hard.py                      Entry point if we want hard mode
wordle_helper.py                    Main entry point, giving wordy feedback on possibilities
sieve.py                            Code to work out what words satisfy the given constraints
wordle.py                           Code to predict wordle responses given a target word (for test purposes) 
strategy.py                         Given a sequence of wordle trial words and results
                                    print the number of  words that satisfy the constraints
                                    at each stage so you can assess how good your word choices were
suggest.py                          Alternate entry point giving a terse suggestion for a trial word
readfile_ignore_comments.py 	    Read a file into a list ignoring #comments . Null return is no such file

wordle-test.py                      Test harness - correct inputs (add any parameter to invoke hard mode)
corner_cases.sh                     Test paths for invalid inputs
generate_test_results               Run test program with differing scenarios

wordle_test_results.txt             Normal test results
wordle_test_results_p.txt           Test results using information about prior results
wordle_test_results_h.txt           Hard mode test results
wordle_test_results_hp.txt          Hard mode used with previous result info

Hard mode using previous results only fails on one case now.


Calling arguments (see later concrete examples)

./wordle_helper.py  trialword1  result1 ... 
./wordle.py  target_word trialword1  result1  ....
./strategy.py  trialword1  result1 ... 
./suggest.py  trialword1 result1 ... 
./wordle-test.py > test_results.txt

Algorithm

I use a frequency analysis of the possible answers to find words that
have a high probability of containing letters of interest, and give them
a score for how many of these they contain. I finesse the score by adding
a bonus for those that try differring positions for letters I know are in there
via Y denotations but dont know where.  The winner gets to be suggest.py output.
wordle_helper.py tells you what the possible solutions are which is interesting
since you can assess how good your strategy is by how fast you narrow down the possibilities.

They recently added a word to the possible answers list and will probably do so again. (Yes reader
they did! Next one will be "fubar" at this rate) In which case the program comes up blank
for the answer but gives you a list of the more general possibilities. Hopefully not
too big a list and with a few crazy entries that almost certainly aren't it. 
I've modified the program so it generates suggested trial words for this case. 

I've enabled the use of a list of previous answers. This is used only to modify
the choice of trial word when we are down to a pair. The original idea was to modify
searches but this by contrast is a gentle nudge. Defaults to enabled but quietly ignores
this feature if we can't find the appropriate list . 
Introduced because I was fed up with choosing the
wrong item from a pair.

Algorithm performance

Distribution of games: Counter({4: 1147, 3: 808, 5: 286, 2: 67, 6: 17, 1: 1})
Giving a solution in this number of tries on average: 3.7313

Which is quite close to the best possible achieved by optimising decision trees,
if the internet is to be believed. This is quite good for such a simple 
algorithm.

The test output gives the sequence the solver uses to arrive at the answer
for example these are the worst case results:


belly found in: 6 using sequence ['later', 'slide', 'whole', 'query', 'jelly', 'belly']
bound found in: 6 using sequence ['later', 'noisy', 'dunce', 'thump', 'frown', 'bound']
boxer found in: 6 using sequence ['later', 'disco', 'woven', 'spiky', 'thumb', 'boxer']
brake found in: 6 using sequence ['later', 'cedar', 'spare', 'verge', 'frame', 'brake']
bring found in: 6 using sequence ['later', 'curio', 'smirk', 'vying', 'wring', 'bring']
broom found in: 6 using sequence ['later', 'curio', 'drown', 'skimp', 'groom', 'broom']
catch found in: 6 using sequence ['later', 'pinch', 'women', 'zebra', 'hatch', 'catch']
chill found in: 6 using sequence ['later', 'lousy', 'clink', 'yield', 'chili', 'chill']
fiber found in: 6 using sequence ['later', 'disco', 'viper', 'unify', 'fixer', 'fiber']
foggy found in: 6 using sequence ['later', 'noisy', 'embed', 'sprig', 'goofy', 'foggy']
folly found in: 6 using sequence ['later', 'lousy', 'gland', 'welch', 'jolly', 'folly']
found found in: 6 using sequence ['later', 'noisy', 'dunce', 'thump', 'frown', 'found']
homer found in: 6 using sequence ['later', 'disco', 'woven', 'spiky', 'thumb', 'homer']
howdy found in: 6 using sequence ['later', 'noisy', 'embed', 'wedge', 'dowdy', 'howdy']
proxy found in: 6 using sequence ['later', 'curio', 'drown', 'skimp', 'proof', 'proxy']
roger found in: 6 using sequence ['later', 'disco', 'woven', 'spiky', 'thumb', 'roger']
wound found in: 6 using sequence ['later', 'noisy', 'dunce', 'thump', 'frown', 'wound']

Example usage

./wordle_helper.py later ybbyb slide bybby whole bbbgy query bbybg

Wordle helper/solver/assistant

7  words satisfy the constraints and they are:
 ['belly', 'felly', 'feyly', 'gelly', 'jelly', 'kelly', 'nelly']
Suggested trial word for this list: feign 

When restricted to words actually known to be wordle answers,
the possible answers are : ['belly', 'jelly'] 

Of these, these have previously been  used as wordle solutions: ['belly']
leaving these more likely: ['jelly']
Suggested trial word for known answers: jelly


./wordle.py jelly later slide whole query belly 
Wordle
jelly [('later', 'YBBYB'), ('slide', 'BYBBY'), ('whole', 'BBBGY'), ('query', 'BBYBG'), ('belly', 'BGGGG')]

Hard mode:

./wordle_hard.py can be used to provide guesses that satify constraints so far.
To produce hard mode test results :
./wordle-test.py hard 
This shows that on average you do better, but risk losing:

Distribution of games: Counter({4: 941, 3: 883, 5: 289, 2: 133, 6: 68, 7: 8, 8: 4, 1: 1})
Giving a solution in this number of tries on average: 3.704

Phase 2 !!:

The set of allowable solutions gets expanded occasionally
and dealing with this gracefully is a design aim.

The addition of 'gofer' led to
boxer taking 7 tries.  'later' is the word my algorithm
comes out with, but it turns out it is slightly non optimal.
Some clever people out there suggest 'tales' as a start word,
and this solves the problem.  At some point looking at
getting this out of the code naturally would be nice. 
for now I force it.  It ammount to seaching for an 's'
first go, wheras I used to search for a 'r'.
'tales' also gets excluded from my candidates because
its a plural...

Here are updated test results. It is notable that
using information from previous results now makes hard mode
doable given the current set of answers.

==> wordle_test_results_hp.txt <==
wreck found in: 3 using sequence ['tales', 'urine', 'wreck']
wrest found in: 3 using sequence ['tales', 'pesto', 'wrest']
wring found in: 4 using sequence ['tales', 'crony', 'drunk', 'wring']
write found in: 3 using sequence ['tales', 'refit', 'write']
wryly found in: 4 using sequence ['tales', 'lyric', 'dryly', 'wryly']
zonal found in: 3 using sequence ['tales', 'coral', 'zonal']
Hooray! worst case is  6
Number of games: 941
Distribution of games: Counter({3: 497, 4: 309, 2: 100, 5: 30, 6: 5})
Giving a solution in this number of tries on average: 3.3018

==> wordle_test_results_h.txt <==
yield found in: 3 using sequence ['tales', 'guile', 'yield']
young found in: 3 using sequence ['tales', 'irony', 'young']
youth found in: 3 using sequence ['tales', 'intro', 'youth']
zebra found in: 4 using sequence ['tales', 'cedar', 'yearn', 'zebra']
zesty found in: 4 using sequence ['tales', 'stone', 'heist', 'zesty']
zonal found in: 3 using sequence ['tales', 'coral', 'zonal']
Failed to solve within 6 tries, worst case is  8
Number of games: 2337
Distribution of games: Counter({4: 990, 3: 908, 5: 247, 2: 122, 6: 56, 7: 11, 8: 3})
Giving a solution in this number of tries on average: 3.6799

==> wordle_test_results_p.txt <==
wreck found in: 3 using sequence ['tales', 'urine', 'wreck']
wrest found in: 3 using sequence ['tales', 'pesto', 'wrest']
wring found in: 4 using sequence ['tales', 'crony', 'drunk', 'wring']
write found in: 3 using sequence ['tales', 'refit', 'write']
wryly found in: 4 using sequence ['tales', 'lyric', 'dryly', 'wryly']
zonal found in: 3 using sequence ['tales', 'coral', 'zonal']
Hooray! worst case is  5
Number of games: 941
Distribution of games: Counter({3: 505, 4: 339, 2: 72, 5: 25})
Giving a solution in this number of tries on average: 3.3369

==> wordle_test_results.txt <==
yield found in: 4 using sequence ['tales', 'guile', 'witty', 'yield']
young found in: 3 using sequence ['tales', 'irony', 'young']
youth found in: 3 using sequence ['tales', 'intro', 'youth']
zebra found in: 4 using sequence ['tales', 'cedar', 'yearn', 'zebra']
zesty found in: 4 using sequence ['tales', 'stone', 'heist', 'zesty']
zonal found in: 4 using sequence ['tales', 'coral', 'windy', 'zonal']
Hooray! worst case is  6
Number of games: 2337
Distribution of games: Counter({4: 1170, 3: 815, 5: 267, 2: 70, 6: 15})
Giving a solution in this number of tries on average: 3.7184

8
