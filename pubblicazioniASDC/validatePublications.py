__author__ = 'fmoscato'

import re
from datetime import datetime


import constants as c


__USER_RE__ = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
__PASS_RE__ = re.compile(r"^.{3,20}$")
__EMAIL_RE__ = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
__NAME_RE__ = re.compile(r"^[a-zA-Z0-9_-]{3,40}$")
__URL_RE__ = re.compile(r'^http?://'  # http:// or https://
                        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                        r'(?::\d+)?', re.IGNORECASE)


class ValidationException(Exception):
    pass

class ValidatePublications(object):

    def __init__(self):

        self.errors = {}
        self.errors['general'] = ""
        self.errors['username_error'] = ""
        self.errors['name_error'] = ""
        self.errors['password_error'] = ""
        self.errors['verify_error'] = ""
        self.errors['email_error'] = ""
        self.errors['start_date_error'] = ""
        self.errors['end_date_error'] = ""
        self.errors['biblicode'] = ""
        self.errors['title'] = ""
        self.errors['authors'] = ""
        self.errors['magazine_error'] = ""
        self.errors['URL_error'] = ""
        self.errors['asdc_authors'] = ""
        self.errors['error_year'] = ""


    def validate_signup(self, username, password, verify, email, start_date, end_date):
        """
        used for add user form
        param : takes the values to validate
        return: void
        """

        if not username:
            self.errors['username_error'] = "invalid username"
            raise ValidationException()
        if not email:
            self.errors['email_error'] = "email mandatory"
            raise ValidationException()
        if not start_date:
            self.errors['start_date_error'] = "start date mandatory"
            raise ValidationException()
        elif start_date:
            try:
                datetime.strptime(start_date.rstrip(), c.DATE_FORMAT)
            except ValueError as e:
                self.errors['start_date_error'] = "invalid start date"
                raise ValidationException()
        if end_date:
            try:
                datetime.strptime(end_date.rstrip(), c.DATE_FORMAT)
            except ValueError as e:
                self.errors['end_date_error'] = "invalid end date"
                raise ValidationException()

        if not __USER_RE__.match(username):
            self.errors['username_error'] = "invalid username. try just letters and numbers"
            raise ValidationException()

        if not __PASS_RE__.match(password):
            self.errors['password_error'] = "invalid password."
            raise ValidationException()
        if password != verify:
            self.errors['verify_error'] = "password must match"
            raise ValidationException()
        if not __EMAIL_RE__.match(email):
            self.errors['email_error'] = "invalid email address"
            raise ValidationException()

    def validate_form_mission(self, mission, start_date, end_date):
        """
        used for add mission form
        param : takes the values to validate
        return: void
        """

        if not __NAME_RE__.match(mission):
            self.errors['name_error'] = "invalid name. try just letters and numbers"
            raise ValidationException()

        if not start_date:
            self.errors['start_date_error'] = 'start date mandatory'
            raise ValidationException()
        elif start_date:
            try:
                datetime.strptime(start_date.rstrip(), c.DATE_FORMAT)
            except ValueError as e:
                self.errors['start_date_error'] = "invalid start date"
                raise ValidationException()
        if end_date:
            try:
                datetime.strptime(end_date.rstrip(), c.DATE_FORMAT)
            except ValueError as e:
                self.errors['end_date_error'] = "invalid end date"
                raise ValidationException()

    def validate_dates(self, start_date, end_date=None):
        """
        used for date forms
        param : takes the values to validate
        return: void
        """
        if not start_date:
            self.errors['start_date_error'] = 'missing start date'
            raise ValidationException()
        elif start_date:
            try:
                datetime.strptime(start_date.rstrip(), c.DATE_FORMAT)
            except ValueError as e:
                self.errors['start_date_error'] = "invalid start date"
                raise ValidationException()
        if end_date:
            try:
                datetime.strptime(end_date.rstrip(), c.DATE_FORMAT)
            except ValueError as e:
                self.errors['end_date_error'] = "invalid end date"
                raise ValidationException()



    def validate_year(self, year):

        try:
            datetime.strptime(year, "%Y")
        except ValueError as e:
            self.errors['error_year'] = 'invalid year'
            raise ValidationException()

    def validate_publication_form(self, kwargs):
        """
        used in add publication form
        raised ValidationException if a condition is not valide
        return: void
        """

        if not kwargs['biblicode']:
            self.errors['biblicode'] = "biblicode mandatory"
            raise ValidationException()
        if not kwargs['title']:
            self.errors['title'] = "title mandatory"
            raise ValidationException()
        if not kwargs['authors']:
            self.errors['authors'] = "authors mandatory"
            raise ValidationException()
        if not kwargs['asdc_authors']:
            self.errors['asdc_authors'] = "asdc authors mandatory"
            raise ValidationException()
        if not kwargs['pub_date']:
            self.errors['start_date_error'] = "publication date mandatory"
            raise ValidationException()
        elif kwargs['pub_date']:
            try:
                datetime.strptime(kwargs["pub_date"], c.DATE_FORMAT)
            except ValueError as e:
                self.errors['start_date_error'] = "invalid pub date"
                raise ValidationException()
        if not kwargs['magazine']:
            self.errors['magazine_error'] = "Journal mandatory"
        if kwargs["URL"]:
            if not __URL_RE__.search(kwargs["URL"]):
                self.errors["URL_error"] = "invalid URL"
                raise ValidationException()

    def validate_add_role(self, role=None):
        """
        used in add role form
        """
        if not role:
            self.errors['name_error'] = "Role mandatory"
            raise ValidationException()
        elif not __NAME_RE__.match(role):
            self.errors['name_error'] = "invalid Role name. try just letters and numbers"
            raise ValidationException()


