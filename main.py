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
      'key': 1
    , 'name': 'Some name'
    , 'storage_type': 'file'
    , 'date': '23.05.2013'
    , 'size': '32768'
    }
  ]
"""

def parent_entity():
  return ndb.Key('Uploads', 'uploads')

class Upload(ndb.Model):
  key = ndb.IntegerProperty()
  name = ndb.StringProperty(indexed=False)
  storage_type = ndb.StringProperty(required=True, choices=set(["file", "blob"]))
  date = ndb.DateTimeProperty(auto_now_add=True)
  size = ndb.IntegerProperty()

class MainPage(webapp2.RequestHandler):
  def get(self):
    try:
      self.messages
    except:
      self.messages = []

    uploads_query = Upload.query(ancestor=parent_entity()).order(-Upload.date)
    uploads = uploads_query.fetch(20)

    template_values = {
      'messages': self.messages
    , 'uploads': uploads
    }

    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render(template_values))

  def post(self):
    # name
    # type
    # file

    upload = Upload(parent=parent_entity())
    previous_uploads = Upload.query(ancestor=parent_entity()).order(-Upload.date).fetch(1)

    upload.key = previous_uploads[0].key + 1 if len(previous_uploads) else 1
    upload.name = self.request.get('name')
    upload.storage_type = self.request.get('storage_type')
    upload.size = 32768
    upload.put()

    # if success
    self.messages = [{'type': 'success', 'text': 'You have successfuly uploaded a file'}]

    self.get()

application = webapp2.WSGIApplication([
  ('/', MainPage),
], debug=True)
