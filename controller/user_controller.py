from flask import request
from app import app 
from model.user_model import user_model

obj= user_model()

@app.route("/user/getall")
def user_getall_controller():
    return obj.user_getall_model() 

@app.route("/user/addone",methods = ["POST"])
def user_addone_controller():
    
    return obj.user_addone_model(request.form) 


@app.route("/user/update",methods = ["PUT"])
def user_update_controller():
    return obj.user_update_model(request.form)


@app.route("/user/delete/<id>",methods = ["DELETE"])
def user_delete_controller(id):
    return obj.user_delete_model(id)