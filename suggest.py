#!/usr/bin/python3
#

import wordle_helper
import sys

# The main code in wordle_helper aims to enlighten
# the user to where they are in the process. Such as how many possibilities
# remain.
#
# This code is much more terse, aimed at machines or users
# that just want the next trial word or a null telling them theres an error
# Hence 'suggest'.  I tell you what I would do for the next word
# Your current state is input as per wordle_helper.py as in:
#
# ./suggest.py guess1 result1 guess2 result2 ...
# (case insensitive)
# example:
# ./suggest.py later bybyb shade bbyby ocean bbygg
#

# Validity checking for word guesses and the reported response


def good_guess(word):
    if 5 == len(word):
        return word.islower()
    else:
        return False


def good_colours(results):

    if 5 != len(results):
        return False

    # Test for only having upper case Y B or G

    correct_responses = {"B", "Y", "G"}
    wordset = set(wordle_helper.split(results))
    return wordset.issubset(correct_responses)


# Iterate the tests over this list..   bet this is old fashioned not pythonesque but really...


def good_guesslist(guesslist):

    for tuple in guesslist:
        if not good_guess(tuple[0]):
            return False
        if not good_colours(tuple[1]):
            return False

    return True


def next_best_guess(guesslist, hard):

    answers = wordle_helper.suggestion(guesslist, hard)
    if answers == []:  # Constraint error probably
        return ""
    last = answers[-1]
    return last[1]


def nextTry(guesslist, hard):

    if good_guesslist(guesslist):
        trial = next_best_guess(guesslist, hard)
        return trial
    else:
        return ""


if __name__ == "__main__":

    # Form list of testword/result tuples
    # Much the same as the code in wordle_helper

    caller = sys.argv.pop(0)
    inputargs = sys.argv

    if (len(inputargs) % 2) != 0:  # Make sure we have pairs of inputs
        print("")
        quit()

    guesslist = []

    for index in range(0, len(inputargs), 2):
        testword = inputargs[index]
        testresult = inputargs[index + 1]
        testword = testword.lower()  # testwords all lower case
        testresult = testresult.upper()  # The results are input all in capitals
        guesslist.append((testword, testresult))  # Form a list of attempts and results.

    #   Now output the next best trial word or a null string if any errors

    print(nextTry(guesslist, False))
