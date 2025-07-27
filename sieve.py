#
#   Return a list of all the dictionary items
#   that meet the wordle constraints
#


def listintersect(a, b):
    sa = set(a)
    sb = set(b)
    c = sa.intersection(sb)
    return list(c)


def how_many(letterarray, condlist):

    nodups = list(set(letterarray))
    letcounts = {s: 0 for s in nodups}

    for pos, letter in enumerate(letterarray):
        cond = condlist[pos]
        if cond == "Y" or cond == "G":
            letcounts[letter] = letcounts[letter] + 1

    return letcounts


#
#
#   Only search within parts of the string
#   which aren't found yet.


def in_undetermined_peice(status, letter, word):

    for ind in range(0, len(word)):
        try:
            if status[ind] == "-" and word[ind] == letter:
                return True
        except:
            print("ERROR: for status,letter,word, position",status,letter,word,ind)

    return False


def all_5_constraints(word, status, letterarray, condlist):

    if word == "\n":
        return False

    for pos, letter in enumerate(letterarray):
        cond = condlist[pos]

        if cond == "G":
            if letter == word[pos]:
                status[pos] = letter
            else:
                return False

    nodups = list(set(letterarray))
    letcounts = {s: 0 for s in nodups}

    for pos, letter in enumerate(letterarray):
        cond = condlist[pos]
        if cond == "Y":
            letcounts[letter] = letcounts[letter] + 1

    for pos, letter in enumerate(letterarray):
        cond = condlist[pos]
        if cond == "Y":
            if letter == word[pos]:
                return False
            else:
                if letter not in word:
                    return False

        # Only look at B constraints if not mentioned in Ys earlier
        # this isnt perfect but coding for multiple letters is painful
        # and of marginal value

        if cond == "B":
            if letcounts[letter] == 0:
                if in_undetermined_peice(status, letter, word):
                    return False
            else:  # Treat it as a "Y"
                #                print("treat it as a Y")
                if letter == word[pos]:
                    return False
                else:
                    if letter not in word:
                        return False

    #  Multiple letters : find out how many had Y or G against them.
    #  The answer must contain at least that many.

    numerics = how_many(letterarray, condlist)
    for lind in range(0, len(letterarray)):
        letter = letterarray[lind]
        if 0 < numerics[letter]:
            if word.count(letter) < numerics[letter]:
                return False
    return True


#
#   Entry point from outside
#   guesslist : a list of guesses and resulting contraints
#   lines : a set of possible words
#   exclude : words to omit
#   mustbeinhere : a known restricted set the items must also be in
#   Returns a list of items that meet the constraints
#


def sieve(guesslist, lines, exclude, mustbeinhere):
    answers = []

    # Inspect each word in turn

    for index, value in enumerate(lines):
        valid = True

        # increase known position marks so subsequent B / Y searchs can be limited to unknown lettters
        # need to form status array as we work through the results since it alters the meaning of the contraints

        for attempt, testtuple in enumerate(guesslist):

            status = ["-", "-", "-", "-", "-"]

            # Before you do anything, find the lettters whose status is now fixed

            for lind in range(0, len(guesslist[attempt][1])):
                if guesslist[attempt][1][lind] == "G":
                    status[lind] = guesslist[attempt][0][lind]

            # Work through the constraints given by the results to each attempt
            # failing any constraint makes the word unwanted

            if not all_5_constraints(
                value, status, guesslist[attempt][0], guesslist[attempt][1]
            ):
                valid = False

        if valid:
            answers.append(value)

    #       exclude a set of results.  target these to make the worse
    #       case not so bad ... not needed in fact usually exclude is a null list

    for remind, illegal in enumerate(exclude):
        if exclude[remind] in answers:
            answers.remove(exclude[remind])
    return sorted(listintersect(answers, mustbeinhere))


#    return answers
