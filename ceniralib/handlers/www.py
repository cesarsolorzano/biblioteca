import webapp2
from .. import models
import datetime, time
from .. import handlers

class MainHandler(webapp2.RequestHandler):
    def get(self):
        libros = models.Books.query().fetch_page(6)
        handlers.render_template(self, "/stivali/index.html", params= {"libros" :libros})

class SearchHandler(webapp2.RequestHandler):
    def get(self):
        handlers.render_template(self, "/stivali/search.html")

class UltimosLibrosHandler(webapp2.RequestHandler):
    def get(self):
        libros = models.Books.query().order(-models.Books.added).fetch_page(100)
        handlers.render_template(self, "/george/UL.html", params= {"libros" :libros})

class EquipoHandler(webapp2.RequestHandler):
    def get(self):
        handlers.render_template(self, "/george/PE.html")
        

class AgregarLibroHandler(webapp2.RequestHandler):
    def get(self):
        authors = models.Authors.query().fetch_page(100)
        publishers = models.Publisher.query().fetch_page(100)
        handlers.render_template(self, "/cesar/add.html", params= {"autores":authors, 'publishers': publishers})
    
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


class AgregarAutorHandler(webapp2.RequestHandler):
    def get(self):
        handlers.render_template(self, "/cesar/addauthor.html")
    
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

class AgregarEditorialHandler(webapp2.RequestHandler):
    def get(self):
        handlers.render_template(self, "/cesar/addeditorial.html")
    
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


class SingleBook(webapp2.RequestHandler):
    def get(self, ide):
        libro = models.Books.get_by_id(int(ide))
        handlers.render_template(self, "/cesar/singlebook.html", params= {"libro" :libro})


class TestHandler(webapp2.RequestHandler):
    def get(self):
      x = models.Publisher(name = "O'Reilly Media",web = "http://oreilly.com/")
      x.put()
      y = models.Authors(name = "Mark Lutz", description= "Mark Lutz is the world leader in Python training, the author of Python's earliest and best-selling texts, and a pioneering figure in the Python community since 1992. He has been a software developer for 25 years, and is the author of O'Reilly's Programming Python, 3rd Edition and Python Pocket Reference, 3rd Edition.")
      y.put()
      z = models.Books(title = "Programming Python", 
        author = y.key, 
        publisher = x.key,
        ISBN10 = 1449355730,
        paginas = 1600,
        publicationDate = datetime.date(2013, 6, 6),
        NumberInStock = 1,
        edition = 4,
        link_to_photo = "http://akamaicovers.oreilly.com/images/9780596158118/cat.gif")
      z.put()


      
class ManualAgregadorHandler(webapp2.RequestHandler):
    def get(self):
        
        publishers = [{'name': "O'Reilly Media", 'web': "http://oreilly.com"},
        {'name': "Houghton Mifflin", 'web':"http://www.hmhco.com"},
        {'name': "McGraw-Hill Interamericana de Espana", 'web': "htpp//www.mcgraw-hill.es/"},
        {'name': "McGraw-Hill", 'web': "http://www.mcgrawhill.ca"},]

        Authors = [{'name': "Mark Lutz", 'description': "Mark Lutz is the world leader in Python training, the author of Python's earliest and best-selling texts, and a pioneering figure in the Python community since 1992. He has been a software developer for 25 years, and is the author of O'Reilly's Programming Python, 3rd Edition and Python Pocket Reference, 3rd Edition."},
        {'name': "Bernard Grob", 'description':""},
        {'name': "John Doe", 'description':""},
        {'name': "Jane Roe", 'description':""},
        {'name': "Charles Severance ", 'description' :"Charles Severance is a Clinical Assistant Professor in the School of Information at the University of Michigan; he has also taught Computer Science at Michigan State University"},
        {'name': "Dan Sanderson", 'description':"Dan Sanderson is a technical writer and software engineer at Google Inc. He has worked in the web industry for over 10 years as a software engineer and technical writer for Google, Amazon.com, and the Walt Disney Internet Group."},]

