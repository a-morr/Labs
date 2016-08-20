import json
import datetime

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

def date_decoder(dct):
    def dedate(s):
        # put stuff here
    
    # try to decode any value that looks like a date
    for i, k in dct.iteritems():
        try:
            dct[i] = dedate(k)
        except:
            continue
    return dct
