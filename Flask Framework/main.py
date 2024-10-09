# Reference: https://flask.palletsprojects.com/en/3.0.x/quickstart/
# Flask is used to develop end-to-end web applications.It is a web framework which is created with the help of python programming
# Two important components: WSGI ( Web Server Gateway Interface ) and Jinja2 Template Engine

# WSGI

# Web Server (AWS,Azure,Apache,IIS)  <----WSGI---->  Web Application (created with the help of flask)
# The WSGI protocol used to redirect the request and get the response from the web application 

# Jinja2 Template Engine

# It is a Web Template Engine which is used to combine the layout of the page with a data source ( can be SQL DB, CSV sheet, ML model, Mongodb ) which will help to load or create dynamic the web page.

# first we need to install the flask library

from flask import Flask, render_template, request

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

@app.route('/form',methods=['GET','POST'])
def form():
    if request.method=='POST':
        print("post request triggered")
        # id value given in form field here 'name'
        name=request.form['name']
        return f'Hello {name}!'
    return render_template('form.html')

# entry point of the any .py file
# .run() will run the flask application. It take two important parameter host as string and debug as boolean
# whenever we make any change in the code to see that change we need to restart the server but if we have used debug=True then it will automatically detect the change in the code and restart the server
if __name__=="__main__":
    app.run(debug=True)