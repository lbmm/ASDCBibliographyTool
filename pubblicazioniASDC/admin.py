__author__ = 'fmoscato'

from datetime import datetime
import json
from collections import OrderedDict

import pymongo
import bottle

import authentication as auth
import publicationDAO
import sessionDAO
import userDAO
import missionDAO
import roleDAO
import pubUtilities as p
import handle_asdc_author
import constants as c
import ADS_download
import validatePublications



#create the app for the admin interface

admin_app = bottle.Bottle()

connection_string = ""
connection = pymongo.MongoClient(connection_string)
database = connection.publication

publication = publicationDAO.PublicationDAO(database)
users = userDAO.UserDAO(database)
missions = missionDAO.MissionDAO(database)
sessions = sessionDAO.SessionDAO(database)
roles = roleDAO.RoleDAO(database)
valid_admin = auth.authenticator(sessions)



"""
 admin can

A- handle users
 A.1 - add user
 A.2 - change validity of the user
 A.3 - remove a user
 A.4 - list users (valide or not, and for a time period)

B-handle missions
 B.1 - add mission
 B.2 - change validity of a mission
 B.3 - remove a mission
 B.4 - list the missions (valide or not, and for a time period)

B.i - handle users role
 B.i.1 - add role
 B.i.2 - remove role

C- handle publications
 C.1 - start new period of publication download
 C.2 - verify if all users validate their publications
 C.3 - close a period
 C.4 - list valide publications for a period
 C.5 - download publications
 C.6 - search (for biblicode, DOI, author, mission, magazine)

D- displays the initial admin page
"""


@bottle.get("/admin")
@valid_admin()
def present_admin():
    # check for a cookie, if present, then extract value

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)  # see if user is logged in
    return bottle.template("admin", dict(username=username, msg= '', errors=''))


########################
#                      #
#  admin user part     #
#                      #
########################

@bottle.get('/add_user')
@valid_admin()
def present_add_user():
    
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    m = missions.get_valide_missions()
    r = roles.get_roles()

    validate = validatePublications.ValidatePublications()

    return bottle.template("add_user",
                           dict(username=username, username_to_add="", password="",
                                password_error="", name="", lastname="",
                                start_date="", end_date="",
                                missions=m, roles=r, role_selected="",
                                email="", errors=validate.errors, admin=""))


@bottle.post('/add_user')
@valid_admin()
def process_add_user():
    
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    username_to_add = bottle.request.forms.get("username")
    name = bottle.request.forms.get("name")
    lastname = bottle.request.forms.get("lastname")
    password = bottle.request.forms.get("password")
    email = bottle.request.forms.get("email")
    missions_selected = bottle.request.forms.getall("missions")
    role_selected = bottle.request.forms.get("role")
    admin = p.str2bool(bottle.request.forms.get("admin"))
    start_date = bottle.request.forms.get("start_date")
    end_date = bottle.request.forms.get("end_date", None)
    verify = bottle.request.forms.get("verify")
    
    m = missions.get_valide_missions()

    r = roles.get_roles()
    # set these up in case we have an error case

    validate = validatePublications.ValidatePublications()

    try:
        validate.validate_signup(username_to_add, password, verify, email, start_date, end_date)
    except validatePublications.ValidationException as e:
        return bottle.template("add_user", dict(username=username,
                                                username_to_add=username_to_add, name=name, lastname=lastname,
                                                password=password, email=email, admin=admin, errors=validate.errors,
                                                start_date=start_date, end_date=end_date, missions=m,
                                                missions_selected=missions_selected, roles=r,
                                                role_selected=role_selected))


    if not users.add_user(username=username_to_add, name=name, lastname=lastname,
                          password=password, email=email, admin=admin,
                          start_date=start_date, end_date=end_date,
                          missions=missions_selected, role=role_selected):
        # this was a duplicate
        validate.errors['username_error'] = 'username already taken'
        return bottle.template("add_user", dict(username=username,
                                                username_to_add=username_to_add, name=name, lastname=lastname,
                                                password=password, email=email, admin=admin,
                                                start_date=start_date, end_date=end_date, missions=m,
                                                missions_selected=missions_selected, roles=r,
                                                role_selected=role_selected,
                                                errors=validate.errors))

    msg = "user %s added" % username_to_add
    return bottle.template("admin", dict(username=username, msg=msg, errors=''))




