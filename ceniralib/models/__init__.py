from google.appengine.ext import ndb
from google.appengine.api import search
from .. import utils

import time
import webapp2_extras.appengine.auth.models

from google.appengine.ext import ndb

from webapp2_extras import security

class Books(ndb.Model):
    """
        Base de datos para libros
    """
    added = ndb.DateTimeProperty(auto_now_add=True)
    title = ndb.StringProperty()
    author = ndb.KeyProperty(repeated=True)
    publisher = ndb.KeyProperty()
    ISBN10 = ndb.StringProperty()
    ISBN13 = ndb.StringProperty()
    paginas = ndb.IntegerProperty()
    publicationDate = ndb.DateProperty()
    NumberInStock = ndb.IntegerProperty()
    edition = ndb.IntegerProperty()
    link_to_photo = ndb.StringProperty()
    description = ndb.TextProperty()

    #After added this is executed
    def _post_put_hook(self, future):
        authors = ''
        for a in self.author:
            authors += a.get().name + ', '  

        doc = search.Document(doc_id=unicode(self.key.id()), fields=[
            search.TextField(name='name', value=self.title),
            search.TextField(name='pieces', value=utils.text_pieces(self.title)),
            search.TextField(name='id', value=unicode(self.key.id())),
            search.TextField(name='publisher', value=self.publisher.get().name),
            search.TextField(name='author', value=authors),
            search.TextField(name='photo', value=self.link_to_photo)])
        search.Index('api-books').put(doc)

    @classmethod
    def _post_delete_hook(cls, key, future):
        search.Index('api-books').delete(key.id())


class Authors(ndb.Model):
    """
        Base de datos para autores o escritores
    """
    name = ndb.StringProperty()
    born = ndb.DateTimeProperty()
    died = ndb.DateTimeProperty()
    description = ndb.TextProperty()

    #After added this is executed
    def _post_put_hook(self, future):
        doc = search.Document(doc_id=unicode(self.key.id()), fields=[
            search.TextField(name='name', value=self.name),
            search.TextField(name='pieces', value=utils.text_pieces(self.name)),
            search.TextField(name='id', value=unicode(self.key.id()))])
        search.Index('api-authors').put(doc)

    @classmethod
    def _post_delete_hook(cls, key, future):
        search.Index('api-authors').delete(key.id())

class Publisher(ndb.Model):
    """
        Empresas publicadoras
    """
    name = ndb.StringProperty()
    web = ndb.StringProperty()
