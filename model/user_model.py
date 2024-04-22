
import json
import mysql.connector
from flask import make_response
from datetime import datetime, timedelta 
import jwt 
class user_model():
    def __init__(self):
        # Connection establishment code 
        try:
            self.con = mysql.connector.connect(host="localhost",username = "root", password = "",database = "flask")
            print("connection successful")
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
        except:print("Some error")
   
    def user_getall_model(self):
        
        #query execution code 
        self.cur.execute("SELECT * FROM users")
        result = self.cur.fetchall()
       
        if len(result)>0: 
            res = make_response({"paload":result}, 200)
            res.headers['Access-Control-Allow-Origin'] = "*"
            return res
        
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
        
        
        
        
    def user_patch_model(self,data,id):
        qry = "UPDATE users SET "
        for key in data:
            qry = qry + f"{key} = '{data[key]}',"
        qry = qry[:-1] + f" WHERE id = {id} "
        
        self.cur.execute(qry)
        if self.cur.rowcount>0:
            return make_response({"message":"user updated successfully"},200)
        else:
            return make_response({"message":"nothing to update"},202)        
        return qry
    
    
    def user_pagination_model(self,limit,page):
        limit = int(limit)
        page = int(page)
        start = (page*limit) - limit 
        qry = f"SELECT * FROM users LIMIT {start} , {limit}"
        
         #query execution code 
        self.cur.execute(qry)
        result = self.cur.fetchall()
        print(result)
        if len(result)>0: 
            res = make_response({"payload":result}, 200)
          
            return res
        
        else: 
            return make_response({"message":"NO DATA FOUND"},204) 
         
    
    
    def user_upload_avatar_model(self,uid,filepath):
        self.cur.execute(f"UPDATE users SET avatar = '{filepath}' WHERE id = '{uid}' ")
        if self.cur.rowcount>0:
            return make_response({"message":"avatar uploaded successfully "},200)
        else:
            return make_response({"message":"nothing to update"},202) 
        
    
    
    def user_login_model(self,data):
        self.cur.execute(f"SELECT id, name , email, avatar , role_id FROM users WHERE email = '{data['email']}' and password = '{data['password']}' ")
        result = self.cur.fetchall()
        userdata = str(result[0])
        exp_time = datetime.now() + timedelta(minutes= 15)
        exp_epoch_time = int(exp_time.timestamp())
        payload = {
            "payload" : userdata ,
            "exp" : exp_epoch_time 
            
        }
        jwtoken = jwt.encode(payload, "chander" , algorithm = "HS256") 
        
        return  make_response({"token":jwtoken},200)
    
        