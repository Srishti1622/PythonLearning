# Reference: https://flask.palletsprojects.com/en/3.0.x/quickstart/
# Flask is used to develop end-to-end web applications.It is a web framework which is created with the help of python programming
# Two important components: WSGI ( Web Server Gateway Interface ) and Jinja2 Template Engine

# WSGI

# Web Server (AWS,Azure,Apache,IIS)  <----WSGI---->  Web Application (created with the help of flask)
# The WSGI protocol used to redirect the request and get the response from the web application 

# Jinja2 Template Engine

# It is a Web Template Engine which is used to combine the layout of the page with a data source ( can be SQL DB, CSV sheet, ML model, Mongodb ) which will help to load or create dynamic the web page.

# first we need to install the flask library

from flask import Flask, render_template, request, redirect, url_for

# It creates an instance of the Flask class, which will be your WSGI application
app=Flask(__name__)

# .route() is a decorator which take rules as first parameter in form of string which means as soon as we hit that route it will execute the below fundtion
# second parameter it take is methods, by default if haven't specified then it will be GET
@app.route('/')
def welcome():
    return "Welcome to this Flask course."

@app.route('/index')
def index():
    return "Welcome to index page."

@app.route('/htmlline')
def htmlline():
    return "<h1>directly returning html line of code</h1>"

# render_template() is responsible to redirect to mentioned html page
@app.route('/html')
def htmlIntegrate():
    return render_template('index.html')

# HTTP Verbs - GET, POST
@app.route('/submit',methods=['GET','POST'])
def form():
    if request.method=='POST':
        print("post request triggered")
        # id value given in form field here 'name'
        # it will be by default string
        name=request.form['name']
        return f'Hello {name}!'
    return render_template('form.html')

# HTTP Verbs - PUT, DELETE
# see the implementation example in todo app

# Variable Rule ( restricting the parameter value to be of mentioned datatype)
# @app.route('/success/<int:score>')
@app.route('/success/<score>')
def success(score):
    if type(score)==int:
        return "This value is in int so we have typecasted it " + str(score)
    return "The value by default is string if no datatype specified "+ score

@app.route('/fail/<score>')
def fail(score):
    return "The value by default is string if no datatype specified "+ score

# Jinja2 Template Engine
# {{ }} expressions to print output in html
# {%  %} conditions, for loop
# {#  #} this is for comments
# this is how to pass value in html page 
@app.route('/passvaluetohtml/<int:value>')
def passvaluetohtml(value):
    res=""
    if value<=10:
        res="{{}}"
    else:
        res={'value':value,'res':'{%   %}'}
    return render_template('result.html',results=res)

# Building url dynamically
# url_for() is used to create dynamic urls
# redirect() is used to redirect to mentioned url
@app.route('/dynamicurl/<int:value>')
def dynamicurl(value):
    score=value+10
    if value<=10:
        return redirect(url_for('success',score=score))
    return redirect(url_for('fail',score=score))


# entry point of the any .py file
# .run() will run the flask application. It take two important parameter host as string and debug as boolean
# whenever we make any change in the code to see that change we need to restart the server but if we have used debug=True then it will automatically detect the change in the code and restart the server
if __name__=="__main__":
    app.run(debug=True)