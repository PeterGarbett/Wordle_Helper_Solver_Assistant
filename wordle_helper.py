#!/usr/bin/python3
#
#   WORDLE HELPER
#
#   Suggest words to try to determine unknown letters.
#
#
import sys
import wordle
import sieve
from functools import reduce
from operator import concat
from collections import Counter
import suggest
import readfile_ignore_comments

# Use list of previous answers. This is only
# used to determine a best guess when the answer is down to a pair


use_previous = True

# The main word list files

wordle_answers_alphabetical = "wordle-answers-alphabetical.txt"
wordle_valid_words = "wordle-valid-words.txt"


status = ["-", "-", "-", "-", "-"]

# Form list of characters from a string


def split(word):
    return [char for char in word]


def print_hi(name):

    # Use a breakpoint in the code line below to debug your script.
    print(f"{name}")  # Press Ctrl+F8 to toggle the breakpoint.


def usage():

    print("./wordle_helper  guess1  result1 guess2 result2 .... ")
    print("where guess<n> are 5 letter trial words and")
    print("result<n> are 5 letter strings composed of y g and b")


#
#   Report the findings. Made messy by the fact that
#   we know there are words that satisfy the constraints
#   but are never used as answers
#


def turned_up_earlier(candidates, gone_before):

    # Candidates is a small list and gone_before is larger...

    usage = []

    for index in range(len(candidates)):
        if candidates[index] in gone_before:
            usage.append(candidates[index])

    return usage


def report(answers, limited, genTrial, gone_before):

    if answers == []:
        print("No solutions, probable constraint conflict")
        quit()

    if 1 == len(answers):
        print(len(answers), " word satisfies the constraints and it is :", answers[0])
        return True
    else:
        print(len(answers), " words satisfy the constraints and they are:\n", answers)

        if 50 <= len(answers):
            print("Number of solutions=", len(answers))

        print("Suggested trial word for this list:", genTrial, "\n")

    if limited == []:
        print("None of these are actually known to be wordle answers")
        return False
    else:
        print("When restricted to words actually known to be wordle answers,")

    if 1 == len(limited):
        print("one wordle word satisfies the constraints and it is :", limited[0])
        return True
    else:
        if len(limited) <= 10:
            print(
                "There are ",
                len(limited),
                " probable answers which are :",
                limited,
                "\n",
            )
            before = turned_up_earlier(limited, gone_before)
            if len(before) != 0:
                if use_previous:
                    print(
                        "Of these, these have previously been  used as wordle solutions:",
                        before,
                    )
                    candidates = [x for x in limited if x not in before]
                    if candidates == []:
                        print(
                            "which is all of them, so perhaps they have reused an answer or added an extra"
                        )
                    else:
                        print("leaving these more likely:", candidates)
        else:
            print(
                "There are ",
                len(limited),
                " wordle solution words that satisfy the constraints and they are:\n",
                limited,
            )
            if 50 <= len(limited):
                print("Number of solutions=", len(limited))

    return False


def Yscore(word, Ylist):

    niceness = 0

    for Yitem in Ylist:
        position = word.find(Yitem[0])
        # if position isnt in the list, its nice
        if 0 <= position:
            if position not in Yitem[1]:
                niceness = niceness + 1

    return niceness


def average(freqs):

    vals = freqs.values()
    denom = sum(vals)

    sumit = 0
    for ind in freqs.items():
        product = ind[0] * ind[1]
        sumit = sumit + product

    av = sumit / denom
    return av


# Split the list of strings out into individual characters and count them


def freqs(mylist):
    charlist = list(map(split, mylist))
    #    print(charlist)
    if charlist != []:
        flatlist = reduce(concat, charlist)
    else:
        flatlist = []
    frequencies = Counter(flatlist)
    #    print(frequencies)
    return frequencies


#   Form frequency table of valid words


