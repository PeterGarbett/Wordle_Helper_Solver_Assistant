
Wordle helper/assistant/solver 
which I wrote to learn Python.  I thought Python was well suited to wordle solving since it involves
character and string handling. Given this some constructs probably aren't very Pythonesque .
Python3 and Linux Fedora 35 


README.md                            This file

wordle-valid-words.txt           Valid words to use in Wordle        
wordle-answers-alphabetical.txt     Words that are actually used as answers

wordle_helper.py                    Main entry point, giving wordy feedback on possibilities
sieve.py                            Code to work out what words satisfy the given constraints
wordle.py                           Code to predict wordle responses given a target word (for test purposes) 
suggest.py                          Alternate entry point giving a terse suggestion for a trial word
test.py                             Test harness - correct inputs
corner_cases.sh                     Test paths for invalid inputs
test_output.txt                     Test output


Calling arguments (see later concrete examples)

./wordle_helper.py  trialword1  result1 ... 
./wordle.py  target_word trialword1  result1  ....
./suggest.py  trialword1 result1 ... 
./test.py > test_output.txt

Algorithm

I use a frequency analysis of the possible answers to find words that
have a high probability of containing letters of interest, and give them
a score for how many of these they contain. I finesse the score by adding
a bonus for those that try differring positions for letters I know are in there
via Y denotations but dont know where.  The winner gets to be suggest.py output.
wordle_helper.py tells you what the possible solutions are which is interesting
since you can assess how good your strategy is by how fast you narrow down the possibilities.


Algorithm performance

Distribution of games: Counter({4: 1137, 3: 807, 5: 288, 2: 68, 6: 14, 1: 1})
Giving a solution in this number of tries on average: 3.7279

Which is quite close to the best possible achieved by optimising decision trees,
if the internet is to be believed. This is quite good for such as simple 
algorithm.

The test output gives the sequence the solver uses to arrive at the answer
for example these are the 14 worst case results:

bound found in: 6 using sequence ['later', 'noisy', 'dunce', 'thump', 'frown', 'bound']
boxer found in: 6 using sequence ['later', 'disco', 'woven', 'spiky', 'thumb', 'boxer']
chill found in: 6 using sequence ['later', 'lousy', 'clink', 'yield', 'chili', 'chill']
fixer found in: 6 using sequence ['later', 'disco', 'viper', 'unify', 'fiber', 'fixer']
found found in: 6 using sequence ['later', 'noisy', 'dunce', 'thump', 'frown', 'found']
frame found in: 6 using sequence ['later', 'cedar', 'spare', 'verge', 'brake', 'frame']
groom found in: 6 using sequence ['later', 'curio', 'drown', 'skimp', 'broom', 'groom']
hatch found in: 6 using sequence ['later', 'pinch', 'women', 'zebra', 'catch', 'hatch']
homer found in: 6 using sequence ['later', 'disco', 'woven', 'spiky', 'thumb', 'homer']
jelly found in: 6 using sequence ['later', 'slide', 'whole', 'query', 'belly', 'jelly'] 
jolly found in: 6 using sequence ['later', 'lousy', 'gland', 'welch', 'folly', 'jolly']
proxy found in: 6 using sequence ['later', 'curio', 'drown', 'skimp', 'proof', 'proxy']
roger found in: 6 using sequence ['later', 'disco', 'woven', 'spiky', 'thumb', 'roger']
wound found in: 6 using sequence ['later', 'noisy', 'dunce', 'thump', 'frown', 'wound']


Example usage

./wordle_helper.py later ybbyb slide bybby whole bbbgy query bbybg
Wordle helper/solver/assistant
7  words satisfy the constraints and they are:
 ['belly', 'felly', 'feyly', 'gelly', 'jelly', 'kelly', 'nelly']
When restricted to words actually known to be wordle answers:
(The answer is one of these): ['belly', 'jelly']
Suggested trial word: belly

./wordle.py jelly later slide whole query belly 
Wordle
jelly [('later', 'YBBYB'), ('slide', 'BYBBY'), ('whole', 'BBBGY'), ('query', 'BBYBG'), ('belly', 'BGGGG')]


