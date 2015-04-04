import json
import datetime
from time import strftime

from google.appengine.ext.ndb import GeoPt

from model.model import *

class JsonSerializer(json.JSONEncoder):

    def default(self, obj):
        
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%dT%H:%M:%SZ")

        elif isinstance(obj, GeoPt):
            return {'lat': obj.lat, 'lon': obj.lon}
            
        elif isinstance(obj, BaseModel):
        	return obj.to_dict()

        return json.JSONEncoder.default(self, obj)