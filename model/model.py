#!/usr/bin/env python

import unicodedata

from google.appengine.ext import ndb
from google.appengine.api import users

PROVIDER_GOOGLE = 'google'
PROVIDER_FACEBOOK = 'facebook'

DATE_FORMAT_STR = '%Y-%m-%dT%H:%MZ'

class BaseModel(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def all(cls):
        return cls.query().order(-cls.created)

    def to_dict(self, exclude=None):
        dict = super(BaseModel, self).to_dict(exclude=exclude)
        dict['id'] = self.key.id()
        return dict

    def __hash__(self):
        return self.key.id()

    def __eq__(self, other):
        return self.key.id() == other.key.id()
      

class UserData(BaseModel):
    auth_provider = ndb.StringProperty(choices=[PROVIDER_GOOGLE, PROVIDER_FACEBOOK], required=True)
    name = ndb.StringProperty(default='')
    search_name = ndb.ComputedProperty(lambda self: unicodedata.normalize('NFKD', unicode(self.name)).encode('ascii','ignore').lower())
    email = ndb.StringProperty(required=True)

    @classmethod
    def create_user(cls, external_user, provider, user_key):

        user = UserData(auth_provider=provider)
        user.key = user_key
        
        if provider == PROVIDER_GOOGLE:
            user.email = external_user.email()
            user.name = external_user.nickname()

        elif provider == PROVIDER_FACEBOOK:
            pass

        else:
            raise ValueError('Provider is unknown: ' + provider)

        user.put()
        return user


class Meeting(BaseModel):
    owner = ndb.KeyProperty(kind=UserData, required=True)
    venue_forsquare_id = ndb.StringProperty(required=True)
    location = ndb.GeoPtProperty()
    earliest_possible_start = ndb.DateTimeProperty(required=True)
    latest_possible_start = ndb.DateTimeProperty()
    topic = ndb.StringProperty(required=True)
    type = ndb.StringProperty(required=True, choices=['drink', 'lunch', 'brunch'])
    tags = ndb.StringProperty(repeated=True)


class MeetingCounter(ndb.Model):
    count = ndb.IntegerProperty(default=0)

    @classmethod
    @ndb.transactional
    def increment(cls, user_key):
        counter = cls.get_by_id(user_key.id())
        if counter is None:
            counter = cls(id=user_key.id())

        counter.count += 1
        counter.put()


class MeetingRequest(BaseModel):
    meeting = ndb.KeyProperty(kind=Meeting, required=True)
    state = ndb.StringProperty(default='pending', choices=['pending', 'accepted', 'rejected'])

    @classmethod
    def for_meeting(cls, meeting_id, state=None):
        if state is None:
            query = cls.query(cls.meeting==ndb.Key(Meeting, meeting_id))
        else:
            query = cls.query(cls.meeting==ndb.Key(Meeting, meeting_id), cls.state == state)

        return query.order(-cls.created)

    def to_dict(self):
        return super(MeetingRequest, self).to_dict(exclude=['meeting'])


