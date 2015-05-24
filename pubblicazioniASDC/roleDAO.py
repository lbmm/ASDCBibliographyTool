_author_ = 'fmoscato'

import pymongo.errors


class RoleDAO:

    def __init__(self, db):
        self.db = db
        self.roles = self.db.roles

    def get_roles(self):
      
        cursor = self.roles.find().sort('_id', direction=1)
        l = []

        for role in cursor:

            l.append({'role': role['_id']})

        return l

    def remove_role(self, _id):

        try:
            self.roles.remove({'_id': _id})
        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False
    
        return True 

    def add_role(self, **kwargs):

        role = {'_id': kwargs['role']}

        try:
            self.roles.insert(role)
        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False
        except pymongo.errors.DuplicateKeyError:
            print "oops, role name is already taken"
            return False

        return True


