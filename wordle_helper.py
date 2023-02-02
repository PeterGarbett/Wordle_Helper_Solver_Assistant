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


def report(answers, limited):

    if answers == []:
        print("No solutions, probable constraint conflict")
        quit()

    if 1 == len(answers):
        print(len(answers), " word satisfies the constraints and it is :", answers[0])
        return True
    else:
        print(len(answers), " words satisfy the constraints and they are:\n", answers)


    if limited==[]:
        print("None of these are actually known to be wordle answers")
        return True     #Suppress trying to find best trial word
    else:
        print("When restricted to words actually known to be wordle answers:")

    if 1 == len(limited):
        print("One wordle word satisfies the constraints and it is :", limited[0])
        return True
    else:
        if len(limited) == 2:
            print("(The answer is one of these):", limited)
        else:
            print(
                "There are ",
                len(limited),
                " wordle solution words that satisfy the constraints and they are:\n",
                limited,
            )

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


def best_trial_words(guesslist, answers, lines):
    global index, value

    # Fish out easy cases first.
    # No answers,1 answer (so it is the answer),and two answers
    # in which case the best trial word is to pick one.

    if answers == []:
        return []

    if len(answers) <= 2:
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
    # representing how well it includes unkown letters that are likeliest
    # to be found

    scores = []
    for index, value in enumerate(lines):
        letter = list(set(value))
        best = 0
        for num, tar in enumerate(letter):
            best = best + frequencies[tar]  # + nice
        scores.append([best, value])
    scores = sorted(scores)

    #
    # Pick from the top items that have a reasonable score
    # This is based on a frequency count of letters occurring
    # about which we currenly know nothing.  This is a pretty
    # simple minded idea that works surprisingly well

    candidates = []
    top_score = scores[-1][0]
    for highscore in range(1, 10):
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


lines = []
full_list = []
exclude = []


# load a large list of 5 letter words


def init_files():
    with open("wordle-valid-words.txt") as f:
        lines = f.readlines()
    # Remove all the pesky \n's
    lines = [x.replace("\n", "") for x in lines]
    return lines


# load a much smaller list of words used as wordle answers


def load_possible_answers():
    with open("wordle-answers-alphabetical.txt") as f:
        lines = f.readlines()
    # Remove all the pesky \n's
    lines = [x.replace("\n", "") for x in lines]
    return lines


def init_exclusions():

    #
    #   One thing we know about wordles is they dont use
    #   the same word twice. This can be used to speed up the search
    #   but isnt appropriate for quordle and is a bit of a hack
    #   Uncomment the next line if you really want to do this

    return []
    #
    #   read list of words to exclude
    #
    #
    with open("gone.txt") as g:
        exclude = g.readlines()
    # Remove all the pesky \n's
    exclude = [x.replace("\n", "") for x in exclude]
    for pos in range(len(exclude)):
        exclude[pos] = exclude[pos].lower()

    return exclude


def main():
    global guesslist, index, lines, full_list, exclude, answers, scores, post, promote
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

    lines = init_files()
    full_list = lines
    exclude = init_exclusions()
    possible_answers = load_possible_answers()

    #   We want a search of all words, not just the ones that
    #   happen to be used as answers.
    #   so do this 1st and then use intersection with possible answers if needed
    #   Sorting is there just to make output pleasant (The intersection scrambles it)

    answers = sieve.sieve(guesslist, lines, exclude, lines)  # possible_answers)
    limited = sorted(sieve.listintersect(answers, possible_answers))

    # answers = full_list

    solved = report(answers, limited)  # Wordy report of possibilities left

    if not solved and 1 < len(answers):
        scores = best_trial_words(guesslist, limited, possible_answers)
        print("Suggested trial word:", scores[-1][1])


#
#   Entry point for suggest.py
#


def suggestion(guesslist):

    lines = init_files()
    exclude = []
    possible_answers = load_possible_answers()

    #   Form a list of wordle solution words that satisfy the constraints

    answers = sieve.sieve(guesslist, lines, exclude, possible_answers)
    scores = best_trial_words(guesslist, answers, possible_answers)

    return scores


if __name__ == "__main__":
    print_hi("Wordle helper/solver/assistant")
    main()
