import webapp2, json, ceniralib.handlers
from google.appengine.api import search


class ApiMainHandler(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'application/json' 
    self.response.out.write(json.dumps({"status": 200, "content":{'msg' : 'ok'}}))


class ApiQueryBooksHandler(webapp2.RequestHandler):
  def get(self, q):
      sort = search.SortOptions(expressions=[
        search.SortExpression(expression='name',
          direction=search.SortExpression.ASCENDING, default_value='')
        ], limit=1000)

      options = search.QueryOptions(limit=10, sort_options=sort, returned_fields=['name', 'id', 'publisher', 'author', 'photo'])

      query_string = ''.join(['pieces:', q])
      query = search.Query(query_string=q, options=options)
      results = search.Index('api-books').search(query)

      out = {'results': [], 'success':True}
      if results:
        for item in results:
          out['results'].append({f.name: f.value for f in item.fields})
      self.response.headers['Content-Type'] = 'application/json' 
      self.response.out.write(json.dumps(out))