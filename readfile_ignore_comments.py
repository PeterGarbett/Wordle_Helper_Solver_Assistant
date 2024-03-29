#!/usr/bin/python3

#
#   Code for reading file ignoring anything following an octothorp
#   and any trailing whitespace after its removal
#
#   Motivated by the desire to annotate the previous answe list
#


def stripString(commented_line, changeCase):

#   Parse option to change case

    if changeCase == -1:
        commented_line = commented_line.lower()
    else:
        if changeCase == 1:
            commented_line = commented_line.upper()

# Only interested in the first item delimited by a #

    cleaved = commented_line.split("#")
    commented_line = cleaved[0].strip()

    return commented_line

#
#   If we can't find the file, return a [] and don't generate an exception
#   This doesnt affect the algorithm in any crucial way


def readfile_ignore_comments(diskname, changeCase):

    try:
        #   read list of words to exclude
        with open(diskname) as g:
            exclude = g.readlines()
            g.close()

            # Remove all the pesky \n's

            exclude = [x.replace("\n", "") for x in exclude]

            # Make list case independent

            for pos in range(len(exclude)):
                exclude[pos] = stripString(exclude[pos], changeCase)

            # If theres now no string left, ignore it
            exclude = list(filter(None, exclude))

            return exclude

    except FileNotFoundError :
        return []

    except Exception as err:
        print(err)

    return []


def main():
    exl = readfile_ignore_comments("previous-answers.txt", -1)
    print(exl)


if __name__ == "__main__":
    print("test readfile no comments \n")
    main()