def best_trial_words(guesslist, answers, pick_list, gone_before, hard_mode=False):
    """guesslist : previous guesses and results
    answers   : list of words matching the constraints
    pick_list : list to pick trial words from
    gone_before :   list of previous results"""

    global index, value

    # Fish out easy cases first.
    # No answers,1 answer (so it is the answer),and two answers
    # in which case the best trial word is to pick one.

    if answers == []:
        return []

    if len(answers) == 1:
        scores = [[1, answers[0]]]  # construct the required wrapper for the answer
        return scores

    #   Use if somethings appeared before to improve your chances when you are down to a pair

    if len(answers) == 2:

        # Default to first of the pair but use the other answer if its a previous answer

        if answers[0] in gone_before:
            scores = [[1, answers[1]]]  # construct the required wrapper for the answer
        else:
            scores = [[1, answers[0]]]  # construct the required wrapper for the answer

        return scores

    #
    # If we are still here, have a non trivial list to look at
    # so find out whats likely to be useful letters to have information about
    #

    frequencies = freqs(answers)
    status = ["-", "-", "-", "-", "-"]
    Ystatus = ["-", "-", "-", "-", "-"]

    #   Improve status array where letters are known by virtue of being the same
    #   in all contrained words

    #
    #   Produce a list of all the letters that have been tried
    #
    allLetterGuesses = []
    for wrdpos in range(len(guesslist)):
        allLetterGuesses.append(guesslist[wrdpos][0])
    charlist = list(map(split, allLetterGuesses))
    if charlist != []:
        flatlist = reduce(concat, charlist)
        lettersTried = list(set(flatlist))
    else:
        lettersTried = []

    # Now work out if we know they are in there but dont know where
    # (ignoring repeated letters since they are pesky)
    # by removing things having a B or G result

    trials = []
    for wrdpos in range(len(guesslist)):
        for letpos in range(len(guesslist[0][0])):
            trial = (letpos, guesslist[wrdpos][0][letpos], guesslist[wrdpos][1][letpos])
            #            print(trial)
            trials.append(trial)

    notinteresting = []

    for trl in trials:
        if trl[2] == "B":
            notinteresting.append(trl[1])
        if trl[2] == "G":
            notinteresting.append(trl[1])
    boring = list(set(notinteresting))

    for getrid in boring:
        lettersTried.remove(getrid)

    keyList = []

    for trite in lettersTried:
        testpositions = []
        for trl in trials:
            if trite == trl[1]:
                testpositions.append(trl[0])
        tested = (trite, list(set(testpositions)))
        keyList.append(tested)

    # keyList is now a list of tuples of letters we know are in there
    # and a list of locations we have tried and fail.
    # use to assign a score for best placement of Y letters later

    # Check the 5 letter positions

    if answers == []:
        return []

    for letpos in range(len(answers[0])):
        letterissame = True
        candidate = answers[0][letpos]
        for wrdpos in range(len(answers)):
            if candidate != answers[wrdpos][letpos]:
                candidate = "-"
                letterissame = False
        if letterissame:
            status[letpos] = candidate

    known_letters = set(status)  #   Remove duplicates from known letters
    known_letters.discard("-")  # and the symbol for unknown
    known = list(known_letters)  # to produce a list of known letters

    # Remove known letters, i'm not interested in trying to find them
    # Just reply on the accummulation of constraints for now to narrow down result
    # This will inadvertantly remove letters of interest if they are repeats
    for knwn in known:
        del frequencies[knwn]
    # Now assign a score to each word in the complete wordle list
    # representing how well it includes unknown letters that are likeliest
    # to be found

    if hard_mode:
        allowed_guesses = answers
    else:
        allowed_guesses = pick_list

    scores = []
    for index, value in enumerate(allowed_guesses):
        letter = list(set(value))
        best = 0
        for num, tar in enumerate(letter):
            best = best + frequencies[tar]  # + nice
        scores.append([best, value])
    scores = sorted(scores)

    #
    # Pick from the top items that have a reasonable score
    # This is based on a frequency count of letters occurring
    # about which we currently know nothing.  This is a pretty
    # simple minded idea that works surprisingly well

    # The way we form the list 'scores' means
    # its size is len(candidates)

    candidates = []
    top_score = scores[-1][0]

    samples = min(len(scores), 10)

    for highscore in range(1, samples):
        if top_score - 60 <= scores[-highscore][0]:
            candidates.append(scores[-highscore])
    #
    #   and from these prefer ones that change where
    #   Letters labelled Y appear so more information
    #   is revealed by its use as a trial word.

    for item in candidates:
        item[0] = item[0] + Yscore(item[1], keyList)
    candidates = sorted(candidates)

    return candidates


valid_words = []
full_list = []
exclude = []

# load a large list of 5 letter words


def init_valid_words():
    with open(wordle_valid_words) as f:
        valid_words = f.readlines()
        f.close()
    # Remove all the pesky \n's
    valid_words = [x.replace("\n", "") for x in valid_words]
    return valid_words


# load a much smaller list of words used as wordle answers


def load_probable_answers():
    with open(wordle_answers_alphabetical) as f:
        valid_words = f.readlines()
        f.close()
    # Remove all the pesky \n's
    valid_words = [x.replace("\n", "") for x in valid_words]
    return valid_words

    #
    #   One thing we know about wordles is they dont use
    #   the same word twice. This can be used to speed up the search
    #   but isnt appropriate for quordle and is a bit of a hack
    #   It also will need revision or removal when words start
    #   repeating as a matter of course.

    # However...  if the search comes down to a choice of two
    # it can be a nice bit of information to have
    # as a guide...  so I've resurrected this idea
    # after getting fed up of choosing the wrong one of a pair a few times.

    # Attempt to open previous guess list
    # if such an attempt is requested
    # but fall back gracefully to not using it if its
    # not found


