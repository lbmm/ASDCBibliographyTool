_author_ = 'fmoscato'


import random
import string
import hashlib
from datetime import datetime

import pymongo.errors

import constants as c
import pubUtilities

# The User Data Access Object handles all interactions with the User collection.


class UserDAO(object):

    def __init__(self, db):
        self.db = db
        self.users = self.db.users

    @staticmethod
    def make_salt():
        salt = ""
        for i in range(5):
            salt = salt + random.choice(string.ascii_letters)
        return salt

    def make_pw_hash(self, pw, salt=None):
        if not salt:
            salt = self.make_salt()
        return hashlib.sha256(pw + salt).hexdigest()+"," + salt

    @staticmethod
    def pub_name(name, lastname):
        #this is for compost name
        name_array = name.split()
        #the replace is needed to handle double lastname
        pub_name_array = []
        pub_lastname = (lastname.title()).replace(" ", "+")
        # 1. Lastname  %2C F.
        pub_name_array.append(pub_lastname + "%2C" + '.'.join([n[:1].upper() for n in name_array]))
        #2. Lastname %2C FirstName
        pub_name_array.append(pub_lastname + "%2C" + name.title().replace(" ", "+"))

        #3. Any combination of the Lastname + name and middlename
        if len(name_array) > 1:
            for n in name_array:
               pub_name_array.append(pub_lastname + "%2C" + n[:1] + '.')
               pub_name_array.append(pub_lastname + "%2C" + n.title())

        return pub_name_array

    # Validates a user login. Returns user record or None
    def validate_login(self, username, password):

        user = None
        try:
            user = self.users.find_one({'_id': username})
        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False

        if not user:
            print "User not in database"
            return None

        salt = user['password'].split(',')[1]

        if user['password'] != self.make_pw_hash(password, salt):
            print "user password is not a match"
            return None

        # Looks good
        return user

    def get_admin_email(self):

        cursor = self.users.find_one({'admin': True})

        return cursor['email']


    def get_users(self, date_format=None):
      
        cursor = self.users.find({'admin': False}).sort('lastname', direction=1)
        date_format_str = "%B %Y"
        if date_format:
            date_format_str = date_format

        l = []

        for user in cursor:

            usr = {'username': user['_id'], 'name': user['name'], 'lastname': user['lastname'],
                   'email': user['email'],
                   'start_date': user['start_date'].strftime(date_format_str),
                   'end_date': user['end_date'].strftime(date_format_str),
                   'missions': user['missions'],
                   'pub_name': user['pub_name'],
                   'role': user.get('role', '')}

            l.append(usr)

        return l

    def get_user(self, _id):

        cursor = self.users.find_one({'_id': _id})

        user = None

        if cursor:

            user = {'username': cursor['_id'], 'name': cursor['name'], 'lastname': cursor['lastname'],
                    'email': cursor['email'],
                    'start_date': cursor['start_date'].strftime(c.DATE_FORMAT),
                    'end_date': cursor['end_date'].strftime(c.DATE_FORMAT),
                    'missions': cursor.get('missions', []),
                    'pub_name': cursor['pub_name'],
                    'role': cursor.get('role', '')}
        return user

    #from a list check if the users are valide in a period of time
    # return list of valid users
    def check_users_validity(self, users, start_date, end_date):

        l = []

        try:

            cursor = self.users.find({'_id': {'$in': users},
                                      'start_date': {'$lte': start_date},
                                      'end_date': {'$gte': end_date},
                                      'admin': False}, {'admin': 0, 'password': 0})
            for user in cursor:

                usr = {"username": user['_id'], "name": user['name'],
                       "lastname": user['lastname'],
                       "email": user['email'],
                       "start_date": user['start_date'].strftime("%B %Y"),
                       "end_date": user['end_date'].strftime("%B %Y"),
                       "pub_name": user['pub_name'],
                       "missions": user['missions'],
                       "role": user.get('role', '')}

                l.append(usr)

        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False

        return l



    #get valide users for a time period
    def get_valide_users(self, start_date=None, end_date=None):

        l = []

        try:
            #no admin. Admins show up in the get_users list
            if not start_date and not end_date:

                today = datetime.now()

                cursor = self.users.find({'end_date': {"$gte": today}, 'admin': False}, {'admin': 0, 'password': 0})
            else:

                cursor = self.users.find({'start_date': {'$lte': start_date},
                                          'end_date': {'$gte': start_date},
                                          'admin': False}, {'admin': 0, 'password': 0})
            for user in cursor:

                usr = {"username": user['_id'], "name": user['name'],
                       "lastname": user['lastname'],
                       "email": user['email'],
                       "start_date": user['start_date'].strftime("%B %Y"),
                       "end_date": user['end_date'].strftime("%B %Y"),
                       "pub_name": user['pub_name'],
                       "missions": user['missions'],
                       "role": user.get('role', '')}

                l.append(usr)

        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False

        return l

    def remove_user(self, _id):

        try:

            print "removing user %s" % _id
 
            self.users.remove({'_id': _id})
  
        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False
    
        return True 
      
    def close_validity_user(self, _id):

        today = datetime.now()

        try:
            self.users.update({'_id': _id}, {'$set': {"end_date": today}})

        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False
         
        return True

    def update_email(self, _id, email):

        try:
            self.users.update({'_id': _id}, {'$set': {'email': email}})
        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False

        return True

    def update_missions(self, _id, missions_list):

        try:
            self.users.update({'_id': _id}, {'$set': {'missions': missions_list}})

        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False

        return True

    def update_role(self, _id, role):

        try:
            self.users.update({'_id': _id}, {'$set': {'role': role}})
        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False

        return True

    #update pub_name
    def update_publication_name(self, _id, pub_name):

        try:
            self.users.update({'_id': _id}, {'$set': {'pub_name': pub_name}})
        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False

        return True

    # creates a new user in the users collection
    def add_user(self, **kwargs):

        pwd = kwargs['password']
        password_hash = self.make_pw_hash(pwd)

        user = {'_id': kwargs['username'], 'password': password_hash, 
                'name': kwargs['name'], 'lastname': kwargs['lastname'],
                'pub_name': self.pub_name(kwargs['name'], kwargs['lastname']),
                'email': kwargs['email'],
                'admin': kwargs['admin'],
                'start_date': datetime.strptime(kwargs['start_date'].rstrip(), c.DATE_FORMAT),
                'missions': kwargs['missions'],
                'role': kwargs.get('role', '')}

        if 'end_date'in kwargs and kwargs['end_date'] != '':
            user['end_date'] = datetime.strptime(kwargs['end_date'], c.DATE_FORMAT)
        else:
            date1 = datetime.strptime(c.END_DATE, c.DATE_FORMAT)
            user['end_date'] = date1
        try:
            self.users.insert(user)
        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False
        except pymongo.errors.DuplicateKeyError:
            print "oops, username is already taken"
            return False

        return True

    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def create_tmp_password(self, _id):
        """
        creates a new password and updating the DB with the new pwd
        sent email to the user telling the new password
        @param: user
        @return: true || false
        """

        new_pwd = self.id_generator()
        new_pwd_hash = self.make_pw_hash(new_pwd)
        user = self.get_user(_id)

        if not pubUtilities.sendMail(user['email'], c.SUBJECT_FORGOT_PASSWORD, c.BODY_FORGOT_PASSWORD % new_pwd):
            print "error sending email user: %" % user['email']
            return False
        try:
            self.users.update({'_id': _id}, {'$set': {'password': new_pwd_hash}})
        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False

        return True


    def get_pub_name(self, name, lastname):

        return self.pub_name(name,lastname)




