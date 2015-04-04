from datetime import datetime

from google.appengine.ext.ndb import GeoPt
from model.model import *

def format_to_date(date_str, format):
	return datetime.strptime(date_str, format)

def format_to_geo_pos(geo_pos_str):
	return GeoPt(geo_pos_str)