def init_previous(use_previous):

    # Check if we need to do this..

    if not use_previous:
        return []

    previous_answers = "previous-answers.txt"
    prevList = readfile_ignore_comments.readfile_ignore_comments(previous_answers, -1)

    if prevList == []:
        use_previous = False

    return prevList


def main(hard):
    global guesslist, index, valid_words, full_list, exclude, answers, scores, post, promote

    # Pick up word/result pairs from the command line

    caller = sys.argv.pop(0)
    inputargs = sys.argv

    # Make sure we have pairs of inputs

    if (len(inputargs) % 2) != 0:
        print("ERROR: Missing input argument")
        usage()
        quit()

    # Form list of testword/result tuples
    # include error checking and reporting : unlike similar code in suggest.py

    guesslist = []
    for index in range(0, len(inputargs), 2):
        #    print(inputargs[index])
        testword = inputargs[index]
        testresult = inputargs[index + 1]

        #   Input length tests

        if len(testword) != 5:
            print("Test word ", testword, " fails length test")
            usage()
            quit()

        if len(testresult) != 5:
            print("Test result ", testresult, " fails length test")
            usage()
            quit()

        # The wordlist is all in lower case
        # so ensure the testword is

        testword = testword.lower()  # The results are input all in capitals
        if not suggest.good_guess(testword):
            print("Bad trial word ", testword)
            usage()
            quit()

        testresult = testresult.upper()
        if not suggest.good_colours(testresult):
            print("Incorrect wordle report ", testresult)
            usage()
            quit()

        # Form a list of attempts and results.

        guesslist.append((testword, testresult))

    valid_words = init_valid_words()
    full_list = valid_words
    gone_before = init_previous(True)
    probable_answers = load_probable_answers()

    #   We want a search of all words, not just the ones that
    #   happen to be used as answers.
    #   so do this 1st and then use intersection with probable answers if needed
    #   Sorting is there just to make output pleasant (The intersection scrambles it)

    answers = sieve.sieve(guesslist, valid_words, [], valid_words)  # probable_answers)
    limited = sorted(sieve.listintersect(answers, probable_answers))

    if 1 < len(answers):
        scores = best_trial_words(guesslist, answers, probable_answers, gone_before, hard)
        genTrial = scores[-1][1]
    else:
        genTrial = ""

    #    print("Suggested trial word for general list :",genTrial)

    solved = report(
        answers, limited, genTrial, gone_before
    )  # Wordy report of possibilities left

    if not solved:
        if 1 < len(limited):
            scores = best_trial_words(
                guesslist, limited, probable_answers, gone_before, hard
            )
            trial_word = scores[-1][1]
            print("Suggested trial word for known answers:", trial_word)

            candidates = [x for x in limited if x not in gone_before]

            if 0 != len(candidates) and len(candidates) != len(limited):
                print(
                    "There are ",
                    len(candidates),
                    " wordle solutions after removing previously used answers",
                )
                scores = best_trial_words(
                    guesslist, candidates, limited, gone_before, hard
                )
                print(candidates)
                trial_word2 = scores[-1][1]
                if trial_word != trial_word2:
                    print(
                        "Suggested trial word ",
                        trial_word,
                        " modified by excluding previous answers which suggest a better word may be:",
                        trial_word2,
                    )
                else:
                    print(
                        "Suggested trial word ",
                        trial_word,
                        "unchanged by considering previous answers",
                    )
        else:  # Suggest a trial word in the case where no known answers fit
            scores = best_trial_words(
                guesslist, answers, probable_answers, gone_before, hard
            )
            print("Now its down to spot the new wordle word")
            print("Suggested trial word:", scores[-1][1])


#
#   Entry point for suggest.py
#


def suggestion(guesslist, hard, use_previous):

    valid_words = init_valid_words()
    gone_before = init_previous(use_previous)
    probable_answers = load_probable_answers()

    #   Form a list of wordle solution words that satisfy the constraints

    answers = sieve.sieve(guesslist, valid_words, [], probable_answers)
    scores = best_trial_words(guesslist, answers, probable_answers, gone_before, hard)

    return scores


import os
from contextlib import chdir

if __name__ == "__main__":

    # The data and .py files should be in the same directory as the executable.
    # Find out where

    directory = os.path.dirname(__file__)

    # Change directory to where all the other files are

    with chdir(directory):
        print_hi("Wordle helper/solver/assistant\n")
        main(False)
