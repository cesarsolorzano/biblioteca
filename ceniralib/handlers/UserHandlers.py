from google.appengine.ext.webapp import template
from google.appengine.ext import ndb

import logging
import os.path
import webapp2, jinja2
import __init__
from .. import models
import re

from webapp2_extras import auth
from webapp2_extras import sessions

from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError

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


""" 
Auth Model

https://webapp-improved.appspot.com/api/webapp2_extras/appengine/auth/models.html 
"""
class RegistrarseHandler(BaseHandler):
  def get(self):
    self.render_template('/carlos/registrarse.html')

  def post(self):
    user_name = self.request.get('username').lower()
    email = self.request.get('email').lower()
    password = self.request.get('password')
    password_validar = self.request.get('password_validar')
    name = self.request.get('name')
    last_name = self.request.get('lastname')

    # Validaciones server-side
    if user_name == "" or email == "" or password == "" or password_validar == "":
      BaseHandler.render_template(self, "/carlos/registrarse.html", params={'error': 'Por favor, llena todos los campos.'})
      return

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
      BaseHandler.render_template(self, "/carlos/registrarse.html", params={'error': 'Por favor, introduce un email valido.'})
      return

    if not password or password != password_validar:
      BaseHandler.render_template(self, "/carlos/registrarse.html", params={ 'error': 'Las contrase#as no coinciden.' })
      return

    # A create_user se le puede pasan los datos que necesitemos guardar del usuario
    # estos datos se guardaran automaticamente en la sesion y sera persistente en la base de datos
    unique_properties = ['email_address']
    user_data = self.user_model.create_user(user_name,
      unique_properties,
      email_address=email, name=name, password_raw=password,
      last_name=last_name, verified=False)
    if not user_data[0]: #user_data es de tipo tuple
      BaseHandler.render_template(self, "/carlos/registrarse.html",
        params={ 'error': 'No fue posible crear el usuario, usuario o email ya existen'})
      return

    self.display_message('Te registraste correctamente.')

"""
class SetPasswordHandler(BaseHandler):

  @user_required
  def post(self):
    password = self.request.get('password')
    old_token = self.request.get('t')

    if not password or password != self.request.get('confirm_password'):
      self.display_message('Las contrasenas no coinciden')
      return

    user = self.user
    user.set_password(password)
    user.put()

    # remove signup token, we don't want users to come back with an old link
    self.user_model.delete_signup_token(user.get_id(), old_token)
    
    self.display_message('Contrasena actualizada')
"""

class LoginHandler(BaseHandler):
  def get(self):
    self._serve_page()

  def post(self):
    username = self.request.get('username')
    password = self.request.get('password')
    try:
      u = self.auth.get_user_by_password(username, password, remember=True,
        save_session=True)
      self.redirect(self.uri_for('Main'))
    except (InvalidAuthIdError, InvalidPasswordError) as e:
      logging.info('Login failed for user %s because of %s', username, type(e))
      self._serve_page(True)

  def _serve_page(self, failed=False):
    username = self.request.get('username')
    params = {
      'username': username,
      'failed': failed,
      'login': True
    }
    self.render_template('/carlos/login.html', params)

class LogoutHandler(BaseHandler):
  def get(self):
    self.auth.unset_session()
    self.redirect(self.uri_for('Main'))

"""
class AuthenticatedHandler(BaseHandler):
  @user_required
  def get(self):
    self.render_template('authenticated.html')
"""

template_dir = os.path.join(os.path.dirname(__file__),'../templates')
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)
