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

    def check(self):
        """ Check dupliaction """
        query = "SELECT * FROM Train WHERE number='%s'" % self.number
        q = db.GqlQuery(query).get()
        return q


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
        form_create = self.request.get('create')
        if form_create:
            self.redirect('/form?type=%s' % form_create)
            return
            
        raw_file_name = self.request.POST.multi['file'].filename
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
            
            # Map items to each attribute from Train
            kwargs = dict(zip(['line', 'route','number','op_id'], row))
            train = Train(**kwargs)

            # Check dupliaction
            if train.check():
                continue

            train.put()


class FormPage(MainHandler):
    """ FormPage
    """
    def get(self):
        """ Load form update/edit page 
        """
        form_type = self.request.get('type')
        self.render("form.html", head = form_type)

    def post(self):
        """ Create or update data
        """
        form_type = self.request.get('type')

        line = self.request.get('line')
        route = self.request.get('route')
        number = self.request.get('number')
        op_id = self.request.get('op_id') 
        
        train = Train(line = line, route = route, number = number, op_id = op_id)

        # Create new data
        if form_type == "Create":
            if not train.check():
                train.put()

        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/form', FormPage)
], debug=True)
