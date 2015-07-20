__author__ = 'fmoscato'

import cgi
from datetime import datetime
import time
import os.path
import argparse

import pymongo
import bottle


import publicationDAO
import sessionDAO
import userDAO
from admin import admin_app
from metrics import metric_app
from temporaryPublications import temporary_app
import constants as c
import pubUtilities as utilities
import PDF
import validatePublications
import authentication as auth


#app = bottle.default_app()
app = bottle.app()

app.mount('/admin/', admin_app)
app.mount('/metrics', metric_app)
app.mount('/tmp_publications', temporary_app)

connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string)
database = connection.publication

publication = publicationDAO.PublicationDAO(database)
users = userDAO.UserDAO(database)
sessions = sessionDAO.SessionDAO(database)

valide_user = auth.authenticator_user(sessions)
DOC_ROOT, TMP_DIR = '', ''


#this route the static files
@bottle.route('/static/:filename#.*#')
def server_static(filename):

    path_static = '%s/static' % DOC_ROOT 
    try:
        if not os.path.exists(path_static+"/"+filename):
            return bottle.template("not_found")
    except Exception as e:
        return bottle.redirect("/internal_error")

    return bottle.static_file(filename, root=path_static)


@bottle.route('/pdf/:filename#.*#')
def send_static(filename):
    return bottle.static_file(filename, root=TMP_DIR)

#this route the js files
@bottle.route('/js/:filename#.*#')
def server_js(filename):
    
    path_js = '%s/js' % DOC_ROOT
    try:
        if not os.path.exists(path_js+"/"+filename):
            return bottle.template("not_found")
    except IOError as e:
        return bottle.redirect("/internal_error")

    return bottle.static_file(filename, root=path_js)


@bottle.error(404)
def error404(error):
    return bottle.template("not_found")

@bottle.error(500)
def error500(error):
    return bottle.template("error_template")

@bottle.get('/internal_error')
@bottle.view('error_template')
def present_internal_error():
    return {'error': "System has encountered a DB error"}


# This route is the main page
@bottle.route('/')
def publication_index():

    #moved overview into metrics
    return bottle.redirect('overview')

# displays the initial blog login form
@bottle.get('/login')
def present_login():
    return bottle.template("login",
                           dict(username="", password="",
                                login_error=""))


# handles a login request
@bottle.post('/login')
def process_login():
    username = bottle.request.forms.get("username")
    password = bottle.request.forms.get("password")

    user_record = users.validate_login(username, password)
    if user_record:
        # username is stored in the user collection in the _id key
        session_id = sessions.start_session(user_record['_id'], user_record['admin'])

        if not session_id:
            bottle.redirect("/internal_error")

        cookie = session_id
        bottle.response.set_cookie("session", cookie)

        if user_record['admin']:
            bottle.redirect("/admin")

        bottle.redirect("/welcome")

    else:
        return bottle.template("login",
                               dict(username=cgi.escape(username), password="",
                                    login_error="Invalid Login"))


@bottle.post('/forgot_password')
def forgot_password():
    return bottle.template('forgot_password')


@bottle.post('/recover_password')
def process_forgot_password():

    username = bottle.request.forms.get("username", "")
    user = users.get_user(username)

    if not user:
        return bottle.template("forgot_password", error="user not in DB. Please contact admin")

    if not users.create_tmp_password(user['username']):
        return bottle.template("forgot_password", error="error processing your request. Please contact admin")

    return bottle.template("message_template", msg="Password sent to your email address")

@bottle.get('/user_info')
def present_user_info():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    user_info = users.get_user(username)

    return bottle.template("user_info", user=user_info, username=username)


@bottle.get('/public_publications')
def public_publications():

    is_refeered = utilities.str2bool(bottle.request.query.get("is_refeered", True))
    year = bottle.request.query.get("year", 2014)
    validate = validatePublications.ValidatePublications()

    try:
        validate.validate_dates("01/01/%s" % year, "12/31/%s" % year)
    except validatePublications.ValidationException as e:
            return bottle.template("public", {'errors': validate.errors})

    start_date = datetime.strptime("01/01/%s" % year, c.DATE_FORMAT)
    end_date = datetime.strptime("12/31/%s" % year, c.DATE_FORMAT)

    l = publication.get_closed_publications(is_refeered, start_date, end_date)

    return bottle.template("public_publications_list", dict(publications=l,
                                                            is_refeered=is_refeered))


