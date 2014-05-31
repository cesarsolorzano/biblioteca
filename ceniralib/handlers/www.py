import webapp2
import datetime, time
from .. import handlers
import UserHandlers
from UserHandlers import BaseHandler

import logging
import os.path
import webapp2, jinja2
from .. import models
import re

from webapp2_extras import auth
from webapp2_extras import sessions

from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError

class MainHandler(UserHandlers.BaseHandler):
    def get(self):
        libros = models.Books.query().fetch_page(6)
        BaseHandler.render_template(self, "/stivali/index.html", params={'libros' :libros})

class SearchHandler(UserHandlers.BaseHandler):
    def get(self):
        BaseHandler.render_template(self, "/stivali/search.html")

class UltimosLibrosHandler(UserHandlers.BaseHandler):
    def get(self):
        libros = models.Books.query().order(-models.Books.added).fetch_page(100)
        BaseHandler.render_template(self, "/george/UL.html", params={"libros" :libros})

class EquipoHandler(UserHandlers.BaseHandler):
    def get(self):
        BaseHandler.render_template(self, "/george/PE.html")
        

class AgregarLibroHandler(UserHandlers.BaseHandler):
    @UserHandlers.user_required
    def get(self):
        authors = models.Authors.query().fetch_page(100)
        publishers = models.Publisher.query().fetch_page(100)
        BaseHandler.render_template(self, "/cesar/add.html", params= {"autores":authors, 'publishers': publishers})
    
    def post(self):
        ISBN10 = None
        ISBN13 = None
        paginas = None
        date = None
        stock = None
        edition = None
        title = self.request.get("title")
        description = self.request.get("description")
        if self.request.get("ISBN10"):
            ISBN10 = self.request.get("ISBN10")
        if self.request.get("ISBN13"):
            ISBN13 = self.request.get("ISBN13")
        if self.request.get("paginas"):
            paginas = int(self.request.get("paginas"))
        if self.request.get("date"):
            date = self.request.get("date").split('-')
            date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
        if self.request.get("stock"):
            stock = int(self.request.get("stock"))
        if self.request.get("edition"):
            edition = int(self.request.get("edition"))
        photo = self.request.get("photo")
        author = self.request.get("author")
        publisher = self.request.get("publisher")
        z = models.Books(title = title, 
            author = models.Authors.get_by_id(int(author)).key, 
            publisher =  models.Publisher.get_by_id(int(publisher)).key,
            ISBN10 = ISBN10,
            ISBN13 = ISBN13,
            paginas = paginas,
            publicationDate = date,
            NumberInStock = stock,
            edition = int(edition),
            link_to_photo = photo,
            description = description)
        z.put()
        time.sleep(1)
        self.redirect('/cenira')


class AgregarAutorHandler(UserHandlers.BaseHandler):
    @UserHandlers.user_required
    def get(self):
        BaseHandler.render_template(self, "/cesar/addauthor.html")
    
    def post(self):
        name = self.request.get("name")
        if self.request.get("born"):
            born = self.request.get("born").split('-')
            born = datetime.date(int(born[0]), int(born[1]), int(born[2]))
        else:
            born = None
        if self.request.get("died"):
            died = self.request.get("died").split('-')
            died = datetime.date(int(died[0]), int(died[1]), int(died[2]))
        else:
            died = None
        description = self.request.get("description")
        au = models.Authors(name =name, 
            born =  born,
            died = died,
            description = description)
        au.put()
        time.sleep(1)
        self.redirect('/cenira')

class AgregarEditorialHandler(UserHandlers.BaseHandler):
    @UserHandlers.user_required
    def get(self):
        BaseHandler.render_template(self, "/cesar/addeditorial.html")
    
    def post(self):
        name = self.request.get("name")
        if self.request.get("web"):
            web = self.request.get("web")
        else:
            web = None
        description = self.request.get("description")
        publi = models.Publisher( name =name, web =  web)
        publi.put()
        time.sleep(1)
        self.redirect('/cenira')


class SingleBook(UserHandlers.BaseHandler):
    def get(self, ide):
        libro = models.Books.get_by_id(int(ide))
        BaseHandler.render_template(self, "/cesar/singlebook.html", {"libro" :libro})



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
      email_address=email,
      name=name,
      password_raw=password,
      last_name=last_name,
      verified=True,
      role = 0)
    if not user_data[0]: #user_data es de tipo tuple
      BaseHandler.render_template(self, "/carlos/registrarse.html", params={ 'error': 'No fue posible crear el usuario, usuario o email ya existen'})
      return

    self.display_message('Te registraste correctamente.')


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
