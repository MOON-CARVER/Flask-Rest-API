
import json
import mysql.connector
from flask import make_response
class user_model():
    def __init__(self):
        # Connection establishment code 
        try:
            self.con = mysql.connector.connect(host="localhost",username = "root", password = "Tsubasa@1105",database = "flask_api")
            print("connection successful")
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
        except:print("Some error")
   
    def user_getall_model(self):
        
        #query execution code 
        self.cur.execute("SELECT * FROM users")
        result = self.cur.fetchall()
        print(result)
        if len(result)>0:
            return make_response({"paload":result}, 200)
        else: 
            return make_response({"message":"NO DATA FOUND"},204) 
        
    def user_addone_model(self,data):
        self.cur.execute(f"INSERT INTO users(name,email,phone,role,password) VALUES('{data['name']}' , '{data['email']}' , '{data['phone']}' , '{data['role']}' , '{data['password']}' )")
        return make_response({"message":"user created successfully"},201)
    
    
    def user_update_model(self, data):
        self.cur.execute(f"UPDATE users SET name = '{data['name']}' , email = '{data['email']}' , phone = '{data['phone']}' , role = '{data['role']}' , password = '{data['password']} ' WHERE id = '{data['id']}' ")
        if self.cur.rowcount>0:
            return make_response({"message":"user updated successfully"},200)
        else:
            return make_response({"message":"nothing to update"},202)
        
        
    def user_delete_model(self,id):
        self.cur.execute(f"DELETE FROM users WHERE id = {id} ")
        if self.cur.rowcount>0: 
            return make_response({"message":"user Deleted successfully"},200)
        else:
            return make_response({"message":"nothing to delete"},204)