@bottle.get('/pub_to_validate/<author>')
@valide_user()
def publication_open_by_author(author="notfound"):
    cookie = bottle.request.get_cookie("session")
    author = cgi.escape(author)
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)
    is_refeered = utilities.str2bool(bottle.request.query.get("is_refeered", True))

    l = publication.get_publication_to_validate(author, is_refeered)

    return bottle.template('publications_list', dict(publications=l,
                                                     username=username,
                                                     is_admin=is_admin,
                                                     is_refeered=is_refeered))


@bottle.get('/pub_closed/<author>')
def publication_closed_by_author(author="notfound"):
    cookie = bottle.request.get_cookie("session")
    author = cgi.escape(author)
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)
    is_refeered = utilities.str2bool(bottle.request.query.get("is_refeered", True))

    l = publication.get_closed_publications_author(author, is_refeered)

    if not username:

        return bottle.template("public_publications_list", dict(publications=l,is_refeered=is_refeered))
    else:

        return bottle.template('publications_list', dict(publications=l,
                                                         username=username,
                                                         is_admin=is_admin,
                                                         is_refeered=is_refeered))


# Displays a particular publication selected by biblicode
@bottle.get("/publication/<biblicode>")
def show_publication(biblicode="notfound"):
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)

    pub = publication.get_publication_by_biblicode(biblicode)

    if not pub:
        bottle.redirect("/publication_not_found")

    return bottle.template("publication_detail", dict(publication=pub,
                                                      username=username,
                                                      is_admin=is_admin,
                                                      errors=""))

@bottle.get("/publication_not_found")
def publication_not_found():
    return "Sorry, publication not found"


@bottle.post("/export_as_pdf")
def process_PDF():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    if not username: username = 'guest'

    filename = c.pdf_file_name + '_' + username + '_' + str(time.time())

    biblicode_to_export = bottle.request.forms.getall("biblicode")

    list_of_publication = [publication.get_publication_by_biblicode(biblicode)
                            for biblicode in biblicode_to_export]


    PDF.generatePDF(list_of_publication, filename, DOC_ROOT, TMP_DIR)

    return bottle.redirect("/pdf/%s.pdf" % filename)

# the search pages
@bottle.get("/search_by_biblicode")
def present_search():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)

    return bottle.template("search_by_biblicode", dict(username=username, is_admin=is_admin))


@bottle.post("/search_by_biblicode")
def process_search():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)

    biblicode = bottle.request.forms.get("biblicode")
    is_refeered = utilities.str2bool(bottle.request.forms.get("is_refeered", True))

    if not username:

        return bottle.template("public_publications_list", dict(publications=publication.get_publications_by_biblicode(biblicode.strip(), is_refeered),
                                                                is_refeered=is_refeered))
    else:

        return bottle.template("publications_list",
                               dict(publications=publication.get_publications_by_biblicode(biblicode.strip(), is_refeered),
                                    username=username, is_admin=is_admin))

# the search pages
@bottle.get("/search_by_DOI")
def present_search():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)

    return bottle.template("search_by_DOI", dict(username=username, is_admin=is_admin))


@bottle.post("/search_by_DOI")
def process_search():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)

    DOI = bottle.request.forms.get("DOI")
    is_refeered = utilities.str2bool(bottle.request.forms.get("is_refeered", True))

    if not username:

        return bottle.template("public_publications_list", dict(publications=publication.get_publications_by_DOI(DOI.strip(), is_refeered),
                                                                is_refeered=is_refeered))
    else:

        return bottle.template("publications_list",
                               dict(publications=publication.get_publications_by_DOI(DOI.strip(), is_refeered),
                                    username=username, is_admin=is_admin))


