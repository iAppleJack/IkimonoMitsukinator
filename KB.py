class KB:
	# Initially is base of persons and answer from user  (FACTS about animal)
	def __init__(self, persons, answers, maxDamage = 10):
		self.activeA 	= answers[:]
		self.activeP 	= persons[:]
		self.maxDamage 	= maxDamage

	# Add new Fact about animal
	def addAnswer(self, answer):
		self.activeA.append(answer)

    # Here Find mistakes for animals and clear animal with big mistake
	def calculateDamage(self):
		for p in self.activeP:
			p.damage = 0
			for q in self.activeA:
				if q.id in p.data:
					result = abs(p.data[q.id][0] - q.answer)
					result = result ** 2;
					p.damage += result
				else:
					result = abs(0.5 - q.answer)
					result = result ** 2;
					p.damage += result

		smallDamage = lambda p : p.damage < self.maxDamage
		resultPersons = list(filter( smallDamage, self.activeP))
		return sorted(resultPersons, key=lambda person: person.damage)
