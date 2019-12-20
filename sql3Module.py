import sqlite3 
import json
#cursor.execute("""CREATE TABLE Person
#        (name text, data text, cnt integer)""")

class DBConnector:
    def __init__(self):
        self.questionsPush = []
       	self.usersPush 	   = []
       	self.users 		   = []
       	self.questions 	   = []
       	self.conn 		   = sqlite3.connect("akinanor.db")
       	self.cursor		   = self.conn.cursor()

    def addUserPush(self, user):
    	self.usersPush.append(user)

    def addQuestionPush(self, q):
    	self.questionsPush.append(q)
    	print( "q print", q.pprint() )

    def takeData(self):
    	print("Load Data from DB")
    	users = "SELECT * FROM PERSON"
    	self.cursor.execute(users, [])
    	print(self.cursor.fetchall())

    def push(self):
    	if len(self.questionsPush) > 0:
    		print("Try Push Questions")
    		qprep = []
    		for q in self.questionsPush:
    			qprep.append( (q.name, q.priority) )

	    	self.cursor.executemany("INSERT INTO QUESTIONS VALUES(?,?)", qprep)
    		print("Questions Succes ")
        	self.questionsPush = []

    	print("Try Push Persons")
    	pprep = []
    	if len(self.usersPush) > 0:
    		for u in self.usersPush:
    			pprep.append( (u.name, json.dumps(u.data), u.cnt) )	
    		self.cursor.executemany("INSERT INTO PERSON VALUES(?,?,?)", pprep)
    	self.conn.commit()
		#	pprep.append( (user.name, user.data, user.cnt) )
		#self.cursor.executemany("INSERT INTO PERSON VALUES(?,?,?)", pprep)
		#self.usersPush = []
		#self.conn.commit()
		



