import webapp2
from ceniralib.handlers import www, api
from webapp2_extras import auth
from webapp2_extras import sessions

config = {
  'webapp2_extras.auth': {
    'user_model': 'UserModel.User',
    'user_attributes': ['name']
  },
  'webapp2_extras.sessions': {
    'secret_key': 'YOUR_SECRET_KEY'
  }
}

app = webapp2.WSGIApplication([    
    # MAIN
    webapp2.Route(r'/cenira', handler=www.MainHandler, name='Main'),
    webapp2.Route(r'/cenira/libro/<ide>', handler=www.SingleBook, name='SingleBook'),
    webapp2.Route(r'/cenira/libros/ultimos', handler=www.UltimosLibrosHandler, name='UL'),
    webapp2.Route(r'/cenira/nosotros/equipo', handler=www.EquipoHandler, name='PE'),
    webapp2.Route(r'/cenira/libros/agregar', handler=www.AgregarLibroHandler, name='agregar'),
    webapp2.Route(r'/cenira/libros/buscar', handler=www.SearchHandler, name='buscar'),
    webapp2.Route(r'/cenira/autores/agregar', handler=www.AgregarAutorHandler, name='agregarautor'),
    webapp2.Route(r'/cenira/editoriales/agregar', handler=www.AgregarEditorialHandler, name='agregareditorial'),

    # USUARIOS
    webapp2.Route(r'/cenira/registrarse', handler=www.RegistrarseHandler, name='registrarse'),
    webapp2.Route(r'/cenira/login', handler=www.LoginHandler, name='login'),
    webapp2.Route(r'/cenira/logout', handler=www.LogoutHandler, name='logout'),
    
    # API
    (r'^/cenira/api/v1/$',api.ApiMainHandler),
    webapp2.Route('/cenira/api/v1/books/q/<q>', api.ApiQueryBooksHandler),
], config=config, debug=True)

def main():
    run_wsgi_app(app)                                    

if __name__ == '__main__':
    main()
