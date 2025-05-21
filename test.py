#!/usr/bin/python3
#
#   Entry point for the test routine
#   Run the helper algorithm against all possible
#   answers (ones actually used by wordle) to work out our worst case
#
import sys
from collections import Counter
import wordle_helper
import suggest
import wordle


def run_tests(inputargs):
    # Defaults

    hard_mode = False
    use_previous = False

    if "hard" in inputargs:
        print("Hard mode selected")
        hard_mode = True

    if "prev" in inputargs:
        print(
            "Restrict tests to unused answers and use previous results to refine search"
        )
        use_previous = True

    gone_before = wordle_helper.init_previous(use_previous)
    possible_answers = wordle_helper.load_probable_answers()
    testcases = possible_answers  # test against all possibles
    worst = [
        "belly",
        "bound",
        "boxer",
        "brake",
        "bring",
        "broom",
        "catch",
        "chill",
        "fiber",
        "foggy",
        "folly",
        "found",
        "homer",
        "howdy",
        "proxy",
        "roger",
        "wound",
    ]
    #testcases= worst # ["bongo"]

    # restrict to solutions we haven't had yet

    if use_previous:
        testcases = [x for x in testcases if x not in gone_before]

    attempts = []  # Save list of number of moves to provide statistics later
    for target in testcases:  # All of them...
        guesslist = []
        trialwords = []
        tries = 0

        for index in range(1, 10):  # Limited to 10 as a backstop.

            guesslist = wordle.wordle(
                target, trialwords
            )  # Generate what wordle would give you for these trial words ignoring previous answers
            nexttrial = suggest.nextTry(
                guesslist, hard_mode, use_previous
            )  # See what I'd suggest given those results

            # Force initial guess
            # if index == 1:
            #    nexttrial="later"

            trialwords.append(nexttrial)  # Prepare to use it
            if nexttrial == target:  # Success
                tries = index  # Record when
                attempts.append(tries)  # Save for stats
                break  # This ones done...carry on
        print(target, "found in:", tries, "using sequence", trialwords)

        if 6 < tries and not hard_mode:
            print(target, "Fails to solve in 6 tries - pointless continuing ")
            sys.exit()
    print("Number of games:", len(attempts))
    print("Distribution of games:", Counter(attempts))
    print(
        "Giving a solution in this number of tries on average:",
        round(wordle_helper.average(Counter(attempts)), 4),
    )


if __name__ == "__main__":
    """Wordle solver test program"""
    print("Wordle solver testing")
    # Defaults

    hard_mode = False
    use_previous = False

    wordletest = sys.argv.pop(0)
    inputargs = sys.argv

    if "all" in inputargs:
        print("Run tests in all conditions to drive test coverage stats")
        run_tests([])
        run_tests(["prev"])
        run_tests(["hard"])
        run_tests(["prev", "hard"])
        sys.exit()
    else:
        run_tests(inputargs)
