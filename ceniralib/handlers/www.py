import webapp2
from .. import models
import datetime, time
from .. import handlers
import UserHandlers
from UserHandlers import BaseHandler

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