@bottle.get('/list_users')
@bottle.get('/list_valide_users')
@valid_admin()
def present_list():
    return bottle.template('users_list')


@bottle.get('/list_users')
@valid_admin()
def process_list():
    cookie = bottle.request.get_cookie("session")

    username = sessions.get_username(cookie)

    l = users.get_users()

    return bottle.template('users_list', dict(users=l,
                                              username=username))


@bottle.get('/list_valide_users')
@valid_admin()
def process_list():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    l = users.get_valide_users()
    return bottle.template('users_list', dict(users=l,
                                              username=username))


@bottle.get('/json_missions')
def present_json():

    keys = OrderedDict((m['name'], m['name']) for m in missions.get_missions())
    return json.dumps(keys)


@bottle.get('/json_authors')
def present_json_authors():

    keys = OrderedDict((u['username'] + "_" + u['pub_name'], u['name'] + " " + u['lastname']) for u in users.get_users())
    return json.dumps(keys)


@bottle.get('/json_roles')
def present_json_authors():

    keys = OrderedDict((r['role'], r['role']) for r in roles.get_roles())
    return json.dumps(keys)


#update is done by ajax
@bottle.post('/users_update_email')
def process_update():

    id = bottle.request.forms.get("user_id")
    user_id = id.split('-')[1]
    email = bottle.request.forms.get("email")

    if not users.update_email(user_id, email):
        return "error updating email"
    else:
        return email

@bottle.post('/users_update_missions')
def process_missions_update():

    id = bottle.request.forms.get("user_id")
    user_id = id.split("-")[1]
    value = bottle.request.forms.get("missions")

    missions_list = value.split(",")

    if not users.update_missions(user_id, missions_list):
        return "error updating missions"
    else:
        return '<br>'.join(missions_list)

#update is done by ajax
@bottle.post('/users_update_role')
def process_update():

    id = bottle.request.forms.get("user_id")
    user_id = id.split('-')[1]
    role = bottle.request.forms.get("role")

    if not users.update_role(user_id, role):
        return "error updating role"
    else:
        return role


@bottle.post('/close_users_validity')
@valid_admin()
def process_close_users_validity():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    users_to_close = bottle.request.forms.getlist("username")

    errors, msg = [], []
    msg_str, err_str = None, None

    for usr in users_to_close:

        if not users.close_validity_user(usr):
            errors.append(usr)
        else:
            msg.append(usr)

    if msg:
        msg_str = "closed the validity of the following users: %s " % '<br> '.join(msg)
    if errors:
        err_str = "error closing users validity for the following users: %s" % '<br>'.join(errors)

    return bottle.template("admin", dict(username=username, msg=msg_str, errors=err_str))




#remove is done by ajax
@bottle.post('/remove_user')
def process_remove():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    user_id = bottle.request.forms.get("user")

    if not users.remove_user(user_id):
        return bottle.HTTPResponse(status=202, body="error")
    else:
        return bottle.HTTPResponse(status=200, body="success")


########################
#                      #
#   Mission part       #
#                      #
########################


@bottle.get('/add_mission')
@valid_admin()
def present_add_mission():
   
    username = bottle.request.forms.get("username")
    cookie = bottle.request.get_cookie("session")

    validate = validatePublications.ValidatePublications()

    return bottle.template("add_mission",
                           dict(username=username, mission="",
                                start_date="", end_date="",
                                error=validate.errors))


@bottle.post('/add_mission')
@valid_admin()
def process_add_mission():

    username = bottle.request.forms.get("username")

    mission = bottle.request.forms.get("mission")
    start_date = bottle.request.forms.get("start_date")
    end_date = bottle.request.forms.get("end_date", None)

    validate = validatePublications.ValidatePublications()

    try:
        validate.validate_form_mission(mission, start_date, end_date)
    except validatePublications.ValidationException as e:
        return bottle.template("add_mission", dict(username=username,
                                                   mission=mission,
                                                   start_date=start_date,
                                                   end_date=end_date,
                                                   error=validate.errors))
    if not missions.add_mission(name=mission,
                                start_date=start_date,
                                end_date=end_date):
            # this was a duplicate
            validate.errors['name_error'] = "Mission Name already in use. Please choose another"
            return bottle.template("add_mission", dict(username=username,
                                                       mission=mission,
                                                       start_date=start_date,
                                                       end_date=end_date,
                                                       error=validate.errors))
    msg = "mission %s added" % mission
    return bottle.template("admin", dict(username=username, msg=msg, errors=''))
      

