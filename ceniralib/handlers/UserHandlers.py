from google.appengine.ext import ndb

import logging
import os.path
import webapp2, jinja2
from .. import models
import re

from webapp2_extras import auth
from webapp2_extras import sessions

from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError

template_dir = os.path.join(os.path.dirname(__file__),'../templates')
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

# Decorador para verificar si hay un usuario en la sesion
def user_required(handler):
  def check_login(self, *args, **kwargs):
    auth = self.auth
    if not auth.get_user_by_session():
      self.redirect(self.uri_for('login'), abort=True)
    else:
      return handler(self, *args, **kwargs)

  return check_login

# Los demas handlers heredaran este handler, 
# contiene informacion sobre el usuario que puede consumir el template
class BaseHandler(webapp2.RequestHandler):
  @webapp2.cached_property
  def auth(self):
    return auth.get_auth()

  @webapp2.cached_property
  def user_info(self):
    return self.auth.get_user_by_session()

  @webapp2.cached_property
  def user(self):
    u = self.user_info
    return self.user_model.get_by_id(u['user_id']) if u else None

  @webapp2.cached_property
  def user_model(self):
    return self.auth.store.user_model

  @webapp2.cached_property
  def session(self):
      return self.session_store.get_session(backend="datastore")


  # Este render template incluye la informacion del usuario en el dic params
  def render_template(self, view_filename, params=None): 
    if not params:
      params = {}
    user = self.user_info
    params['user'] = user
    template = JINJA_ENVIRONMENT.get_template(view_filename)
    self.response.out.write(template.render(params))

  # Funcion que permite mostrar un peque#o mensaje en una pagina nueva
  def display_message(self, message):
    params = {
      'message': message
    }
    self.render_template('/carlos/message.html', params)

  # Lo necesita webapp2 para funcionar y para poder soltar los recursos
  def dispatch(self):
      self.session_store = sessions.get_store(request=self.request)

      try:
          webapp2.RequestHandler.dispatch(self)
      finally:
          self.session_store.save_sessions(self.response)



#Auth Model
#https://webapp-improved.appspot.com/api/webapp2_extras/appengine/auth/models.html 


