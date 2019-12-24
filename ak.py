import sql3Module
import json
class Person:
	def __init__(self, name, pdata, cnt, pId = 0):
		self.id   = pId
		self.name = name
		self.data = pdata
		self.cnt  = cnt
		self.damage = 0

	def pprint(self):
		print( "name:" , self.name, "data:", self.data, "cnt:", self.cnt, "damage:" , self.damage , " ID:",self.id  )


class Question:
	def __init__(self, name, id, prior = 0):
		self.id   = id
		self.name = name
		self.priority = prior

	def pprint(self):
		print("id:" , self.id , "Question name:", self.name, "priority :", self.priority )


class KB:
	def __init__(self, persons, questions):
		self.activeQ = questions[:]
		self.activeP = persons[:]
		self.lastQuestions = []

	def getActiveQuestion(self):
		if len(self.activeQ) > 0:
			return self.activeQ[0]
		else:
			print("No have Active Questions")
			return None

	def makeAnswerActiveQuestion(self, answer):
		q = self.getActiveQuestion()
		if q:
			self.lastQuestions.append(q)
			self.activeQ.pop(0)
		



class Session:
	def __init__(self):
		self.persons = []
		self.questions = []
		self.db = sql3Module.DBConnector()
		self.db.takeData()
		self.parseDataPersons(self.db.users)
		self.parseDataQuestions(self.db.questions)


	def updateP(self, pNew):
		for p in self.persons:
			if p.id == pNew.id:
				p = pNew

	def parseDataPersons(self, persons):
		for p in persons:
			name = p['name']
			data = p['data']
			cnt  = p['cnt']
			pid  = p['pid']
			self.persons.append( Person(name, data,cnt, pid) )
		self.showP(self.persons)

	def parseDataQuestions(self, questions):
		for q in questions:
			name = q['name']
			prio = q['priority']
			qid  = q['qid'] 
			self.questions.append( Question(name, qid, prio) )
		self.showQ(self.questions)

	def addQ (self):
		qname = input(" Write Question Name")
		q = Question( qname, len(qlist) + 1 )
		self.questions.append(q)

	def showQ(self, staticQuestions):
		for q in staticQuestions:
			q.pprint()

	def showP(self, staticPersons):
		for p in staticPersons:
			p.pprint()

	def addPersons(self, p):
		self.persons = self.persons + p

	def addQuestions(self, q ):
		self.questions = self.questions + q
	
	def startAsker(self): 
		copyperson  = self.persons[:]
		activeQuestions = self.questions[:]
		uQuestions = []
		isFinish = False
		while not(isFinish):
			if not activeQuestions:
				break
			q = activeQuestions[0]
			answer = int(input(" Question : " + q.name + " 0 No 1 I think Not 2 Dont Know 3 May be  4 Yes"))
			uQuestions.append([q, answer])
			activeQuestions.pop(0)
			for p in copyperson:
				self.checkAnswerWithUPerson(p, q, answer)

		pRes = sorted(copyperson, key=lambda person: person.damage)
		self.showP(pRes)

		needNewPet = int(input("is Correct Pet ? 0 No 1 Yes"))
		p = pRes[0]
		if needNewPet == 0:
			name = input("Input Name\n")
			qres = {}
			for q in uQuestions:
				qres[q[0].id] = [ q[1] * 0.25, 1]
			p1 = Person(name, qres,  0, len(self.persons))
			self.persons.append(p1)
			self.db.addUserPush(p1)
			self.db.push()

		else :
			# update person by new data from user
			# q [0] - question 
			# q[1] user Answer
			print("CHECK PERSON DB :", p.name)
			for q in uQuestions:
				if q[0].id in p.data.keys():
					print("OLD QUESTION", q)
					val = p.data[q[0].id][0]
					cnt = p.data[q[0].id][1]
					cnt += 1
					newVal = val - (val - q[1] * 0.25) / cnt
					p.data[q[0].id][0] = newVal
					p.data[q[0].id][1] = cnt
					p.damage = 0
					p.cnt += 1
				else:
					print("NEW QUESTION", q)
					val = q[1] * 0.25
					cnt = 1
					p.data[q[0].id] = [newVal, cnt]

			self.updateP(p)
			self.db.updatePerson(p)

	def checkAnswerWithUPerson(self,  p , q, answer ):
		print( "Q ID", q.id, p.data.keys(), type(p.data.keys()), q.id in p.data.keys() )
		if q.id in p.data.keys():
			value = p.data[q.id][0]
			p.damage += abs(value - answer * 0.25)
		else:
			p.damage += abs(0.5 - answer * 0.25)
'''
questions = []
persons   = []
db = sql3Module.DBConnector()
#db.takeData()
#print(db.users)
#print(db.questions)


p1 = Person("Cat", 		{ 1: [1.0, 1] , 2: [1.0, 1], 3:[1.0, 1], 4: [1.0, 1], 5: [0.0,  1], 6: [0.0, 1], 7: [0.0, 1] },  0, 1)
p2 = Person("Dog", 		{ 1: [1.0, 1] , 2: [1.0, 1], 3:[0.0, 1], 4: [1.0, 1], 5: [0.0,  1], 6: [0.0, 1], 7: [0.75, 1] }, 0, 2)
p3 = Person("Horse", 	{ 1: [1.0, 1] , 2: [1.0, 1], 3:[0.0, 1], 4: [0.0, 1], 5: [1.0,  1], 6: [0.0, 1], 7: [1.0, 1] },  0, 3)
p4 = Person("Parrot", 	{ 1: [0.0, 1] , 2: [1.0, 1], 3:[0.0, 1], 4: [0.0, 1], 5: [0.75, 1], 6: [1.0, 1], 7: [0.0, 1] },  0, 4)

persons.append(p1)
persons.append(p2)
persons.append(p3)
persons.append(p4)


q1 = Question("Does your pet have 4 legs?", 1)
q2 = Question("Does your pet have a tail?", 2)
q3 = Question("Does your pet eat mouses?", 3)
q4 = Question("Does your pet eat meat ", 4)
q5 = Question("Does your pet can't eat meat ", 5)
q6 = Question("Does your pet have a wings ", 6)
q7 = Question("Can u ride on your pet?", 7)
q8 = Question("Does your pet eat carrot?", 8)


questions.append(q1)
questions.append(q2)
questions.append(q3)
questions.append(q4)
questions.append(q5)
questions.append(q6)
questions.append(q7)
questions.append(q8)

for q in questions:
	db.addQuestionPush(q)
for p in persons:
	db.addUserPush(p)
db.push()
'''

print("init Session")

session = Session()
while(True):
	print( "START GAME" )
	session.startAsker()