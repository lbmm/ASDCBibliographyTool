__author__ = 'fmoscato'

#dummy file with some constant values

END_DATE = "02/20/2020"

DATE_FORMAT = "%m/%d/%Y"

"""
Email sent when there was a new publication download
"""

SUBJECT_PUB_VALIDATION = "Nuove publicazioni da validare"

BODY_MAIL_PUB_VALIDATION = "Ci sono delle nuove publicazioni da validare."\
                            "Loggarsi nel sistema e validare le publicazioni."

"""
Email sent when a temporary publication is inserted
"""

SUBJECT_TMP_PUB = "Inserita nuova publicazione manuale"

BODY_TMP_PUB = "E' stata inserita una nuova pubblicazione dall'utente %s."\
                "Necessita approvazione da parte dell'amministratore"
"""
Email sent when admin confirm the temporary publication
"""

SUBJECT_ADMIN_CONFIRM_TMP_PUB = "La pubblicazione inserita e' stata validata"

BODY_ADMIN_CONFIRM_TMP_PUB = "La pubblicazione %s inserita e' stata validata dall'amministratore \n"\
                             "Dettagli della pubblicazione disponibili a questo link: " \
                             "/publication/%s"

"""
Email sent to recover the password
"""

SUBJECT_FORGOT_PASSWORD = "ASDC Bibliography tool"

BODY_FORGOT_PASSWORD = "Your password is %s"

"""
END
"""


URL_ADS = "http://adsabs.harvard.edu/abs/"

pdf_file_name = "publications_list"


years = [2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005,2004, 2003, 2002, 2001, 2000]