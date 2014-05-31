from google.appengine.ext import ndb
from webapp2_extras import security
import webapp2_extras.appengine.auth.models
import time

class User(webapp2_extras.appengine.auth.models.User):
  def set_password(self, raw_password):
    self.password = security.generate_password_hash(raw_password, length=22)

  @classmethod
  def get_by_auth_token(cls, user_id, token, subject='auth'):
    token_key = cls.token_model.get_key(user_id, subject, token)
    user_key = ndb.Key(cls, user_id)
    valid_token, user = ndb.get_multi([token_key, user_key])
    if valid_token and user:
        timestamp = int(time.mktime(valid_token.created.timetuple()))
        return user, timestamp

    return None, None