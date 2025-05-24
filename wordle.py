#!/usr/bin/python3
#
''' #   I need an implementation of wordle
#   in order to test my wordle helper (solver)
#   Sanity checks added which are hopefully only
#   tripped from command line inputs
#
#   Example usage:
#
#   ./wordle.py later lemon
# gives output
#   Wordle
#   later [('lemon', 'GYBBB')]
'''

import sys
import sieve


def wordle(target, guesses):
    '''   An implementation of wordle '''

    state = ["-", "-", "-", "-", "-"]
    resultlist = []

    for value in guesses:

        results = ["-", "-", "-", "-", "-"]
        nodups = list(set(value))
        letcounts = {s: target.count(s) for s in nodups}

        if 5 != len(value):
            return []

        for index, val in enumerate(value):
            if value[index] == target[index]:
                letcounts[value[index]] = letcounts[value[index]] - 1
                results[index] = "G"
                state[index] = value[index]

        for index, val in enumerate(value):
            if not sieve.in_undetermined_peice(state, value[index], target):
                if results[index] == "-":
                    results[index] = "B"

        #   Count occurrences of each letter
        #
        #   Cases where multiple same letter appears in the guess require care
        #   Y's get handed out until the count of them in the target is exhausted
        #   then they get greyed out.

        for index, val in enumerate(value):
            if results[index] != "G":
                if 0 < letcounts[value[index]]:
                    results[index] = "Y"
                else:
                    results[index] = "B"
                letcounts[value[index]] = letcounts[value[index]] - 1

        resultlist.append((value, "".join(results)))

    return resultlist


if __name__ == "__main__":
    print("Wordle")

    wordletest = sys.argv.pop(0)

    inputs = sys.argv

    if inputs == []:
        print("Missing calling parameters")
        print("./wordle  target_word  guess1 etc ....")
        sys.exit()

    target = inputs.pop(0)
    result = wordle(target, inputs)

    if not result:
        print("Invalid inputs")
        sys.exit()

    print(target, wordle(target, inputs))
