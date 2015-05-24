__author__ = 'fmoscato'

from datetime import datetime
from collections import OrderedDict

import pymongo.errors

import constants as c



# The Aggregation DAO  handles interactions with the publication collection,
# and aggregate the results.

class AggregationDAO:

    # constructor for the class
    def __init__(self, database):
        self.db = database
        self.publications = database.publications
        self.missions = database.missions
        self.users = database.users

    def aggregateJournal(self, is_refeered=True, year=None):

        journal = []
        pipe = None

        try:

            if year:


                date_start = datetime.strptime('01/01/%s' % year, c.DATE_FORMAT)
                date_end = datetime.strptime('12/31/%s' % year, c.DATE_FORMAT)

                pipe = [{'$match': {'is_refeered': is_refeered, 'is_open': False,
                                    'pub_date': {'$gte': date_start, '$lte': date_end}}},
                        {'$project': {'Magazine': 1}},
                        {'$group': {'_id': '$Magazine', 'count': {'$sum': 1}}},
                        {'$sort': {'count': -1}}]


            else:

                pipe = [{'$match': {'is_refeered': is_refeered, 'is_open': False}},
                        {'$project': {'Magazine': 1}},
                        {'$group': {'_id': '$Magazine', 'count': {'$sum': 1}}},
                        {'$sort': {'count': -1}}]

            res = self.publications.aggregate(pipeline=pipe)

            for j in res['result']:

                journal.append({"journal": j["_id"], "count": j["count"]})

        except pymongo.errors.OperationFailure:
            print "Mongo error, aggregating publications"

        return journal

    def aggregateAuthor(self, is_refeered=True, year=None):

        authors = []
        pipe = None

        try:

            if year:

                date_start = datetime.strptime('01/01/%s' % year, c.DATE_FORMAT)
                date_end = datetime.strptime('12/31/%s' % year, c.DATE_FORMAT)

                pipe = [{'$unwind': '$asdc_auth'},
                        {'$match': {'is_refeered': is_refeered, 'is_open': False,
                                    'asdc_auth.validate': True,
                                    'pub_date': {'$gte': date_start, '$lte': date_end}}},
                        {'$project': {'asdc_auth.author': 1}},
                        {'$group': {'_id': '$asdc_auth.author', 'count': {'$sum': 1}}},
                        {'$sort': {'count': -1}}]

            else:

                pipe = [{'$unwind': '$asdc_auth'},
                        {'$match': {'is_refeered': is_refeered, 'is_open': False,
                                    'asdc_auth.validate': True}},
                        {'$project': {'asdc_auth.author': 1}},
                        {'$group': {'_id': '$asdc_auth.author', 'count': {'$sum': 1}}},
                        {'$sort': {'count': -1}}]

            res = self.publications.aggregate(pipeline=pipe)

            for j in res['result']:

                authors.append({"author": j["_id"], "count": j["count"]})

        except pymongo.errors.OperationFailure:
            print "Mongo error, aggregating publications"

        return authors

    def aggregateMission(self, is_refeered=True, year=None):

        missions = []
        pipe = None

        try:

            if year:

                date_start = datetime.strptime('01/01/%s' % year, c.DATE_FORMAT)
                date_end = datetime.strptime('12/31/%s' % year, c.DATE_FORMAT)

                pipe = [{'$unwind': '$mission'},
                        {'$match': {'is_refeered': is_refeered, 'is_open': False,
                                    'asdc_auth.validate': True,
                                    'pub_date': {'$gte': date_start, '$lte': date_end}}},
                        {'$project': {'mission': 1}},
                        {'$group': {'_id': '$mission', 'count': {'$sum': 1}}},
                        {'$sort': {'count': -1}}]

            else:

                pipe = [{'$unwind': '$mission'},
                        {'$match': {'is_refeered': is_refeered, 'is_open': False,
                                    'asdc_auth.validate': True}},
                        {'$project': {'mission': 1}},
                        {'$group': {'_id': '$mission', 'count': {'$sum': 1}}},
                        {'$sort': {'count': -1}}]

            res = self.publications.aggregate(pipeline=pipe)

            for j in res['result']:

                missions.append({"mission": j["_id"], "count": j["count"]})

        except pymongo.errors.OperationFailure:
            print "Mongo error, aggregating publications"

        return missions

    def aggregateMissionCount(self, mission, is_refeered=True):

        mission_count = 0
        pipe = None

        try:

            pipe = [{'$unwind': '$mission'},
                    {'$match': {'is_refeered': is_refeered, 'is_open': False,
                                'asdc_auth.validate': True, 'mission': mission}},
                    {'$project': {'mission': 1}},
                    {'$group': {'_id': '$mission', 'count': {'$sum': 1}}},
                    {'$sort': {'count': -1}}]

            res = self.publications.aggregate(pipeline=pipe)

            for j in res['result']:

                mission_count = j["count"]


        except pymongo.errors.OperationFailure:
            print "Mongo error, aggregating publications"

        return mission_count



    def aggregateMissionsAuthor(self, mission, is_refeered=True):

        author_per_mission = []

        pipe = [{'$unwind': '$asdc_auth'},
                {'$match': {'is_refeered': is_refeered, 'is_open': False, 'asdc_auth.validate': True,
                            'mission': mission}},
                {'$project': {'asdc_auth.author': 1}},
                {'$group': {'_id': '$asdc_auth.author', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}}]

        try:

            res = self.publications.aggregate(pipeline=pipe)

            for j in res['result']:

                author_per_mission.append({"author": j["_id"], "count": j["count"]})

        except pymongo.errors.OperationFailure:
            print "Mongo error, aggregating publications"

        return author_per_mission


    def aggregateYearHistogram(self, author=None):

        pipe_refeered, pipe_not_refeered  = None, None
        publications_per_year = []

        if not author:

            pipe_refeered = [{'$match': {'is_refeered': True, 'is_open': False}},
                             {'$project': {'year': {'$year': '$pub_date'}}},
                             {'$group': {'_id': '$year', 'count': {'$sum': 1}}},
                             {'$sort': {'_id': 1}}]

            pipe_not_refeered = [{'$match': {'is_refeered': False, 'is_open': False}},
                                 {'$project': {'year': {'$year': '$pub_date'}}},
                                 {'$group': {'_id': '$year', 'count': {'$sum': 1}}},
                                 {'$sort': {'_id': 1}}]

        else:

            pipe_refeered = [{'$unwind': '$asdc_auth'},
                             {'$match': {'is_refeered': True, 'is_open': False,
                                         'asdc_auth.validate': True, 'asdc_auth.author': author}},
                             {'$project': {'year': {'$year': '$pub_date'}}},
                             {'$group': {'_id': '$year', 'count': {'$sum': 1}}},
                             {'$sort': {'_id': 1}}]

            pipe_not_refeered = [{'$unwind': '$asdc_auth'},
                                 {'$match': {'is_refeered': False, 'is_open': False,
                                             'asdc_auth.validate': True, 'asdc_auth.author': author}},
                                 {'$project': {'year': {'$year': '$pub_date'}}},
                                 {'$group': {'_id': '$year', 'count': {'$sum': 1}}},
                                 {'$sort': {'_id': 1}}]

        res_refeered = self.publications.aggregate(pipeline=pipe_refeered)
        res_not_refeered = self.publications.aggregate(pipeline=pipe_not_refeered)

        years = [year['_id'] for year in res_refeered['result']]
        years_not_ref = [year['_id'] for year in res_not_refeered['result']]
        years_common = list(set(years).union(set(years_not_ref)))


        for y in years_common:

            refeered_value = [res['count'] for res in res_refeered['result'] if str(res['_id']) == str(y)]
            if not refeered_value: refeered_value = [0]

            not_refeered_value = [res['count'] for res in res_not_refeered['result'] if str(res['_id']) == str(y)]
            if not not_refeered_value: not_refeered_value = [0]

            publications_per_year.append({'year': y, 'refeered': sum(refeered_value),
                                          'not_refeered': sum(not_refeered_value)})

        return publications_per_year


    def aggregatePublicationASDC(self):

        pipe = [{'$match': {"is_open": False, "asdc_auth.validate": True}},
                {'$project': {'is_refeered': 1, 'year': {'$year': "$pub_date"}, 'month': {'$month': "$pub_date"}}},
                {'$group': {'_id': {'year': "$year", 'month': "$month", 'is_refeered': "$is_refeered"},
                            'count': {'$sum': 1}}},
                {'$sort': {'_id.year': 1, '_id.month': 1}}]


        res = self.publications.aggregate(pipeline=pipe)

        tmp_list = [{'year': j['_id']['year'], 'month': j['_id']['month'], 'refeered': j['count']}
                     if j['_id']['is_refeered']
                     else {'year': j['_id']['year'], 'month': j['_id']['month'], 'not_refeered': j['count']}
                     for j in res["result"]]


        publications_time_line = {}

        for f in tmp_list:
            key = '%s-%s' % (f['year'], f['month'])
            if key not in publications_time_line:
               publications_time_line[key] = f
            else:
                for k in f.keys():
                    if k not in publications_time_line.keys():
                        publications_time_line[key][k] = f[k]

        return list(publications_time_line.values())


    def aggregateCountAuthors(self):

        authors_count = OrderedDict()

        for y in reversed(c.years):

            if y == 2000 : continue

            start_date = datetime.strptime("01/01/%s" % y, c.DATE_FORMAT)
            end_date = datetime.strptime("12/31/%s" % y, c.DATE_FORMAT)

            pipeline = [{'$match': {'start_date': {'$lte': start_date}, 'end_date': {'$gte': end_date}}},
                        {'$project': {'_id': 1}}, {'$group': {'_id': '_id', 'count': {'$sum': 1}}}]

            res = self.users.aggregate(pipeline=pipeline)

            results = res['result']

            if results:
               authors_count[y] = results[0]['count']
            else:
                authors_count[y] = 0

        return authors_count



















