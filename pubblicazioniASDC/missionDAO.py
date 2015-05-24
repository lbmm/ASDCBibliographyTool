_author_ = 'fmoscato'

from datetime import datetime

import pymongo.errors

import constants as c

# The Mission  Data Access Object handles all interactions with the Mission collection.
# The Mission collection is a collections of missions that are related with missions. Users can 
# have multiple missions to work with.


class MissionDAO(object):

    def __init__(self, db):
        self.db = db
        self.missions = self.db.missions

    def get_missions(self, date_format=None):
      
        cursor = self.missions.find().sort('_id', direction=1)
        l = []

        date_format_str = "%B %Y"

        if date_format:
            date_format_str = date_format

        for mission in cursor:

            l.append({'name': mission['_id'],
                      'start_date': mission['start_date'].strftime(date_format_str),
                      'end_date': mission['end_date'].strftime(date_format_str)})

        return l



    #get valide missions for a time period
    def get_valide_missions(self, start_date=None, end_date=None):

        l = []

        try:

            if not start_date and not end_date:
                
                today = datetime.now()
                cursor = self.missions.find({'end_date': {"$gt": today}})
 
            else:
                cursor = self.missions.find({'end_date': {"$lte": start_date,
                                                          "$gte": end_date}})
            for mission in cursor:

                l.append({'name': mission['_id'],
                          'start_date': mission['start_date'].strftime("%B %Y"),
                          'end_date': mission['end_date'].strftime("%B %Y")})


        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False


        return l

    def remove_mission(self, _id):

        try:
 
            self.missions.remove({'_id': _id})
  
        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False
    
        return True 
      
    def close_validity_mission(self, _id):
 
        today = datetime.now()

        try:
            self.missions.update({'_id': _id}, {'$set': {"end_date": today}})
        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False
         
        return True

    # creates a new mission in the missions collection
    def add_mission(self, **kwargs):

        mission = {'_id': kwargs['name'],
                   'start_date': datetime.strptime(kwargs['start_date'].rstrip(), c.DATE_FORMAT)}

        if 'end_date'in kwargs and kwargs['end_date'] != '':
            mission['end_date'] = datetime.strptime(kwargs['end_date'], c.DATE_FORMAT)
        else:
            date1 = datetime.strptime(c.END_DATE, c.DATE_FORMAT) 
            mission['end_date'] = date1

        try:
            self.missions.insert(mission)
        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False
        except pymongo.errors.DuplicateKeyError:
            print "oops, mission name is already taken"
            return False

        return True


