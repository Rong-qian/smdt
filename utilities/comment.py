###############################################################################
#   File: cleanup.py
#   Author(s): Paul Johnecheck
#   Date Created: 02 May, 2021
#
#   Purpose: This simple script just wipes the new_data and the locks directory.
#   Crashed or prematurely ended programs can leave data here that can mess with things.
#   This should only be ran while developing, this can and will cause data to not get put into the database.
#   DO NOT RUN THIS FILE IN THE REAL LAB IF YOU KNOW WHAT YOU'RE DOING!!!!!
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################


import os
import sys
import datetime

DROPBOX_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(DROPBOX_DIR)

from sMDT import db, tube, mini_tube
from sMDT.data.status import ErrorCodes


def YN_answer_loop(string):
    """
    Gets a yes/no response from the user. Returns true if yes.
    """
    answer = ""
    answer = input(string)
    while answer.lower() not in ['y', 'n']:
        print("Answer not of the form (Y/N).")
        answer = input(string)
    return answer.lower() == 'y'


def answer_loop(string, options):
    """
    Gets an answer from the user
    """
    answer = ""
    answer = input(string)
    while answer.lower() not in options:
        print("Lowercase input is not in ", options, ", try again.\n")
        answer = input(string)
    return answer.lower()

if __name__ == "__main__":
    database = db.db()
    tubeID = input("Which tube would you like to comment on?\n")
    try:
        tube1 = database.get_tube(tubeID)
        print()
        print(tube1)
        if YN_answer_loop("Would you like to add a comment to this tube? (Y/N)\n"):
            comment = input("What is your comment?\n")
            if YN_answer_loop("Would you still like to add the above comment to the tube? (Y/N)\n"):
                tube2 = mini_tube.Mini_tube()
                tube2.set_ID(tubeID)
                for code in ErrorCodes:
                    print(int(code), code.name)
                codeChoice = int(answer_loop("Choose an error code:\n", [str(int(i)) for i in ErrorCodes]))
                user = input("Enter your name:\n")
                tube2.new_comment((comment, user, datetime.datetime.now(), ErrorCodes(codeChoice)))
                database.add_tube(tube2)

                input("Comment added.\nPress enter to continue...")
            else:
                input("\nPress enter to continue...")
        else:
            input("\nPress enter to continue...")


    except KeyError:
        input("No tube with that ID found.\nPress enter to continue...")
