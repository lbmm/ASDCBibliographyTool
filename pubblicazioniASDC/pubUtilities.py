__author__ = 'fmoscato'

"""
utilities module for the publications project
"""

import os

def str2bool(string):
    return string in ('true', 'T', 'True', 'Y', 1)

def find_nth(s, x, n):
    """
    find the nth occurence in a string
    takes string where to search, substring, nth-occurence
    """
    i = -1
    for _ in range(n):
        i = s.find(x, i + len(x))
        if i == -1:
            break
    return i


def clean_string(a_str):
    """
    remove left/right white spaces, special characters
    @param : string from the form
    @return : clean string
    """

    a_str = a_str.replace('\n', '')
    a_str = a_str.replace('\r', '')
    a_str = a_str.rstrip()
    a_str = a_str.lstrip()

    return a_str


def sendMail(to, sub, body):
    """
    TODO: here update the sender !!!
    """
    sendmail_location = "/usr/sbin/sendmail" # sendmail location
    p = os.popen("%s -t" % sendmail_location, "w")
    p.write("From: %s\n" % "moscato@asdc.asi.it")
    p.write("To: %s\n" % to)
    p.write("Subject: %s \n" % sub)
    p.write("\n") # blank line separating headers from body
    p.write(body)
    p.close()

    return True
