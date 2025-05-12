#!/usr/bin/python3
""" Call wordle_helper with hard mode flag set True """

import os
from contextlib import chdir

if __name__ == "__main__":

    # The data and .py files should be in the same directory as the executable.
    # Find out where

    directory = os.path.dirname(__file__)

    # Change directory to where all the other files are

    with chdir(directory):
        import wordle_helper

        wordle_helper.print_hi("Wordle helper/solver/assistant (hard mode)\n")
        retVal = wordle_helper.main(True,False)
