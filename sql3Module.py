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

    def addOnePerson(self, person):
    	pass

    def addOneQuestion(self, question):
    	pass

    def updatePerson(self, person):
    	self.cursor.execute("UPDATE PERSON  SET DATA=? WHERE ID=?", (json.dumps(person.data), person.id))
    	self.conn.commit()
    	print( " UPDATE  PERSON ", person.name, person.data )

    def takeData(self):
    	print("Load Data from DB")
    	users = "SELECT * FROM PERSON"
    	self.cursor.execute(users, [])
    	self.users = []
    	pdata = self.cursor.fetchall()
    	for i in pdata:
    		name = str(i[0])
    		data = json.loads(i[1])
    		data = dict(data)
    		cnt  = int(i[2])
    		pid  = int(i[3])
    		person = { 'name' : name, 'data' : data, 'cnt' : cnt, 'pid' : pid  } 
    		self.users.append( person )
    		
    	questions = "SELECT * FROM QUESTIONS"
    	self.cursor.execute(questions, [])
    	qdata = self.cursor.fetchall()

    	for j in qdata:
    		name 		= str(j[0])
    		priority 	= int(j[1])
    		qid 		= str(j[2])
    		question = {'name' : name, 'priority' : priority, 'qid' : qid}
    		self.questions.append( question )

    def push(self):
    	if len(self.questionsPush) > 0:
    		print("Try Push Questions")
    		qprep = []
    		for q in self.questionsPush:
    			qprep.append( (q.name, q.priority, q.id) )

	    	self.cursor.executemany("INSERT INTO QUESTIONS VALUES(?,?)", qprep)
    		print("Questions Succes ")
    		self.questionsPush = []

    	print("Try Push Persons")
    	if len(self.usersPush) > 0:
    		for u in self.usersPush:
    			self.cursor.execute("INSERT INTO PERSON  VALUES( ? , ? , ?, ?) ", (u.name, json.dumps(u.data), u.cnt, None))

    			#pprep.append( (u.name, json.dumps(u.data), u.cnt) )	
    		#self.cursor.execute("INSERT INTO PERSON VALUES(?,?,?)", pprep)
    	self.conn.commit()
		#	pprep.append( (user.name, user.data, user.cnt) )
		#self.cursor.executemany("INSERT INTO PERSON VALUES(?,?,?)", pprep)
		#self.usersPush = []
		#self.conn.commit()
		