# the search pages
@bottle.get("/search_by_author")
def present_search():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)

    validate = validatePublications.ValidatePublications()

    return bottle.template("search_by_author", dict(username=username, is_admin=is_admin,
                                                    errors=validate.errors, author="",
                                                    start_date="", end_date=""))


@bottle.post("/search_by_author")
def process_search():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)

    author = bottle.request.forms.get("author")
    is_refeered = utilities.str2bool(bottle.request.forms.get("is_refeered", True))

    start_date = bottle.request.forms.get("start_date", None)
    end_date = bottle.request.forms.get("end_date", c.END_DATE)
    if not end_date: end_date = c.END_DATE

    if start_date or end_date:

        validate = validatePublications.ValidatePublications()

        try:
            validate.validate_dates(start_date, end_date)
        except validatePublications.ValidationException as e:
            return bottle.template("search_by_author", {'username': username, "is_refeered": is_refeered,
                                                        'start_date': start_date, 'is_admin': is_admin,
                                                        'end_date': end_date, 'author': author,
                                                        'errors': validate.errors})

        date_start = datetime.strptime(start_date, c.DATE_FORMAT)
        date_end = datetime.strptime(end_date, c.DATE_FORMAT)

        p = publication.get_closed_publications_author(author.lower(), is_refeered, date_start, date_end)

    else:
        p = publication.get_closed_publications_author(author.lower(), is_refeered)

    if not username:

        return bottle.template("public_publications_list", dict(publications=p,
                                                                is_refeered=is_refeered))
    else:

        return bottle.template("publications_list",
                               dict(publications=p, username=username, is_admin=is_admin))


@bottle.get("/detail_author_year")
def process_search():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)

    author = bottle.request.query.get("author", "")
    is_refeered = utilities.str2bool(bottle.request.query.get("is_refeered", True))

    year = bottle.request.query.get("year", None)

    validate = validatePublications.ValidatePublications()

    if year:
        try:
            validate.validate_year(year)
            start_date = ('01/01/%s' % year)
            end_date = ('12/31/%s' % year)
        except validatePublications.ValidationException as e:
            return bottle.redirect("metrics_authors")

        date_start = datetime.strptime(start_date, c.DATE_FORMAT)
        date_end = datetime.strptime(end_date, c.DATE_FORMAT)

        p = publication.get_closed_publications_author(author.lower(), is_refeered, date_start, date_end)

    else:

        p = publication.get_closed_publications_author(author.lower(), is_refeered)

    if not username:

        return bottle.template("public_publications_list", dict(publications=p,
                                                                is_refeered=is_refeered))
    else:

        return bottle.template("publications_list",
                               dict(publications=p, username=username, is_admin=is_admin))

@bottle.get("/detail_by_year")
def process_search():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)

    is_refeered = utilities.str2bool(bottle.request.query.get("is_refeered", True))

    year = bottle.request.query.get("year", None)

    validate = validatePublications.ValidatePublications()

    if year:
        try:
            validate.validate_year(year)
            start_date = ('01/01/%s' % year)
            end_date = ('12/31/%s' % year)
        except validatePublications.ValidationException as e:
            return bottle.redirect("metrics_authors")

        date_start = datetime.strptime(start_date, c.DATE_FORMAT)
        date_end = datetime.strptime(end_date, c.DATE_FORMAT)

        p = publication.get_closed_publications(is_refeered, date_start, date_end)

    else:

        return bottle.redirect("metrics_authors")

    if not username:

        return bottle.template("public_publications_list", dict(publications=p,
                                                                is_refeered=is_refeered))
    else:

        return bottle.template("publications_list",
                               dict(publications=p, username=username, is_admin=is_admin))



@bottle.get("/search_by_mission")
def present_search():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)
    validate = validatePublications.ValidatePublications()

    return bottle.template("search_by_mission", dict(username=username,
                                                     is_admin=is_admin, errors=validate.errors,
                                                     mission="", start_date="", end_date=""))


