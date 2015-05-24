import urls 
import urllib2
import httplib

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

_KEY_LIST = ["Title", "Authors", "Publication Date", "DOI", "Publication",
             "Bibliographic Code", "Astronomy Keywords", "Keywords", "Origin", "Abstract"]
_KEY_LIST_TO_DROP = ["Affiliation", "Abstract Copyright", "Category"]


class ADSDownload(object):

    def __init__(self):

        self.refeered_url = urls.refeered
        self.not_refeered_url = urls.not_refeered

    def download(self, start_date, end_date, users, is_refeered=True):

        if is_refeered:
            url = self.refeered_url
        else:
            url = self.not_refeered_url

        pub = {}
        request = url % (users, start_date.month, start_date.year, end_date.month, end_date.year)

        try:

            response = urllib2.urlopen(request)
            data = response.read()
            pub = self._clean_data(data)

 
        except urllib2.HTTPError, e:
            log.error('HTTPError = ' + str(e.code))
        except urllib2.URLError, e:
            log.error('URLError = ' + str(e.reason))
        except httplib.HTTPException, e:
            log.error('HTTPException')
        except Exception:
            import traceback
            log.error('generic exception: ' + traceback.format_exc())

        return pub

    def _clean_data(self, data):

        #remove the part of the output
        data_to_consider = (data.split("Query Parameters"))[0]
        #define an array of publications
        arr = data_to_consider.split("Title:")
   
        publications = []

        for i in range(1, len(arr)):

            d = "Title:"+arr[i]
            pub_info = {}
            is_new = True
            tmp_key = None
            for line in d.split('\n'):

                if not line or line == "":
                    continue

                values = line.split(":")
                the_key = (values[0]).strip()

                if the_key in _KEY_LIST:
                    pub_info[the_key] = ' '.join([(values[i]).strip() for i in range(1, len(values))])
                    is_new = False
                    tmp_key = the_key
                elif not is_new and the_key not in _KEY_LIST_TO_DROP:
                    pub_info[tmp_key] = "%s %s" % (pub_info[tmp_key], ' '.join([v.strip() for v in values]))
                elif the_key in _KEY_LIST_TO_DROP:
                    is_new = True

            publications.append(pub_info)

        return publications
