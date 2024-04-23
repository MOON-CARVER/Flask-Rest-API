
from functools import wraps
import json
import mysql.connector
from flask import make_response ,request
import jwt 
import re
from config.config import dbconfig
class auth_model():
    def __init__(self):
        # Connection establishment code 
        try:
            self.con = mysql.connector.connect(host=dbconfig['hostname'],user = dbconfig['username'],password =  dbconfig['password '],databse = dbconfig['database'])
            print("connection successful")
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
        except:print("Some error")
        
    def token_auth(self, endpoint = ""):
        def inner1(func):
            @wraps(func)
            def inner2(*args):
                endpoint = request.url_rule
                print(endpoint)
                authorization = request.headers.get("Authorization")
                if re.match("^Bearer *([^ ]+) *$", authorization, flags = 0 ):
                    token = authorization.split(" ")[1]
                    try:
                        jwtdecoded = jwt.decode(token, "chander" , algorithms = "HS256" )
                    except jwt.ExpiredSignatureError:
                        return make_response({"error":"Token Exprired"}, 401)                
                    role_id = jwtdecoded['payload']['role_id']
                    
                 
                    self.cur.execute(f"SELECT roles FROM accessibiilty_view WHERE endpoint ='{endpoint}' ")
                    result = self.cur.fetchall()
                    if len(result) > 0 :
                        allowed_roles = (json.loads(result[0]['roles']))
                        if role_id in allowed_roles: 
                            return func(*args)
                        else: 
                            return make_response({"ERROR":"INVALID_ROLE"}, 400)
                        
                    else: 
                        return make_response({"ERROR":"UNKNOWN ENDPOINT"}, 400)
                        
                    print(token)
                else:
                    return make_response({"error":"INVALID TOKEN"}, 401)
                
            return inner2
        return inner1
     
                