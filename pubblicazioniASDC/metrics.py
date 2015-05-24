__author__ = 'fmoscato'

#Router for the metrics pages

from datetime import datetime

import pymongo
import bottle

import aggregationDAO
import sessionDAO
import missionDAO
import userDAO
import constants as c
import validatePublications


#create the app for the metrics interface

metric_app = bottle.Bottle()


@bottle.get('/metrics_journal')
def process_journal():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)
    year = bottle.request.query.get("year", None)

    if year:
        validate = validatePublications.ValidatePublications()
        try:
            validate.validate_year(year)
        except validatePublications.ValidationException as e:
            print "guffy year for metrics journal: resetting to null"
            year = None

    refeered = metrics.aggregateJournal(True, year)
    not_refeered = metrics.aggregateJournal(False, year)

    return bottle.template('journal_metrics', dict(refeered_count=refeered,
                                                   not_refeered_count=not_refeered,
                                                   username=username, years=c.years,
                                                   year=year, is_admin=is_admin))


@bottle.get('/metrics_authors')
def process_journal():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)
    year = bottle.request.query.get("year", None)
    author = bottle.request.query.get("author", None)

    if year:
        validate = validatePublications.ValidatePublications()
        try:
            validate.validate_year(year)
        except validatePublications.ValidationException as e:
            print "guffy year for metrics authors: resetting to null"
            year = None

    refeered = metrics.aggregateAuthor(True, year)
    not_refeered = metrics.aggregateAuthor(False, year)

    # i need information regarding authors: this information is
    #already stored in the aggregate author method

    authors = sorted([f['author'] for f in refeered])
    complete_authors = users.get_users("%B %d, %Y")
    histogram_year = metrics.aggregateYearHistogram(author)
    count_authors = metrics.aggregateCountAuthors()

    return bottle.template('author_metrics', dict(refeered_count=refeered,
                                                  not_refeered_count=not_refeered,
                                                  histogram_year=histogram_year,
                                                  username=username, years=c.years,
                                                  year=year, complete_authors=complete_authors,
                                                  today=(datetime.today().date()).strftime("%B %d, %Y"),
                                                  authors=authors, author=author, is_admin=is_admin,
                                                  header_authors=count_authors))


@bottle.get('/metrics_missions')
def process_journal():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)
    year = bottle.request.query.get("year", None)
    mission = bottle.request.query.get("mission", None)
    author_per_mission = {'refeered': [], 'not_refeered': []}

    if year:
        validate = validatePublications.ValidatePublications()
        try:
            validate.validate_year(year)
        except validatePublications.ValidationException as e:
            print "guffy year for metrics missions: resetting to null"
            year = None

    refeered = metrics.aggregateMission(True, year)
    not_refeered = metrics.aggregateMission(False, year)

    missions_list = missions.get_missions("%B %d, %Y")
    tot_missions = {}

    if mission:
        author_per_mission['refeered'] = metrics.aggregateMissionsAuthor(mission, True)
        author_per_mission['not_refeered'] = metrics.aggregateMissionsAuthor(mission, False)
        tot_missions = {mission: {'refereed': metrics.aggregateMissionCount(mission, True),
                                  'not_refereed': metrics.aggregateMissionCount(mission, False)}}

        tot_missions

    return bottle.template('mission_metrics', dict(refeered_count=refeered,
                                                   not_refeered_count=not_refeered,
                                                   username=username, years=c.years,
                                                   year=year, missions_list=missions_list,
                                                   today=(datetime.today().date()).strftime("%B %d, %Y"),
                                                   mission=mission, author_per_mission=author_per_mission,
                                                   is_admin=is_admin, tot_missions=tot_missions))

@bottle.get('/metrics_ASDC')
def process_journal():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)
    histogram_year = metrics.aggregatePublicationASDC()

    return bottle.template('asdc_metrics', dict(username=username, is_admin=is_admin,
                                                histogram_year=histogram_year))



@bottle.get('/ASDC_authors_timeline')
def process_authors_timeline():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)


    complete_authors = users.get_users("%B %d, %Y")
    count_authors = metrics.aggregateCountAuthors()

    return bottle.template('ASDC_authors_timeline', dict(username=username, complete_authors=complete_authors,
                                                         today=(datetime.today().date()).strftime("%B %d, %Y"),
                                                         is_admin=is_admin, header_authors=count_authors))


@bottle.get('/ASDC_missions_timeline')
def process_missions_timeline():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)

    missions_list = missions.get_missions("%B %d, %Y")

    return bottle.template('missions_timeline', dict(username=username,
                                                     missions_list=missions_list,
                                                     today=(datetime.today().date()).strftime("%B %d, %Y"),
                                                     is_admin=is_admin))






@bottle.get('/overview')
def present_ASDC_overview():

    histogram_year = metrics.aggregateYearHistogram()

    return bottle.template('overview', dict(histogram_year=histogram_year))





connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string)
database = connection.publication


sessions = sessionDAO.SessionDAO(database)
metrics = aggregationDAO.AggregationDAO(database)
missions = missionDAO.MissionDAO(database)
users = userDAO.UserDAO(database)


