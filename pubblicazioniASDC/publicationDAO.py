__author__ = 'fmoscato'

"""
The Publication DAO  handles interactions with the publication collection
The DAO provides 3 levels interface (da scrivere meglio)
1 - ADMIN can add publications + validate
2- search publications
3- users level
"""

import sys
from datetime import datetime

import pymongo.errors

import constants as c
import handle_asdc_author


class PublicationDAO(object):

    def __init__(self, database):
        self.db = database
        self.publications = database.publications

    def add_publication(self, **kwargs):
        """
        insert publication.
        param: **kwargs
        return : true || false
        """

        print "inserting publication entry ", kwargs['biblicode']

        magazine = (kwargs["biblicode"].split('.')[0])[4:]

        if magazine.startswith('arXiv'):
            magazine = 'arXiv'

        #this piece is done for the not refeered publications, that some times can have 00 instead
        #of a valid month
        try:
            pub_date = datetime.strptime(kwargs["pub_date"], "%m/%Y")
        except ValueError:
            print "guffy pub_date: %s" % kwargs["pub_date"]
            pub_date = datetime.strptime("01/%s" % (kwargs["pub_date"].split("/")[1]), "%m/%Y")


        # Build a new publication 
        publication = {"_id": kwargs["biblicode"],
                       "title": unicode(kwargs["Title"], 'utf-8', 'ignore'),
                       "authors": unicode(kwargs["authors"], 'utf-8', 'ignore'),
                       "mission": kwargs["mission"],
                       "pub_date": pub_date,
                       "DOI": kwargs["DOI"],
                       "Keywords": kwargs["Keywords"],
                       "URL": c.URL_ADS + kwargs["biblicode"],
                       "Origin": kwargs["Origin"],
                       "Magazine": magazine,
                       "Abstract": unicode(kwargs["Abstract"], 'utf-8', 'ignore'),
                       # we are assuming that all the publications belongs to the users
                       #they have to explicit say that don't belong to them
                       "asdc_auth": [dict(author=usr, validate=True)for usr in kwargs["asdc_author"]],
                       "publication": unicode(kwargs["Publication"], 'utf-8', 'ignore'),
                       "is_open": kwargs.get("is_open", True),
                       "is_refeered": kwargs["is_refeered"]}

        # now insert the publication 
        try:
            self.publications.insert(publication)
            print "Inserted the publication: ", kwargs['biblicode']
        except pymongo.errors.DuplicateKeyError:
            #it's OK. same biblicode can have multiple ASDC users
            # then need only to be updated: fields that can be updated:
            #1- asdc_authors 2- missions
            #this is can be done only if the publication is open
            #otherwise skip
            try:
                pub = self.get_publication_by_biblicode(kwargs["biblicode"])
                print "biblicode %s and state %s " % (pub['biblicode'], pub['is_open'])
                if pub["is_open"]:
                    self.publications.update({"_id": kwargs["biblicode"]},
                                             {"$set":
                                             {"asdc_auth": [dict(author=usr, validate=True)for usr in kwargs["asdc_author"]],
                                              "mission": kwargs["mission"],
                                              "authors": unicode(kwargs["authors"], 'utf-8', 'ignore')}})
                else:

                    print ("skipping update for publication :%s - already validated " % kwargs["biblicode"])

            except pymongo.errors.OperationFailure:
               print "Error updating publication %s: %s" % (kwargs["biblicode"], sys.exc_info()[0])
        except pymongo.errors.OperationFailure:
            print "Error inserting publication %s: %s" % (kwargs["biblicode"], sys.exc_info()[0])

        return True

    def remove_publication(self, _id):

        try:

            print "removing publication %s" % _id

            self.publications.remove({'_id': _id})

        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False

        return True

    # return an array of publications still open sorting descending for pub_date, in short format
    def get_open_publications(self, is_refeered, start_date=None, end_date=None, ):

        pub = []

        try:

            if not start_date and not end_date:

                cursor = self.publications.find({'is_open': True, 'is_refeered': is_refeered}
                                                ).sort('pub_date', pymongo.DESCENDING)

            else:

                cursor = self.publications.find({'is_open': True, 'is_refeered': is_refeered,
                                                 'pub_date': {'$gte': start_date, '$lte': end_date}}).sort('pub_date', direction=-1)

            for publication in cursor:

                pub.append({'title': publication['title'],
                            'authors': publication['authors'],
                            'biblicode': publication['_id'],
                            'pub_date': publication['pub_date'].strftime("%B %Y"),
                            'is_refeered':publication['is_refeered']})


        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False

        return pub

    def get_publications_to_close(self, is_refeered, start_date, end_date, ):

        pub = []

        try:

            cursor = self.publications.find({'is_open': True, 'is_refeered': is_refeered,
                                             'pub_date': {'$gte': start_date, '$lte': end_date}}
                                            ).sort('pub_date', pymongo.DESCENDING)

            for publication in cursor:

                pub.append({'title': publication['title'],
                            'asdc_auth': publication['asdc_auth'],
                            'biblicode': publication['_id'],
                            'pub_date': publication['pub_date'].strftime("%B %Y"),
                            'mission': publication['mission'],
                            'is_refeered': publication['is_refeered'],
                            'DOI': publication['DOI']})


        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False

        return pub

     # returns an array of valide publications sorted for ascending pub_date, in short format
    def get_closed_publications(self, is_refeered, start_date=None, end_date=None):

        pub = []

        if not start_date and not end_date:

            cursor = self.publications.find({'is_open': False, 'is_refeered': is_refeered}).sort('pub_date')

        else:

            cursor = self.publications.find({"is_open": False, 'is_refeered': is_refeered,
                                            "pub_date": {"$gte": start_date, "$lte": end_date}
                                             }).sort('pub_date', pymongo.ASCENDING)

        for publication in cursor:

            pub.append({'title': publication['title'],
                        'URL': publication['URL'],
                        'authors': publication['authors'],
                        'asdc_auth': publication['asdc_auth'],
                        'mission': publication['mission'],
                        'biblicode': publication['_id'],
                        'pub_date': publication['pub_date'].strftime("%B %Y"),
                        'is_refeered': publication['is_refeered']})

        return pub

    def close_publication(self, biblicode):

        try:
            self.publications.update({"_id": biblicode},
                                     {"$set": {'is_open': False}})

        except pymongo.errors.OperationFailure:
            print "Mongo error, closing publication %s" % biblicode
            return False
        return True

    # this is needed at user level
    def get_publication_to_validate(self, author, is_refeered):

        cursor = self.publications.find({'asdc_auth.author': author, 'is_refeered': is_refeered,
                                         "is_open": True}).sort('pub_date', direction=1)
        pub = []

        for publication in cursor:

            pub.append({'title': publication['title'],
                        'asdc_auth': publication['asdc_auth'],
                        'authors': publication['authors'],
                        'biblicode': publication['_id'],
                        'pub_date': publication['pub_date'].strftime("%B %Y"),
                        'mission': publication['mission'],
                        'is_refeered':publication['is_refeered'],
                        'DOI': publication['DOI']})

        return pub

    # this is needed at user level
    #user has to specify in the publications are not valid
    def invalidate_publication(self, biblicode, user):

        try:
            #to find the author list
            record = self.publications.find_one({'_id': biblicode}, {'authors': 1, '_id': 0})

            #update on the publication entry for valide and update the title for the user (remove his/her part)
            self.publications.update({'_id': biblicode, 'asdc_auth.author': user},
                                     {'$set': {'asdc_auth.$.validate': False,
                                               'authors': handle_asdc_author.update_asdc_authors(record['authors'], user)}})

        except pymongo.errors.OperationFailure as e:
            print "Mongo error, closing publication %s" % biblicode
            return False
        return True

    def update_authors_mission(self, biblicode, auth_list):

        try:
            #to find the author list
            record = self.publications.find_one({'_id': biblicode}, {'authors': 1, '_id': 0})
            asdc_names = [(asdc.split("_"))[0] for asdc in auth_list]
            #update the entry and update the asdc authors and total authors
            self.publications.update({'_id': biblicode},
                                     {'$set':
                                            {'asdc_auth': [dict(author=usr, validate=True)for usr in asdc_names],
                                             'authors': handle_asdc_author.overwrite_asdc_authors(record['authors'],
                                                                                                 auth_list)}})

        except pymongo.errors.OperationFailure as e:
            print e
            print "Mongo error, updating authors per biblicode %s" % biblicode
            return False
        return True


    # this is needed at user level
    def update_missions(self, biblicode, missions_list):

        try:
            self.publications.update({'_id': biblicode},
                                     {'$set': {'mission': missions_list}})

        except pymongo.errors.OperationFailure:
            print "Mongo error, updating missions in publication %s" % biblicode
            return False
        return True


    # here methods for publications search (the search is done only on the close publications):
    # the search can be done
    # 1- biblicode (return single publication with detail)
    # 2- DOI       (return single publication with detail)
    # 3- Author    (return a list of publications)
    # 4- Mission   (return a list of publications)
    # 5- Magazine  (return a list of publications)


    # find a publiction corresponding to a particular biblicode
    def get_publication_by_biblicode(self, biblicode):

        publication = self.publications.find_one({'_id':  biblicode})

        pub = None

        if publication:

            pub = dict(title=publication['title'], authors=publication['authors'],
                       biblicode=publication['_id'], pub_date=publication['pub_date'].strftime("%B %Y"),
                       is_refeered=publication['is_refeered'], URL=publication['URL'],
                       is_open=publication['is_open'],
                       DOI=publication['DOI'], Origin=publication['Origin'],
                       Abstract=publication['Abstract'], Keywords=publication["Keywords"])


        return pub

    #return an array of publications that match with the biblicode pattern
    def get_publications_by_biblicode(self, biblicode, is_refeered):

        publications = self.publications.find({'_id': {'$regex': biblicode},
                                               'is_refeered': is_refeered,
                                               'is_open': False})

        pub = []

        for p in publications:

            pub.append({'title': p['title'],
                        'authors': p['authors'],
                        'URL': p['URL'],
                        'biblicode': p['_id'],
                        'pub_date': p['pub_date'].strftime("%B %Y"),
                        'is_refeered': p['is_refeered']})

        return pub


     #return an array of publications that match with the DOI pattern
    def get_publications_by_DOI(self, DOI, is_refeered):

        publications = self.publications.find({'DOI': {'$regex': DOI},
                                               'is_refeered': is_refeered,
                                               'is_open': False})

        pub = []

        for p in publications:

            pub.append({'title': p['title'],
                        'authors': p['authors'],
                        'URL': p['URL'],
                        'biblicode': p['_id'],
                        'pub_date': p['pub_date'].strftime("%B %Y"),
                        'is_refeered': p['is_refeered']})

        return pub

    #returns an array of valide publications per author
    def get_closed_publications_author(self, author, is_refeered, start_date=None, end_date=None, mission=None):

        pipe = None

        if not start_date and not end_date and not mission:

            pipe = [{'$unwind': '$asdc_auth'},
                    {'$match': {'is_refeered': is_refeered, 'is_open': False,
                                'asdc_auth.validate': True, 'asdc_auth.author': author}},
                    {'$sort': {'pub_date': -1}}]

        elif not start_date and not end_date and mission:

            pipe = [{'$unwind': '$asdc_auth'},
                    {'$match': {'is_refeered': is_refeered, 'is_open': False, 'mission': mission,
                                'asdc_auth.validate': True, 'asdc_auth.author': author}},
                    {'$sort': {'pub_date': -1}}]

        elif start_date and end_date and not mission:

            pipe = [{'$unwind': '$asdc_auth'},
                    {'$match': {'is_refeered': is_refeered, 'is_open': False,
                                'asdc_auth.validate': True, 'asdc_auth.author': author,
                                'pub_date': {'$gte': start_date, '$lte': end_date}}},
                    {'$sort': {'pub_date': -1}}]

        elif start_date and end_date and mission:

            pipe = [{'$unwind': '$asdc_auth'},
                    {'$match': {'is_refeered': is_refeered, 'is_open': False, 'mission': mission,
                                'asdc_auth.validate': True, 'asdc_auth.author': author,
                                'pub_date': {'$gte': start_date, '$lte': end_date}}},
                    {'$sort': {'pub_date': -1}}]

        res = self.publications.aggregate(pipeline=pipe)
        pub = []

        for publication in res['result']:

            pub.append({'title': publication['title'],
                        'authors': publication['authors'],
                        'URL': publication['URL'],
                        'biblicode': publication['_id'],
                        'pub_date': publication['pub_date'].strftime("%B %Y"),
                        'is_refeered': publication['is_refeered']})

        return pub

    def get_closed_publications_mission(self, mission, is_refeered, start_date=None, end_date=None):

        cursor = []

        if not start_date and not end_date:

            cursor = self.publications.find({'mission': {'$regex': mission, '$options': 'i'},
                                             'is_refeered': is_refeered,
                                             "is_open": False}).sort('pub_date', pymongo.DESCENDING)
        elif start_date and end_date:

            cursor = self.publications.find({'mission': {'$regex': mission, '$options': 'i'},
                                             'is_refeered': is_refeered,
                                             'pub_date': {'$gte': start_date, '$lte': end_date},
                                             "is_open": False}).sort('pub_date', pymongo.DESCENDING)
        pub = []

        for publication in cursor:

            pub.append({'title': publication['title'],
                        'URL': publication['URL'],
                        'authors': publication['authors'],
                        'biblicode': publication['_id'],
                        'pub_date': publication['pub_date'].strftime("%B %Y"),
                        'is_refeered': publication['is_refeered']})

        return pub


    def get_closed_publications_journal(self, journal, is_refeered, start_date=None, end_date=None):

        cursor = []

        if not start_date and not end_date:

            cursor = self.publications.find({'Magazine': {'$regex': journal, '$options': 'i'},
                                             'is_refeered': is_refeered,
                                             "is_open": False}).sort('pub_date', pymongo.DESCENDING)
        elif start_date and end_date:

            cursor = self.publications.find({'Magazine': {'$regex': journal, '$options': 'i'},
                                             'is_refeered': is_refeered,
                                             'pub_date': {'$gte': start_date, '$lte': end_date},
                                             "is_open": False}).sort('pub_date', pymongo.DESCENDING)
        pub = []

        for publication in cursor:

            pub.append({'title': publication['title'],
                        'URL': publication['URL'],
                        'authors': publication['authors'],
                        'biblicode': publication['_id'],
                        'pub_date': publication['pub_date'].strftime("%B %Y"),
                        'is_refeered': publication['is_refeered']})

        return pub















