import sql3Module
import json
import KB
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
		self.id   		= id
		self.name 		= name
		self.priority 	= prior
		### This Fiels use only for user answer its not save in db
		self.answer 	= 0

	def pprint(self):
		print("id:" , self.id , "Question name:", self.name, "priority :", self.priority )



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
	def getPersonById(self ,id ):
		for p in self.persons:
			if p.id == id:
				return p
		return None

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

		kb = KB.KB(copyperson, [])
		isAskerWork = True
		usedQ = []
		while isAskerWork:
			fact = activeQuestions[0]

			#Take Answer from User
			answer = int(input(" Question : " + fact.name + " 0 No 1 I think Not 2 Dont Know 3 May be  4 Yes"))
			
			#update fact about animal
			fact.answer = answer * 0.25
			#add to KB
			kb.addAnswer(fact)
			
			# update first active Question
			usedQ.append(fact)
			activeQuestions.pop(0)
			if  not activeQuestions:
				isAskerWork = False

		persons = kb.calculateDamage()
		wonPerson = persons[0]
		for p in persons:
			p.pprint()
		wonPerson.pprint()
		answer = int(input(" Is It Correct Animal? 0 NO 1 Yes "))
		if (answer == 0):
			answer2 = int(input(" Does Have Animal on Animal List ? 0 NO 1 Yes "))
			if (answer2 == 1):
				idAnimal = int (input ("Input ID Animal"))
				wonPerson = self.getPersonById(idAnimal)
				if not wonPerson:
					print(" Animal Not Found ")
					return
			else:
				name = input (" Input Name New Animal")
				qres = {}
				for q in usedQ:
					qres[q.id] = [ q.answer, 1]
				p1 = Person(name, qres,  0, len(self.persons))
				self.persons.append(p1)
				self.db.addUserPush(p1)
				self.db.push()
				print("Finish Play")
				return 

		for a in usedQ:
			if a.id in wonPerson.data.keys():
				cnt = wonPerson.data[a.id][1]
				val = wonPerson.data[a.id][0]
				newVal = a.answer 
				upval = (val * cnt + newVal) / (cnt + 1)
				wonPerson.data[a.id] = [ upval, cnt + 1 ]
			else:
				wonPerson.data[a.id] = [ a.answer, 1]
		wonPerson.pprint()

		self.updateP(wonPerson)
		self.db.updatePerson(wonPerson)



	def checkAnswerWithUPerson(self,  p , q, answer ):
		print( "Q ID", q.id, p.data.keys(), type(p.data.keys()), q.id in p.data.keys() )
		if q.id in p.data.keys():
			value = p.data[q.id][0]
			p.damage += abs(value - answer * 0.25)
		else:
			p.damage += abs(0.5 - answer * 0.25)

print("init Session")

session = Session()
session.startAsker()