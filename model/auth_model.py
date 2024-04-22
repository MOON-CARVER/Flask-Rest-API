
import json
import mysql.connector
from flask import make_response ,request
import jwt 
import re
class auth_model():
    def __init__(self):
        # Connection establishment code 
        try:
            self.con = mysql.connector.connect(host="localhost",username = "root", password = "",database = "flask")
            print("connection successful")
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
        except:print("Some error")
        
    def token_auth(self, endpoint):
        def inner1(func):
            def inner2(*args):
                authorization = request.headers.get("Authorization")
                if re.match("^Bearer *([^ ]+) *$", authorization, flags = 0 ):
                    token = authorization.split(" ")[1]
                    try:
                        jwt_decoded = jwt.decode(token, "chander" , algorithms = "HS256" )
                    except jwt.ExpiredSignatureError:
                        make_response({"error":"Token Exprired"}, 401)
                    role_id = jwt_decoded['payload']['role_id']
                    self.cur.execute(f"SELECT roles FROM accessibility_view WHERE endpoint ='{endpoint}' ")
                    result = self.cur.fetchall()
                    if len(result) > 0 :
                        allowed_roles = (json.loads(result[0]['roles']))
                        return func(*args)
                    else: 
                        return make_response({"ERROR":"UNKNOWN ENDPOINT"}, 400)
                        
                    print(token)
                else:
                    return make_response({"error":"INVALID TOKEN"}, 401)
                return func(*args)
            return inner2
        return inner1
     
                