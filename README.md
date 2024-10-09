
Wordle helper/assistant/solver 
which I wrote to learn Python.  I thought Python was well suited to wordle solving since it involves
character and string handling. Given this some constructs probably aren't very Pythonesque .
Python3 and Linux Fedora 35 


README.md                            This file

wordle-valid-words.txt              Valid words to use in Wordle        
wordle-answers-alphabetical.txt     Words that are actually known to be possible answers

wordle_helper.py                    Main entry point, giving wordy feedback on possibilities
sieve.py                            Code to work out what words satisfy the given constraints
wordle.py                           Code to predict wordle responses given a target word (for test purposes) 
strategy.py                         Given a sequence of wordle trial words and results
                                    print the number of  words that satisfy the constraints
                                    at each stage so you can assess how good your word choices were
suggest.py                          Alternate entry point giving a terse suggestion for a trial word
readfile_ignore_comments.py 	    Read a file into a list ignoring #comments . Null return is no such file

test.py                             Test harness - correct inputs
corner_cases.sh                     Test paths for invalid inputs
test_results.txt                    Test output


Calling arguments (see later concrete examples)

./wordle_helper.py  trialword1  result1 ... 
./wordle.py  target_word trialword1  result1  ....
./strategy.py  trialword1  result1 ... 
./suggest.py  trialword1 result1 ... 
./test.py > test_results.txt

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

Distribution of games: Counter({4: 1142, 3: 808, 5: 289, 2: 67, 6: 16, 1: 1})
Giving a solution in this number of tries on average: 3.7314


Which is quite close to the best possible achieved by optimising decision trees,
if the internet is to be believed. This is quite good for such as simple 
algorithm.

The test output gives the sequence the solver uses to arrive at the answer
for example these are the 16 worst case results:


test_results.txt:belly found in: 6 using sequence ['later', 'slide', 'whole', 'query', 'jelly', 'belly']
test_results.txt:bound found in: 6 using sequence ['later', 'noisy', 'dunce', 'thump', 'frown', 'bound']
test_results.txt:boxer found in: 6 using sequence ['later', 'disco', 'woven', 'spiky', 'thumb', 'boxer']
test_results.txt:brake found in: 6 using sequence ['later', 'cedar', 'spare', 'verge', 'frame', 'brake']
test_results.txt:broom found in: 6 using sequence ['later', 'curio', 'drown', 'skimp', 'groom', 'broom']
test_results.txt:catch found in: 6 using sequence ['later', 'pinch', 'women', 'zebra', 'hatch', 'catch']
test_results.txt:chill found in: 6 using sequence ['later', 'lousy', 'clink', 'yield', 'chili', 'chill']
test_results.txt:fixer found in: 6 using sequence ['later', 'disco', 'viper', 'unify', 'fiber', 'fixer']
test_results.txt:foggy found in: 6 using sequence ['later', 'noisy', 'embed', 'sprig', 'goofy', 'foggy']
test_results.txt:folly found in: 6 using sequence ['later', 'lousy', 'gland', 'welch', 'jolly', 'folly']
test_results.txt:found found in: 6 using sequence ['later', 'noisy', 'dunce', 'thump', 'frown', 'found']
test_results.txt:homer found in: 6 using sequence ['later', 'disco', 'woven', 'spiky', 'thumb', 'homer']
test_results.txt:howdy found in: 6 using sequence ['later', 'noisy', 'embed', 'wedge', 'dowdy', 'howdy']
test_results.txt:proxy found in: 6 using sequence ['later', 'curio', 'drown', 'skimp', 'proof', 'proxy']
test_results.txt:roger found in: 6 using sequence ['later', 'disco', 'woven', 'spiky', 'thumb', 'roger']
test_results.txt:wound found in: 6 using sequence ['later', 'noisy', 'dunce', 'thump', 'frown', 'wound']


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