@bottle.get('/list_missions')
@valid_admin()
def present_list():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)  # see if user is logged in

    m = missions.get_missions()
    
    return bottle.template('missions_list', dict(missions=m, username=username, msg=""))


@bottle.post('/list_missions')
@valid_admin()
def process_list():
    """


    :return:
    """
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    start_date = bottle.request.forms.get("start_date", None)
    end_date = bottle.request.forms.get("end_date", c.END_DATE)

    if start_date and end_date:

        date_start = datetime.strptime(start_date, c.DATE_FORMAT)
        date_end = datetime.strptime(end_date, c.DATE_FORMAT)

        m = missions.get_valide_missions(date_start, date_end)

    else:
        m = missions.get_missions()

    return bottle.template('missions_list', dict(missions=m, username=username, msg=""))


@bottle.get('/list_valide_missions')
@valid_admin()
def process_list():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    m = missions.get_valide_missions()

    return bottle.template('missions_list', dict(missions=m, username=username, msg=""))

@bottle.post('/close_missions_validity')
@valid_admin()
def process_close_users_validity():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    missions_to_close = bottle.request.forms.getlist("mission")

    errors, msg = [], []
    msg_str, err_str = None, None

    for m in missions_to_close:

        if not missions.close_validity_mission(m):
            errors.append(m)
        else:
            msg.append(m)

    if msg:
        msg_str = "closed the validity of the following missions: <br> %s " % '<br> '.join(msg)
    if errors:
        err_str = "error closing users validity for the following missions: <br> %s " % '<br>'.join(errors)

    return bottle.template("admin", dict(username=username, msg=msg_str, errors=err_str))


@bottle.post('/remove_mission')
def process_remove():
    mission = bottle.request.forms.get("mission")

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    if not missions.remove_mission(mission):
        return bottle.HTTPResponse(status=202, body="error")
    else:
        return bottle.HTTPResponse(status=200, body='success')


########################
#                      #
#   Roles part         #
#                      #
########################


@bottle.get('/add_role')
@valid_admin()
def present_add_role():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    validate = validatePublications.ValidatePublications()

    return bottle.template("add_role",
                           dict(username=username, role="",
                                error=validate.errors))


@bottle.post('/add_role')
@valid_admin()
def process_add_mission():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    role = bottle.request.forms.get("role")

    validate = validatePublications.ValidatePublications()

    try:
        validate.validate_add_role(role)
    except validatePublications.ValidationException as e:
        return bottle.template("add_role", dict(username=username,
                                                role=role,
                                                error=validate.errors))
    if not roles.add_role(role=role):
            validate.errors['name_error'] = "role already in use. Please choose another"
            return bottle.template("add_role", dict(username=username,
                                                    role=role,
                                                    error=validate.errors))
    msg = "role %s added" % role
    return bottle.template("admin", dict(username=username, msg=msg, errors=''))


@bottle.get('/list_roles')
@valid_admin()
def present_list():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)  # see if user is logged in

    r = roles.get_roles()

    return bottle.template('roles_list', dict(roles=r, username=username, msg=""))


@bottle.post('/remove_role')
def process_remove():

    code = bottle.request.forms.get("code")

    if not roles.remove_role(code):
        return bottle.HTTPResponse(status=202, body="error")
    else:
        return bottle.HTTPResponse(status=200, body='success')




########################
#                      # 
#   Publications part  #
#                      #
########################

@bottle.get('/ads_download')
@valid_admin()
def present_download():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)  # see if user is logged in
    is_refeered = p.str2bool(bottle.request.query.get("is_refeered", True))
    default_errors = {'start_date_error': "", 'end_date_error': ""}
    return bottle.template("ads_download", {'username': username, "is_refeered": is_refeered,
                                            'start_date': "", 'end_date': "",
                                            'asdc_authors': users.get_users(),
                                            'errors': default_errors})