@bottle.post("/search_by_mission")
def process_search():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)

    mission = bottle.request.forms.get("mission")
    is_refeered = utilities.str2bool(bottle.request.forms.get("is_refeered", True))

    start_date = bottle.request.forms.get("start_date", None)
    end_date = bottle.request.forms.get("end_date", c.END_DATE)

    if start_date and end_date:

        validate = validatePublications.ValidatePublications()

        try:
            validate.validate_dates(start_date, end_date)
        except validatePublications.ValidationException as e:
            return bottle.template("search_by_mission", {'username': username, "is_refeered": is_refeered,
                                                         'start_date': start_date, 'is_admin': is_admin,
                                                         'end_date': end_date, 'errors': validate.errors,
                                                         'mission': mission})

        date_start = datetime.strptime(start_date, c.DATE_FORMAT)
        date_end = datetime.strptime(end_date, c.DATE_FORMAT)

        p = publication.get_closed_publications_mission(mission, is_refeered, date_start, date_end)

    else:
        p = publication.get_closed_publications_mission(mission, is_refeered)

    if not username:

        return bottle.template("public_publications_list", dict(publications=p,
                                                                is_refeered=is_refeered))
    else:

        return bottle.template("publications_list",
                               dict(publications=p, username=username, is_admin=is_admin))


@bottle.get("/search_by_journal")
def present_search():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)
    validate = validatePublications.ValidatePublications()


    return bottle.template("search_by_journal", dict(username=username, is_admin=is_admin, errors=validate.errors,
                                                     start_date="", end_date="", journal=""))


@bottle.post("/search_by_journal")
def process_search():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)

    journal = bottle.request.forms.get("journal")
    is_refeered = utilities.str2bool(bottle.request.forms.get("is_refeered", True))

    start_date = bottle.request.forms.get("start_date", None)
    end_date = bottle.request.forms.get("end_date", c.END_DATE)
    year = bottle.request.forms.get("year", None)

    validate = validatePublications.ValidatePublications()

    if start_date and end_date:
        try:
            validate.validate_dates(start_date, end_date)
        except validatePublications.ValidationException as e:
            return bottle.template("search_by_journal", {'username': username, "is_refeered": is_refeered,
                                                         'start_date': start_date, 'is_admin': is_admin,
                                                         'end_date': end_date, 'errors': validate.errors,
                                                         'journal': journal})

        date_start = datetime.strptime(start_date, c.DATE_FORMAT)
        date_end = datetime.strptime(end_date, c.DATE_FORMAT)

        p = publication.get_closed_publications_journal(journal, is_refeered, date_start, date_end)

    else:

        p = publication.get_closed_publications_journal(journal, is_refeered)

    if not username:

        return bottle.template("public_publications_list", dict(publications=p,
                                                                is_refeered=is_refeered))
    else:

        return bottle.template("publications_list",
                               dict(publications=p, username=username, is_admin=is_admin))

@bottle.get("/journals_publications_detail")
def process_search():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)

    journal = bottle.request.query.get("journal", "").replace("!", "&")
    is_refeered = utilities.str2bool(bottle.request.query.get("is_refeered", True))

    year = bottle.request.query.get("year", None)

    validate = validatePublications.ValidatePublications()

    if year:
        try:
            validate.validate_year(year)
            start_date = ('01/01/%s' % year)
            end_date = ('12/31/%s' % year)
        except validatePublications.ValidationException as e:
            return bottle.template("journal_metrics", {'username': username, 'errors': validate.errors,
                                                        'journal': journal})

        date_start = datetime.strptime(start_date, c.DATE_FORMAT)
        date_end = datetime.strptime(end_date, c.DATE_FORMAT)

        p = publication.get_closed_publications_journal(journal, is_refeered, date_start, date_end)

    else:

        p = publication.get_closed_publications_journal(journal, is_refeered)

    if not username:

        return bottle.template("public_publications_list", dict(publications=p,
                                                                is_refeered=is_refeered))
    else:

        return bottle.template("publications_list",
                               dict(publications=p, username=username, is_admin=is_admin))


