import os
from flask import Flask
from flask import request
from flask import g
from flask import render_template
from jinja2 import Template

import json

import db_poly

app = Flask(__name__)

nav_bar = [
('/marketview/', 'marketview', 'Market View'),
('/chart/', 'chart', 'Chart'),
('/about/', 'about', 'about')]

def embedTemplate(mainTemplate,active_page):
    html = ""
    html += render_template('header.html')
    html += render_template('nav.html',navigation_bar=nav_bar,active_page=active_page)
    html += render_template(mainTemplate)
    html += render_template('footer.html')

    return html

@app.route('/marketview/')
def show_marketview():
    html = embedTemplate('marketview.html',"marketview")
    return html

@app.route('/about/')
def show_about():
    html = embedTemplate('about.html',"about")
    return html

@app.route('/')
def code():
    html = ""
    html += render_template('header.html')
    html += render_template('nav.html',navigation_bar=nav_bar,active_page="chart")
    html += render_template("chart.html")
    html += render_template('footer.html')
    return html

@app.route('/stocklist/')
def show_ticker():	
	ticker = db_poly.get_ticker()
	nl = []
	for tk in ticker:
		nl.append({'stock':tk,'roc4':0,'roc26':0})
	return json.dumps(nl)

@app.route('/<stockticker>/closes/')
def get_stock_data_closes(stockticker):
    try:
      closes = db_poly.get_closes(stockticker)
      return json.dumps(closes)
      #html = ""
      #html += render_template('header.html')
      #html += render_template('nav.html',navigation_bar=nav_bar,active_page="chart")
      #html += render_template("table.html")
      #html += render_template('footer.html')
      #return html

    except:
      #todo: log
      return 'error reading %s'%(stockticker)	



if __name__=='__main__':
	app.run(debug=True,port=8080,host='0.0.0.0')