#il download e' fatto per
# 1- prendere tutte le pubblicazioni di quel periodo
# 2- inserire nel db
# 3- avvertire utenti che ci sono pubblicazioni da validare
@bottle.post('/ads_download')
@valid_admin()
def process_download():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    is_refeered = p.str2bool(bottle.request.forms.get("is_refeered", True))
    start_date_str = bottle.request.forms.get("start_date")
    end_date_str = bottle.request.forms.get("end_date")
    asdc_author_list = bottle.request.forms.getall("asdc_authors")

    validate = validatePublications.ValidatePublications()

    try:
        validate.validate_dates(start_date_str, end_date_str)
    except validatePublications.ValidationException as e:
        return bottle.template("ads_download", {'username': username, "is_refeered": is_refeered,
                                                'start_date': start_date_str, 'asdc_authors': users.get_users(),
                                                'end_date': end_date_str, 'errors': validate.errors})

    if not end_date_str: end_date_str = c.END_DATE

    date_start = datetime.strptime(start_date_str, c.DATE_FORMAT)
    date_end = datetime.strptime(end_date_str, c.DATE_FORMAT)

    single_authors = False
    if asdc_author_list:
        users_list = users.check_users_validity(asdc_author_list, date_start, date_end)
        single_authors = True
    else:
        #prendere tutti gli utenti ASDC validi in quel periodo
        users_list = users.get_valide_users(date_start, date_end)

    users_name_list_tmp = [users.get_pub_name(user['name'], user['lastname']) for user in users_list]
    users_name_list = [item for sublist in users_name_list_tmp for item in sublist]


    ads = ADS_download.ADSDownload()
    publications_from_ads = ads.download(date_start, date_end, ".%3B+".join(users_name_list), is_refeered)
    errors, errors_utf8 = [], []
    asdc_author = []


    for l in publications_from_ads:

        if single_authors : users_list = users.get_valide_users(date_start, date_end)

        authors, asdc_author = handle_asdc_author.clean_asdc_authors(l['Authors'], users_list)
        try:

            if not publication.add_publication(biblicode=l["Bibliographic Code"],
                                               Title=l["Title"],
                                               authors=authors,
                                               # all this to have a unique flat list of missions for the asdc_author in the pub
                                               mission=list(set(sum([user.get("missions", None) for user in users_list
                                                                 if user['username'] in asdc_author and "missions" in user], []))),
                                               pub_date=l["Publication Date"],
                                               DOI=l.get("DOI", ''),
                                               Keywords=l["Astronomy Keywords"] if "Astronomy Keywords" in l else l["Keywords"] if "Keywords" in l else "",
                                               Origin=l["Origin"],
                                               Publication=l['Publication'],
                                               Abstract=l["Abstract"],
                                               asdc_author=asdc_author,
                                               is_refeered=is_refeered):

                errors['publication_error'] = "publication error"
                return bottle.template("ads_download", errors)

        except pymongo.errors.InvalidStringData:
            errors_utf8.append("error inserting biblicode %s: not valide UTF-8 data" % l["Bibliographic Code"])
            continue


    for email in [user['email'] for user in users_list if user['username'] in asdc_author]:

        if not p.sendMail(email, c.SUBJECT_PUB_VALIDATION, c.BODY_MAIL_PUB_VALIDATION):
            print "error sending email user: %" % email

    #return the list of publications saved (they should be the same list)
    l = publication.get_open_publications(is_refeered, date_start, date_end)

    return bottle.template("publications_list", dict(publications=l, is_refeered=is_refeered,
                                                     username=username, is_admin=True,
                                                     errors_utf8=errors_utf8))



@bottle.get('/list_open_publications')
def present_close_period():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_refeered = p.str2bool(bottle.request.query.get("is_refeered", True))

    l = publication.get_open_publications(is_refeered)

    return bottle.template("publications_list", dict(publications=l, username=username,
                                                     is_refeered=is_refeered, is_admin=True))

@bottle.get('/close_publications_period')
@valid_admin()
def present_close_period():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_refeered = p.str2bool(bottle.request.query.get("is_refeered", True))
    default_errors = {'start_date_error': "", 'end_date_error': ""}


    return bottle.template('close_publications', dict(username=username, is_refeered=is_refeered,
                                                      start_date="", end_date="",
                                                      errors=default_errors))


