__author__ = 'fmoscato'

import pubUtilities
from collections import OrderedDict


"""
utilities module that handles the
syntax for the asdc author
"""

def clean_asdc_authors(auth_str, users_list):
    """
    rules to clean the asdc authors name:
    1- always keep the first 3 authors
    2- the asdc authors are underline in bold
    3- at the end append the 'et al' string, if still author

    param: long string for all authors
           list of valid asdc users at that period.
    return: string of cleaned user
"""

    arr_auth = auth_str.split(";")
    arr_auth = [pubUtilities.clean_string(auth) for auth in arr_auth]
    users_name = ["%s, %s" % (u['lastname'].title(),
                              ' '.join(["%s." % name[:1].upper() for name in u['name'].split()]))
                  for u in users_list]
    users_last_name = ["%s" % (u['lastname'].title()) for u in users_list]


    authors_cleaned = []
    asdc_author = []

    for i in range(len(arr_auth)):

        auth = (arr_auth[i]).strip()

        if i < 3:

          if auth in users_name or auth.split(",")[0] in users_last_name:
             authors_cleaned.append('<b> %s </b>' % auth)
             asdc_author.append((auth.split(",")[0]).lower())

          else:
             authors_cleaned.append(auth)

        elif auth in users_name or auth.split(",")[0] in users_last_name:
            authors_cleaned.append("...<b> %s </b>" % auth)
            asdc_author.append((auth.split(",")[0]).lower())

        if i == (len(arr_auth)-1) and auth not in users_name:
            authors_cleaned.append(" et al.")

    return '; '.join(authors_cleaned), asdc_author


def def_asdc_auth_auto_archiving(string_authors, asdc_auth):
    """
    takes a string and trying to recognize asdc_authors
    return cleaned string to save in DB
    """
    author_list = string_authors.split(";")
    arr_auth = [pubUtilities.clean_string(auth) for auth in author_list]

    authors_cleaned = []
    #dirty trick: my apologies
    #select all the pub_name that comes from the string encoded in the form (username_pubname)
    #for each authors I could have multiple pub_name (due to the multiple names)
    #I need only one, so discard the rest
    asdc_pub_name = [((asdc.split("_"))[1]).split(",")[0] for asdc in asdc_auth]
    for i in range(len(arr_auth)):

        auth = (arr_auth[i]).strip()

        for asdc_au in asdc_pub_name:
            only_lastname = (asdc_au.split("%2C"))[0]
            auth_to_compare = auth.lower()

            if auth_to_compare.startswith(only_lastname.lower()):
                if i < 3:
                    authors_cleaned.append('<b> %s </b>' % asdc_au.replace("%2C", ". "))
                else:
                    authors_cleaned.append('...<b> %s </b>' % asdc_au.replace("%2C", ". "))

            elif i < 3 and auth not in authors_cleaned:
                authors_cleaned.append(auth)

    authors_cleaned.append(" et al.")

    return '; '.join(authors_cleaned)


def update_asdc_authors(string_authors, auth_toremove):
    """
    it is call when a user not validate his/her publications
    param: take a long of string of authors
           authors to remove

    return: string with updated information for asdc author
    """
    author_list = string_authors.split(";")
    tags = ['<b>', '...<b>']
    for auth in author_list:
        for tag in tags:
            if (auth.strip()).startswith("%s %s" % (tag, auth_toremove.title())):
                author_list.remove(auth)
                break

    return '; '.join(author_list)

def overwrite_asdc_authors(string_authors,  asdc_auth):
    """
    takes the authors string and update regarding what the admins decide
    param: take a long string of authors
           authors to underline
    return: string with updated information for asdc author
    """

    repls = {'<b>': '', '</b>': '', '...': ''}
    string_clean = reduce(lambda a, kv: a.replace(*kv), repls.iteritems(), string_authors)
    author_list = string_clean.split(";")
    asdc_auth = OrderedDict((auth.split("_")[0], auth.split("_")[1]) for auth in asdc_auth)
    auth_dict = OrderedDict((auth.split(",")[0].lower().strip().replace(" ", ""), auth) for auth in author_list)


    append_last_element = False
    if next(reversed(auth_dict)).strip() == 'et al.':
        auth_dict.popitem()
        append_last_element = True

    for auth in asdc_auth.keys():
        auth_dict[auth] = '<b> %s </b>' % (asdc_auth[auth].replace("%2C", ", ")).replace("+", " ")


    if append_last_element:
        auth_dict.update({'  et al.': '  et al.'})

    return ';'.join(auth_dict.itervalues())



