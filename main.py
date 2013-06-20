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
  messages: an arrary of objects. each object have a type and a text.
  messages = [
    {'type': '', 'text': 'You have an alert'}
  , {'type': 'error', 'text': 'You have an error'}
  , {'type': 'success', 'text': 'You have an success'}
  , {'type': 'info', 'text': 'You have an info'}
  ]

  uploads:
  uploads = [
    {
      'id': 1
    , 'name': 'Some name'
    , 'type': 'file'
    , 'date': '23.05.2013'
    , 'size': '32768'
    }
  ]
"""

class MainPage(webapp2.RequestHandler):
  def get(self):
    messages = []
    uploads = []

    template_values = {
      'messages': messages
    , 'uploads': uploads
    }

    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render(template_values))

  def post(self):
    # name
    # type
    # file

    self.get()

application = webapp2.WSGIApplication([
  ('/', MainPage),
], debug=True)
