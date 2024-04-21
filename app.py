from flask import Flask 
app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)
    
    
@app.route("/")
def welcome():
    return 'helllo world'

    
@app.route("/home")
def home():
    return 'welcome to home '

from controller import *