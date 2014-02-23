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
import webapp2
import jinja2
import urllib

from google.appengine.ext import db 

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class Train(db.Model):
    """ Database entry class

    Attributes:
        line: Train line.
        route: Train route.
        number: Run number.
        op_id: Operator ID.
    """
    line = db.StringProperty(required = True)
    route = db.StringProperty(required = True)
    number = db.StringProperty(required = True)
    op_id = db.StringProperty(required = True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class MainHandler(webapp2.RequestHandler):
    """Page handler for page write & template rendering 

    """ 
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class HomePage(MainHandler):
    """Home page

    """ 
    def get(self):
        """ Load data from database """
        entities = Train.all()
        entities.order("number")

        # Render template
        kwargs = {"head": ['Train Line', 'Train route', 'Run number', 'Operator ID'], "entry": entities}
        self.render('index.html', kwargs = kwargs)

    def post(self):
        """ Upload data to database """
        raw_file_name = filename = self.request.POST.multi['file'].filename
        raw_file = self.request.POST.multi['file'].file
        self.load(raw_file)
        self.redirect('/')

    def load(self, filestream):
        """ Load & parse csv data """
        # Load head and each entry
        head = [h.strip() for h in filestream.next().split(",")]
        
        for line in filestream:
            # Load each item
            row = [i.strip() for i in line.split(",")]
            
            # Check dupliaction
            if self.check(row):
                continue

            # Map items to each attribute from Train
            kwargs = dict(zip(['line', 'route','number','op_id'], row))

            train = Train(**kwargs)
            train.put()

    def check(self, data):
        """ Check dupliaction """
        line, route, number, op_id = data
        query = "SELECT * FROM Train WHERE number='%s'" % number
        q = db.GqlQuery(query).get()
        return q

app = webapp2.WSGIApplication([
    ('/', HomePage)
], debug=True)
