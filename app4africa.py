#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import os
import cgi
import wsgiref.handlers
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import mail


#Create the AppEngine Apps 4 Africa data Model for ...
# As it extends the db.Model the content of the class will automatically be stored 

class App4AfricaModel(db.Model):
    names = db.StringProperty()
    email = db.EmailProperty()
    app_name = db.StringProperty()
    description = db.StringProperty(multiline = True)
    created = db.DateTimeProperty(auto_now_add = True)
    address= db.StringProperty(multiline = True )
    size = db.StringProperty()
    
    
    
    
#Mani page 
# MainPage class is a subclass of webapp.RequestHandler and overwrites the get method

class MainPage(webapp.RequestHandler):
    def get(self):
           
        #GQL or Google Query Language is like SQL 
        #BRB to change back to 50 ..
        apps = db.GqlQuery("SELECT * FROM App4AfricaModel ORDER BY date DESC LIMIT 5")
        
        
        template_values = {
            'apps':apps
     
        
        }
        
        self.response.out.write(template.render('index.html',template_values))
        
        
        
        
#This class creates a new item . 
class NewApp(webapp.RequestHandler):
    def post(self):
                
        apps = App4AfricaModel()
        apps.names = self.request.get('names')
        apps.email = self.request.get('email')
        apps.app_name = self.request.get('app_name')
        apps.description = self.request.get('description')
        apps.address= self.request.get('address')
        apps.size = self.request.get('size')
               
            
            
        apps.put()
        self.redirect('/')
            
            

            

def main():
    application = webapp.WSGIApplication([('/', MainPage),
                                          ('/new',NewApp),],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
