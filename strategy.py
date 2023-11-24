#!/usr/bin/python3
#
# 	Given a sequence of wordle trial words and results
# 	print the number of  words that satisfy the constraints
# 	at each stage so you can assess how good your word choices were
#
#   report word count of words that meet the constraints from the
#   full list of 5 letter words and also the much smaller list
#   of wordle answers
#

import pexpect
import sys
import suggest


# Lets assume these are in the same directory but allow override

path_to_wordle_helper = "./"

# 	Strings in the output that are  of interest

title = "Wordle helper/solver/assistant"
satisfy = "words satisfy the constraints and they are:"  # Expect a number prior to this
restricted = "When restricted to words actually known to be wordle answers:"

# Expect a number between these two strings:

There = "There are"
wrdlAnswers = "wordle solution words that satisfy the constraints and they are:"

# Output for two and one solutions:

Pairs = "The answer should be  one of these"
Singleton = "word satisfies the constraints and it is"

# A couple of error cases... no solutions

goneWrong = "No solutions, probable constraint conflict"
goneWrong2 = "ERROR: Missing input argument"

scantime = 9


def collect_data(guesslist):

    Wordle_results = []

    try:
        child = pexpect.spawn(
            #   Lets hope wordle_helper.py is on ones path
            path_to_wordle_helper + "wordle_helper.py " + guesslist,
            encoding="utf-8",
            timeout=scantime,
        )
        #        child.logfile = sys.stdout
        result = child.readlines()
        child.close()

        #   Catch all sorts of nonsense... wrong controller
        #   can't get hold of the dongle etc

    except:
        pass
        result = []

    # Trim some rubbish out

    stripp = [s.replace("\r", "") for s in result]
    stripped = [s.replace("\n", "") for s in stripp]

    # general has to default to 1 because thats what it should be when
    # only the restricted result is one

    restrict = 0        # assume you won't find any
    general = 1

    # Look for strings of interest and find the values they infer or contain

    for iter in stripped:
        if title in iter:
            stripped.remove(title)
            break

    for index, iter in enumerate(stripped):
        if satisfy in iter:
            Nwords = iter
            Nwords = Nwords.replace(satisfy, "")
            Nwords = Nwords.replace(" ", "")
            general = int(Nwords)

    for index, iter in enumerate(stripped):
        if goneWrong2 in iter:
            general = 0
            restrict = 0

    for index, iter in enumerate(stripped):
        if goneWrong in iter:
            general = 0
            restrict = 0

    for index, iter in enumerate(stripped):
        if Pairs in iter:
            restrict = 2

    for index, iter in enumerate(stripped):
        if Singleton in iter:
            restrict = 1

    for index, iter in enumerate(stripped):
        if wrdlAnswers in iter:
            Wwords = iter

            #   Clumsy.  But error free

            xxx = Wwords.replace(wrdlAnswers, "")
            xxxy = xxx.replace(There, "")
            xxxz = xxxy.replace(" ", "")
            restrict = int(xxxz)

    return (general, restrict)


# 	The usual entry point stuff...

if __name__ == "__main__":

    # Process the argument list and do some sanity checks on it
    # including using functions imported from suggest.py

    wordletest = sys.argv.pop(0)
    inputargs = sys.argv

    length = len(inputargs)
    if length % 2 != 0:
        print("Even number of inputs required")
        quit()

    couples = int(length / 2)

    # Lets start by knowing nothing at step zero
    # Print titles and results

    arglist = ""
    trial = collect_data(arglist)
    print("\nTurn   Words     Wordle")
    print("                 answers")
    print(0, "   ", f"{round(trial[0], 5): 6d}", " ", f"{round(trial[1], 5): 6d}")

    for index in range(0, couples):

        # Inspect pairs of inputs and see what good they do us
        # and print the results

        guess = inputargs[index * 2]

        if not suggest.good_guess(guess):
            print("Bad input word:", guess)
            quit()

        rawColours = inputargs[index * 2 + 1]
        colours = rawColours.upper()
        if not suggest.good_colours(colours):
            print("Bad input result", rawColours, " for word ", guess)
            quit()

        pair = guess + " " + colours
        arglist = arglist + " " + pair
        trial = collect_data(arglist)
        print(
            index + 1,
            "   ",
            f"{round(trial[0], 5): 6d}",
            " ",
            f"{round(trial[1], 5): 6d}",
        )
