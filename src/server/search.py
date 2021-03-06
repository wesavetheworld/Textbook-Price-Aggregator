#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        search.py
# Purpose:     Contains all Request Handlers relating to generic search 
#              functions
#
# Author:      Andre Wiggins
#
# Created:     04/07/2011
# Copyright:   (c) Jacob Marsh, Andrew Stewart, Andre Wiggins 2011
# License:
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#-------------------------------------------------------------------------------

import parsers
import server
from google.appengine.ext.webapp import template

from google.appengine.ext import webapp

class SearchResultsPage(webapp.RequestHandler):
    '''Handles request for the /search path which returns the HTML for
    a user searching for a textbook by a generic search term'''
    
    def get(self):
        query = self.request.get('q')
        type = self.request.get('type')
        if type and query:
            if type=="isbn":
                newurl = "book/%s"%query
                self.redirect(newurl)
        
            else:
                path = '../static/templates/search.html'                
                retailer = "halfdotcom"
                newurl = "/search/%s?q=%s&type=%s"%(retailer,query,type)
                url2 = "/book"
                template_values={"url":newurl,"url2":url2,"retailer":retailer}
                self.response.out.write(template.render(path, template_values, True))             
            
        else:
            
            self.redirect("/")    
    
class SearchRetailer(webapp.RequestHandler):
    '''Handles request for the /search/retailer which returns the JSON for 
    searching a retailer for a generic search term'''
    
    def get(self):
        retailer_name = self.request.path.rstrip('/').split('/')[-1]
        retailer = parsers.import_parser(retailer_name)
        
        query = self.request.get('q')
        type = self.request.get('type')
        textbooks = server.getjson(retailer.search(query, type))
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(textbooks)
        