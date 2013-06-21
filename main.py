#!/usr/bin/env python

import os
import urllib
import jinja2
import webapp2
import logging

from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

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
    , 'quality_type': 'file'
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
  quality_type = ndb.StringProperty(required=True, choices=set(["Good", "Bad"]))
  date = ndb.DateTimeProperty(auto_now_add=True)
  size = ndb.IntegerProperty()
  blob = ndb.BlobKeyProperty()

class MainPage(webapp2.RequestHandler):
  def get(self):
    # Create upload url
    upload_url = blobstore.create_upload_url('/upload')

    try:
      self.messages
    except:
      self.messages = []

    uploads_query = Upload.query(ancestor=parent_entity()).order(-Upload.date)
    uploads = uploads_query.fetch(20)

    template_values = {
      'messages': self.messages
    , 'uploads': uploads
    , 'upload_url': upload_url
    }

    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render(template_values))

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def get(self):
    self.redirect('/')

  def post(self):
    # Init response
    mainPage = MainPage()

    # Upload file
    upload_files = self.get_uploads()

    if (len(upload_files)):
      blob_info = upload_files[0]

      # Init Upload object data
      upload = Upload(parent=parent_entity())
      previous_uploads = Upload.query(ancestor=parent_entity()).order(-Upload.date).fetch(1)

      # Populate Upload object with data
      upload.key = previous_uploads[0].key + 1 if len(previous_uploads) else 1
      upload.name = self.request.get('name')
      upload.quality_type = self.request.get('quality_type')
      upload.size = blob_info.size
      upload.blob = blob_info.key()
      upload.put()

      # if success
      mainPage.messages = [{'type': 'success', 'text': 'You have successfuly uploaded a file'}]
    else:
      # file upload error
      mainPage.messages = [{'type': 'error', 'text': 'File wasn\'t uploaded'}]

    mainPage.response = self.response
    mainPage.get()

class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, resource):
    resource = str(urllib.unquote(resource))

    if resource == "None":
      mainPage = MainPage()
      mainPage.response = self.response
      mainPage.messages = [{'type': 'info', 'text': 'This row has no associated file'}]
      mainPage.get()
    else:
      blob_info = blobstore.BlobInfo.get(resource)
      self.send_blob(blob_info)

application = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/upload', UploadHandler),
  ('/download/([^/]+)?', DownloadHandler),
], debug=True)
