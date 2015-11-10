__author__ = 'federicamoscato'

import argparse
from datetime import datetime
import pymongo

import sys
sys.path.insert(0, "../")

import pubblicazioniASDC.userDAO as userDAO


connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string)
database = connection.publication
users = userDAO.UserDAO(database)


class AuthorException(ValueError):
    pass


class InsertError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class Admin(object):

    def __init__(self, **parameters):

         for name, value in parameters.iteritems():
            setattr(self, name, value)



def insertIntoDB(admin):

     return users.add_user(name=admin.name, lastname=admin.lastname,
                           start_date=admin.start_date, password=admin.password,
                           username='admin',
                           email=admin.email,
                           missions=[],
                           admin=True)



def valid_date(s):
    """"
    Validation of the command line options.
    Check if a date is of the right format
    e.g. = 2013-01-08T15:39:05.169
    Arg: string
    Return: string
    Raise ArgumentTypeError
    """

    try:
        datetime.strptime(s, "%d/%m/%Y")
        #date string is well formatted
        return s
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def main(parser):

   args = parser.parse_args()

   #creates the NASAQuery obj
   admin = Admin()
   # Parse the arguments and directly load in the NASAQuery namespace
   args = parser.parse_args(namespace=admin)

   if insertIntoDB(admin):
       print "Inserted admin with password : %s" % admin.password

   else:
       print "An error occured"



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Admin creation for the publication tool")
    # Define the command line options

    requiredNamed = parser.add_argument_group('required  arguments')

    requiredNamed.add_argument('--name', help="admin name ", required=True)
    requiredNamed.add_argument('--lastname', help="admin lastname ", required=True)
    requiredNamed.add_argument('--start_date', help="admin start_date (format: %d/%m/%Y)",  type=valid_date,
                               required=True)
    requiredNamed.add_argument('--email', help="admin email ", required=True)

    requiredNamed.add_argument('--password',  help="admin password",
                               required=True)

    main(parser)
