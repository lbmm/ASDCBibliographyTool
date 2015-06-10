__author__ = 'fmoscato'

"""
App to handle the temporary publications
"""

from datetime import datetime

import pymongo
import bottle

import publicationDAO
import temporaryPublicationDAO
import sessionDAO
import missionDAO
import userDAO
import validatePublications
import pubUtilities as utilities
import authentication as auth
import constants as c
import handle_asdc_author


temporary_app = bottle.Bottle()

connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string)
database = connection.publication

sessions = sessionDAO.SessionDAO(database)
missions = missionDAO.MissionDAO(database)
users = userDAO.UserDAO(database)
publications = publicationDAO.PublicationDAO(database)
temporary_publications = temporaryPublicationDAO.TemporaryPublicationDAO(database)
valide_user = auth.authenticator_user(sessions)
valide_admin = auth.authenticator(sessions)



@bottle.get('/add_publication')
@valide_user()
def present_add_publication():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    m_list = missions.get_missions()
    asdc_authors = users.get_users()

    default_values = {'biblicode': '',
                      'DOI': '',
                      'title': '',
                      'authors': '',
                      'asdc_authors': [],
                      'pub_date': '',
                      'origin': '',
                      'magazine': '',
                      'URL': '',
                      'abstract': '',
                      'keywords': '',
                      'missions': [],
                      'is_refeered': 'Y'}

    validate = validatePublications.ValidatePublications()

    return bottle.template("add_publication", dict(username=username, missions=m_list, asdc_authors=asdc_authors,
                                                   publication=default_values, errors=validate.errors))


@bottle.post('/add_publication')
@valide_user()
def process_add_publication():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    m_list = missions.get_missions()
    asdc_authors = users.get_users()

    form_values = {
        'biblicode': bottle.request.forms.get("biblicode"),
        'DOI': bottle.request.forms.get("DOI"),
        'title': utilities.clean_string(bottle.request.forms.get("title")),
        'authors': utilities.clean_string(bottle.request.forms.get("authors")),
        'asdc_authors': bottle.request.forms.getall("asdc_authors"),
        'pub_date': bottle.request.forms.get("pub_date"),
        'origin': bottle.request.forms.get("origin"),
        'magazine': bottle.request.forms.get("magazine"),
        'URL': utilities.clean_string(bottle.request.forms.get("URL")),
        'abstract': utilities.clean_string(bottle.request.forms.get("abstract", "")),
        'keywords': utilities.clean_string(bottle.request.forms.get("keywords", "")),
        'publication': bottle.request.forms.get("publication", ""),
        'missions': bottle.request.forms.getall("missions"),
        'is_refeered': utilities.str2bool(bottle.request.forms.get("is_refeered", True)),
        'user': username
    }

    validate = validatePublications.ValidatePublications()
    try:

        validate.validate_publication_form(form_values)

    except validatePublications.ValidationException as e:
        return bottle.template("add_publication", dict(username=username, missions=m_list, asdc_authors=asdc_authors,
                                                       publication=form_values, errors=validate.errors))

    # publication to add looks fine -> adding publication

    authors = handle_asdc_author.def_asdc_auth_auto_archiving(form_values['authors'], form_values['asdc_authors'])
    form_values['authors'] = authors
    form_values['asdc_authors'] = [auth.split("_")[0] for auth in bottle.request.forms.getall("asdc_authors")]
    if not temporary_publications.add_publication(form_values, validate.errors):
        return bottle.template("add_publication", dict(username=username, missions=m_list, asdc_authors=asdc_authors,
                                                       publication=form_values, errors=validate.errors))

    if not utilities.sendMail(users.get_admin_email(), c.SUBJECT_TMP_PUB, c.BODY_TMP_PUB % username):
            print "error sending email admin "

    msg = "La pubblicazione %s e' stata temporaneamente inserita. " \
          "Quando approvata dall'amministratore sarete avvertiti con una mail." % form_values['biblicode']

    return bottle.template("welcome", dict(username=username, msg=msg))


# Displays a particular publication selected by biblicode in the tmp collections
@bottle.get("/tmp_publication/<biblicode>")
@valide_admin()
def show_publication(biblicode="notfound"):
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    pub = temporary_publications.get_tmp_publication_by_biblicode(biblicode)

    if not pub:
        bottle.redirect("/publication_not_found")

    return bottle.template("tmp_publication_detail", dict(publication=pub, username=username))


@bottle.get('/validate_users_publications')
@valide_admin()
def present_publications_to_save():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    l = temporary_publications.get_publications()

    return bottle.template("tmp_publication_list", dict(publications=l, username=username,
                                                        is_admin=True))


@bottle.post('/remove_tmp_publications')
@valide_admin()
def remove_tmp_publication():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    bibcode = bottle.request.forms.get("biblicode")

    #here a special char is used to send biblicode that contains &
    #otherwise the request will split the information

    bibcode = bibcode.replace("!", "&")

    if not temporary_publications.remove_publication(bibcode):
        print "error removing tmp publications"
        return bottle.HTTPResponse(status=202, body="error")
    else:
        return bottle.HTTPResponse(status=200, body="success")




@bottle.post('/validate_users_publications')
@valide_admin()
def process_publications_to_save():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    biblicode_to_consolidate = bottle.request.forms.getlist("biblicode")

    errors, msg = [], []
    msg_str, err_str = None, None
    msg = []
    err = {'admin': '', 'general': ''}

    for bib in biblicode_to_consolidate:

        all_info_tmp_publications = temporary_publications.get_tmp_publication_by_biblicode(bib)
        user_email = users.get_user(all_info_tmp_publications['user'])['email']

        if not temporary_publications.consolidate_publication(bib, err):
            errors.append(bib)
        else:
            msg.append(bib)
            utilities.sendMail(user_email, c.SUBJECT_ADMIN_CONFIRM_TMP_PUB,
                               c.BODY_ADMIN_CONFIRM_TMP_PUB % (bib, bib))

    if err['general']:
        errors.extend(err['general'])

    for err in err['admin']:
        utilities.sendMail(users.get_admin_email(), "ADMIN Error", err)

    if msg:
        msg_str = "Users publications validate: <br> %s" % '<br> '.join(msg)
    if errors:
        err_str = "error validating users publications:<br> %s" % '<br> '.join(errors)
    return bottle.template("admin", dict(username=username, msg=msg_str, errors=err_str))




