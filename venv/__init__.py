from flask import Flask

app = Flask(__name__)   #create app instance,object of class flask

@app.route('/')
def index():
    return '<h1> hello world</h1>'          #setting up a map between funtions and urls,so that flask knows what fnt to call when client requests given url

@app.route('/user/<name>')
def user(name):
    return '<h1>hello {0} </h1>'.format(name)   #flask matches what user types in that space and gives it to the argument

if __name__ =='__main__':            #starting server
    app.run(debug=True)
