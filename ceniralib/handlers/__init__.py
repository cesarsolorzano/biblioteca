import webapp2, jinja2, os

template_dir = os.path.join(os.path.dirname(__file__),'../templates')
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


def render_template(self, template_filename, params={}):
    template = JINJA_ENVIRONMENT.get_template(template_filename)
    self.response.out.write(template.render(params))
