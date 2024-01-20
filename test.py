#!/usr/bin/python3
#
#   Entry point for the test routine
#   Run the helper algorithm against all possible
#   answers (ones actually used by wordle) to work out our worst case
#
import wordle_helper
import suggest
import wordle
from collections import Counter


if __name__ == "__main__":

    print("Wordle solver testing")

    possible_answers = wordle_helper.load_possible_answers()
    testcases = possible_answers  # test against all possibles

    attempts = []  # Save list of number of moves to provide statistics later
    for target in testcases:  # All of them...
        guesslist = []
        trialwords = []
        tries = 0

        for index in range(1, 10):  # Limited to 10 as a backstop.

            guesslist = wordle.wordle(
                target, trialwords
            )  # Generate what wordle would give you for these trial words
            nexttrial = suggest.nextTry(
                guesslist
            )  # See what I'd suggest given those results
            trialwords.append(nexttrial)  # Prepare to use it
            if nexttrial == target:  # Success
                tries = index  # Record when
                attempts.append(tries)  # Save for stats
                break  # This ones done...carry on
        print(target, "found in:", tries, "using sequence", trialwords)

        if 6 < tries:
            print("Fails to solve in 6 tries - pointless continuing ")
            exit()

    print("Distribution of games:", Counter(attempts))
    print(
        "Giving a solution in this number of tries on average:",
        round(wordle_helper.average(Counter(attempts)), 4),
    )