@bottle.get("/missions_publications_detail")
def process_search():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)

    mission = bottle.request.query.get("mission", "")
    is_refeered = utilities.str2bool(bottle.request.query.get("is_refeered", True))

    year = bottle.request.query.get("year", None)

    validate = validatePublications.ValidatePublications()

    if year:
        try:
            validate.validate_year(year)
            start_date = ('01/01/%s' % year)
            end_date = ('12/31/%s' % year)
        except validatePublications.ValidationException as e:
            return bottle.redirect("metrics_missions")

        date_start = datetime.strptime(start_date, c.DATE_FORMAT)
        date_end = datetime.strptime(end_date, c.DATE_FORMAT)

        p = publication.get_closed_publications_mission(mission, is_refeered, date_start, date_end)

    else:

        p = publication.get_closed_publications_mission(mission, is_refeered)

    if not username:

        return bottle.template("public_publications_list", dict(publications=p,
                                                                is_refeered=is_refeered))
    else:

        return bottle.template("publications_list",
                               dict(publications=p, username=username, is_admin=is_admin))




@bottle.get("/missions_author_publications_detail")
def process_search():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_admin = sessions.get_admin(cookie)

    mission = bottle.request.query.get("mission", "")
    author = bottle.request.query.get("author", "")
    is_refeered = utilities.str2bool(bottle.request.query.get("is_refeered", True))

    p = publication.get_closed_publications_author(author, is_refeered, None, None, mission)

    if not username:

        return bottle.template("public_publications_list", dict(publications=p,
                                                                is_refeered=is_refeered))
    else:

        return bottle.template("publications_list",
                               dict(publications=p, username=username, is_admin=is_admin))


# here the publications to validate
@bottle.get('/validate_publications')
@valide_user()
def show_validation():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_refeered = utilities.str2bool(bottle.request.query.get("is_refeered", True))

    pub = publication.get_publication_to_validate(username, is_refeered)

    return bottle.template('publications_list_to_validate', dict(username=username, publications=pub))


@bottle.post('/invalidate_publications')
@valide_user()
def process_validation():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    biblicode_toinvalidate = bottle.request.forms.getlist('biblicode')

    errors, msg = [], []
    msg_str, err_str = None, None

    for biblicode in biblicode_toinvalidate:

        if not publication.invalidate_publication(biblicode, username):
            errors.append(biblicode)
        else:
            msg.append(biblicode)

    if not biblicode_toinvalidate:
         msg.append(c.publications_confirm)

    if msg:
        msg_str = "Publications invalidate: <br> %s" % '<br> '.join(msg)
    if errors:
        err_str = "error validating publications:<br> %s" % '<br>'.join(errors)

    return bottle.template("user", dict(username=username, msg=msg_str, errors=err_str))


@bottle.post('/publications_update_missions')
@valide_user()
def process_missions_update():

    id = bottle.request.forms.get("biblicode")
    value = bottle.request.forms.get("missions")
    biblicode = id.split("-")[1]
    missions_list = value.split(",")

    if not publication.update_missions(biblicode, missions_list):
        return "error updating missions"
    else:
        return '<br>'.join(missions_list)



@bottle.get('/logout')
def process_logout():
    cookie = bottle.request.get_cookie("session")
    sessions.end_session(cookie)
    bottle.response.set_cookie("session", "")
    bottle.redirect("/login")


@bottle.get("/welcome")
def present_welcome():
    # check for a cookie, if present, then extract value

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)  # see if user is logged in
    if username is None:
        print "welcome: can't identify user...contact administrator to obtain user and pwd"
        bottle.redirect("/login")

    return bottle.template("welcome", {'username': username})


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='python publication.py will start the publications service')
    parser.add_argument('-d', '--dir', help='where to find the statics files', required=True)
    parser.add_argument('-t', '--tmp', help='tmp dir where to create pdf files', required=True)
    args = vars(parser.parse_args())
 
    DOC_ROOT = args['dir']
    TMP_DIR = args['tmp']

    bottle.debug(True)
    #bottle.run(host='localhost', port=8084, reloader=True)  # Start the webserver running and wait for requests
    from paste import httpserver
    httpserver.serve(app, host='0.0.0.0', port='8084')




