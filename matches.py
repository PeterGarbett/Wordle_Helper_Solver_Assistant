""" 
Posting solutions as colours is common, lets see if we can
find what words they have used.  Search amongst known wordle solutions
first.. A much smaller list but misses out obvious things including plurals
"""

import sys
import wordle


def find_in_dictionary(target, want, wrds):
    """find words in the dictionary that match the wanted pattern given a known target solution"""

    with open(wrds, encoding="ascii") as candidates:
        wordle_words = candidates.readlines()
        words = [x.replace("\n", "") for x in wordle_words]

    candidates.close()

    solutions = []

    for try_this in words:
        inputs = [try_this]

        result = wordle.wordle(target, inputs)
        pair = result[0]

        if pair[1] == want:
            solutions.append(try_this)

    return solutions


def find_matchs():
    """find words that match those colours in both word lists"""

    print("\nFind words that match a pattern given we know the solution\n")

    sys.argv.pop(0)

    inputs = sys.argv

    if not inputs:
        print("Missing calling parameters")
        print("./matches  solution  colors")
        sys.exit()

    target = inputs.pop(0)
    want = inputs[0].upper()
    wrd_list = "wordle-answers-alphabetical.txt"

    solutions = find_in_dictionary(target, want, wrd_list)
    how_many = len(solutions)

    print(
        "Solution is :",
        target,
        ", guess has colours:",
        want,"\n",how_many,
        " possibles among words known to be wordle answers which are:\n",
        solutions,
        "\n",
    )

    wrd_list = "wordle-valid-words.txt"
    solutions = find_in_dictionary(target, want, wrd_list)
    how_many = len(solutions)

    print(
        "Solution is :",
        target,
        ", guess has colours:",
        want,"\n",how_many,
        " possibles among valid words which are:\n",
        solutions,
    )


if __name__ == "__main__":
    find_matchs()
