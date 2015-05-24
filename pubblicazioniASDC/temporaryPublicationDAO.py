__author__ = 'fmoscato'

from datetime import datetime

import pymongo
from pymongo import errors as pymongoErr
from publicationDAO import PublicationDAO
import constants as c

"""
This class will provide the access to the
the temporary publications collection
"""


class TemporaryPublicationDAO(PublicationDAO):

    # constructor for the class
    def __init__(self, database):

        PublicationDAO.__init__(self, database)
        self.temporary_publication = database.tmp_publications




    def add_publication(self, kwargs, error):
        """
        1- check if a same biblicode exist
        2- add publication in the temporaty db
        """

        if self.get_publication_by_biblicode(kwargs["biblicode"]):
            error["biblicode"] = "biblicode already exist"
            return False

        publication = {"_id": kwargs["biblicode"],
                       "title": unicode(kwargs["title"], 'utf-8', 'ignore'),
                       "authors": unicode(kwargs["authors"], 'utf-8', 'ignore'),
                       "mission": kwargs["missions"],
                       "pub_date":  datetime.strptime(kwargs["pub_date"], c.DATE_FORMAT),
                       "DOI": kwargs["DOI"],
                       "Keywords": kwargs["keywords"],
                       "URL": kwargs["URL"],
                       "Origin": kwargs["origin"],
                       "Magazine": kwargs["magazine"],
                       "Abstract": unicode(kwargs["abstract"], 'utf-8', 'ignore'),
                       "asdc_auth": [dict(author=usr, validate=True)for usr in kwargs["asdc_authors"]],
                       "publication": unicode(kwargs["publication"], 'utf-8', 'ignore'),
                       "is_open": True, #insert time: all publications need to be validated
                       "is_refeered": kwargs["is_refeered"],
                       "user": kwargs["user"],
                       "daystamp": (datetime.today().date()).strftime(c.DATE_FORMAT)}

        try:
            self.temporary_publication.insert(publication)
            print "Inserted the publication: ", kwargs['biblicode']
        except pymongoErr.OperationFailure as e:
            print "Error inserting publication %s: %s" % (kwargs["biblicode"], e.message)
            error['general'] = "Error inserting publication %s: %s" % (kwargs["biblicode"], e.message)
            return False

        return True

    def remove_publication(self, biblicode):
        try:
            self.temporary_publication.remove({'_id': biblicode})
        except pymongoErr.OperationFailure as e:
            print "error removing tmp publication : %s " % biblicode
            return False
        return True

    def flag_tmp_publication_corrupted(self, biblicode):

        err = []
        try:
            self.temporary_publication.update({'_id': biblicode}, {'$set': {'corrupted': True}})
            err.append("corrupted entry in the tmp publications: %s" % biblicode)
        except pymongoErr.OperationFailure as e:
            err.append("Error in flagging corrupted biblicode %s in the temporary database" % biblicode)
        finally:
            return err

    def get_tmp_publication_by_biblicode(self, biblicode, date_format="%B %Y"):

        publication = self.temporary_publication.find_one({'_id':  biblicode})


        pub = None

        if publication:

            pub = dict(biblicode=publication['_id'], title=publication['title'],
                       authors=publication['authors'], mission=publication['mission'],
                       pub_date=publication['pub_date'].strftime(date_format),
                       DOI=publication['DOI'], Keywords=publication["Keywords"],
                       URL=publication['URL'], Origin=publication['Origin'],
                       Magazine=publication['Magazine'], Abstract=publication['Abstract'],
                       asdc_auth=publication['asdc_auth'], publication=publication['publication'],
                       is_open=publication['is_open'], is_refeered=publication['is_refeered'],
                       user=publication['user'])

        return pub

    def get_publications(self):

        publications = self.temporary_publication.find().sort('daystamp', pymongo.ASCENDING)

        publication_list = []

        for publication in publications:

            publication_list.append(dict(biblicode=publication['_id'], title=publication['title'],
                                         authors=publication['authors'], mission=publication['mission'],
                                         pub_date=publication['pub_date'].strftime("%B %Y"),
                                         DOI=publication['DOI'], Keywords=publication["Keywords"],
                                         URL=publication['URL'], Origin=publication['Origin'],
                                         Magazine=publication['Magazine'], Abstract=publication['Abstract'],
                                         asdc_auth=publication['asdc_auth'], publication=publication['publication'],
                                         is_open=publication['is_open'], is_refeered=publication['is_refeered'],
                                         user=publication['user'], daystamp=publication['daystamp']))

        return publication_list

    def consolidate_publication(self, biblicode, error):

        publication = self.get_tmp_publication_by_biblicode(biblicode, "%m/%Y")
        #update is_open, since admin has approved the publication
        publication['is_open'] = False

        try:

            super(TemporaryPublicationDAO, self).add_publication(biblicode=publication['biblicode'],
                                                                 Title=publication['title'].encode("utf-8"),
                                                                 authors=publication['authors'].encode("utf-8"),
                                                                 mission=publication['mission'],
                                                                 pub_date=publication['pub_date'],
                                                                 DOI=publication['DOI'],
                                                                 Keywords=publication["Keywords"],
                                                                 URL=publication['URL'], Origin=publication['Origin'],
                                                                 Magazine=publication['Magazine'],
                                                                 Abstract=publication['Abstract'].encode("utf-8"),
                                                                 asdc_author=[auth['author'] for auth in publication['asdc_auth']],
                                                                 Publication=publication['publication'].encode("utf-8"),
                                                                 is_open=publication['is_open'],
                                                                 is_refeered=publication['is_refeered'],
                                                                 user=publication['user'])
        except pymongoErr.OperationFailure as e:
            error['general'] = "Mongo error in adding publication %s" % biblicode
            return False

        if not self.remove_publication(biblicode):
            msg = self.flag_tmp_publication_corrupted(biblicode)
            if msg:
                error['admin'] = msg
        return True







