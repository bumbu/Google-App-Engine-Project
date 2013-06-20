#!/usr/bin/env python

import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  extensions=['jinja2.ext.autoescape'])

"""
  erros: an arrary of objects. each object have a type and a message.
  errors = [
    {'type': '', 'message': 'You have an alert'}
  , {'type': 'error', 'message': 'You have an error'}
  , {'type': 'success', 'message': 'You have an success'}
  , {'type': 'info', 'message': 'You have an info'}
  ]
"""

class MainPage(webapp2.RequestHandler):
  def get(self):
    errors = []

    template_values = {
      'errors': errors
    }

    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
  ('/', MainPage),
], debug=True)
