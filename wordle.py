#!/usr/bin/python3
#
#   I need an implmentation of the wordle rules
#   in order to test my wordle helper (solver)
#   Example usage:
#
#   ./wordle.py later lemon
# gives output
#   Wordle
#   later [('lemon', 'GYBBB')]


import sys
import sieve


def wordle(target, guesses):

    state = ["-", "-", "-", "-", "-"]
    resultlist = []

    for value in guesses:

        results = ["-", "-", "-", "-", "-"]
        nodups = list(set(value))
        letcounts = {s: target.count(s) for s in nodups}

        for index in range(0, len(value)):
            if value[index] == target[index]:
                letcounts[value[index]] = letcounts[value[index]] - 1
                results[index] = "G"
                state[index] = value[index]

        for index in range(0, len(value)):
            if not sieve.in_undetermined_peice(state, value[index], target):
                if results[index] == "-":
                    results[index] = "B"

        #   Count occurrences of each letter
        #
        #   Cases where multiple same letter appears in the guess require care
        #   Y's get handed out until the count of them in the target is exhausted
        #   then they get greyed out.

        for index in range(0, len(value)):
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
        quit()

    target = inputs.pop(0)
    print(target, wordle(target, inputs))