@bottle.post('/close_publications_period')
@valid_admin()
def present_close_period():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    is_refeered = p.str2bool(bottle.request.forms.get("is_refeered", True))
    start_date_str = bottle.request.forms.get("start_date")
    end_date_str = bottle.request.forms.get("end_date")

    validate = validatePublications.ValidatePublications()

    try:
        validate.validate_dates(start_date_str, end_date_str)
    except validatePublications.ValidationException as e:
        return bottle.template("close_publications", {'username': username, "is_refeered": is_refeered,
                                                      'start_date': start_date_str,
                                                      'end_date': end_date_str, 'errors': validate.errors})


    if not end_date_str: end_date_str= c.END_DATE

    start_date = datetime.strptime(start_date_str, c.DATE_FORMAT)
    end_date = datetime.strptime(end_date_str, c.DATE_FORMAT)

    pub = publication.get_publications_to_close(is_refeered, start_date, end_date)

    return bottle.template('publications_list_to_close', dict(publications=pub, username=username,
                                                              is_refeered=is_refeered))


#remove is done by ajax
@bottle.post('/remove_publication')
@valid_admin()
def process_remove():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    bibcode = bottle.request.forms.get("biblicode")

    #here a special char is used to send biblicode that contains &
    #other wise the request will split the information

    bibcode = bibcode.replace("!", "&")

    if not publication.remove_publication(bibcode):
        return bottle.HTTPResponse(status=202, body="error")
    else:
        return bottle.HTTPResponse(status=200, body="success")


@bottle.get('/modify_valid_publication')
@valid_admin()
def show_modify_valid_publication():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_refeered = p.str2bool(bottle.request.query.get("is_refeered", True))
    default_errors = {'start_date_error': "", 'end_date_error': ""}


    return bottle.template('modify_publications', dict(username=username, is_refeered=is_refeered,
                                                       start_date="", end_date="",
                                                       errors=default_errors))

@bottle.post('/modify_valid_publication')
@valid_admin()
def process_modify_valid_publication():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    is_refeered = p.str2bool(bottle.request.forms.get("is_refeered", True))
    start_date_str = bottle.request.forms.get("start_date")
    end_date_str = bottle.request.forms.get("end_date")

    validate = validatePublications.ValidatePublications()

    try:
        validate.validate_dates(start_date_str, end_date_str)
    except validatePublications.ValidationException as e:
        return bottle.template("modify_publications", {'username': username, "is_refeered": is_refeered,
                                                       'start_date': start_date_str,
                                                       'end_date': end_date_str, 'errors': validate.errors})

    if not end_date_str: end_date_str= c.END_DATE

    start_date = datetime.strptime(start_date_str, c.DATE_FORMAT)
    end_date = datetime.strptime(end_date_str, c.DATE_FORMAT)

    pub = publication.get_closed_publications(is_refeered, start_date, end_date)

    return bottle.template('publications_list_to_modify', dict(publications=pub, username=username,
                                                               is_refeered=is_refeered))

@bottle.post('/publications_update_authors')
@valid_admin()
def process_missions_update():

    id = bottle.request.forms.get("biblicode")
    value = bottle.request.forms.get("authors")
    biblicode = id.split("-")[1]
    authors_list = value.split(",")


    if not publication.update_authors_mission(biblicode, authors_list):
        return "error updating authors"
    else:
        return '<br>'.join(['%s: True' % auth.split("_")[0] for auth in authors_list])




#close publication period
@bottle.post('/close_publications')
@valid_admin()
def process_validate():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)

    biblicode_to_close = bottle.request.forms.getlist("biblicode")

    errors, msg = [], []
    msg_str, err_str = None, None
    msg = []

    for bib in biblicode_to_close:

        if not publication.close_publication(bib):
            errors.append(bib)
        else:
            msg.append(bib)

    if msg:
        msg_str = "Publications closed: <br> %s" % '<br> '.join(msg)
    if errors:
        err_str = "error closing publications:<br> %s" % '<br> '.join(errors)
    return bottle.template("admin", dict(username=username, msg=msg_str, errors=err_str))

@bottle.get('/list_valide_publications')
def present_close_period():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    is_refeered = p.str2bool(bottle.request.query.get("is_refeered", True))

    l = publication.get_closed_publications(is_refeered)

    return bottle.template("publications_list", dict(publications=l, username=username,
                                                     is_refeered=is_refeered, is_admin=True))







