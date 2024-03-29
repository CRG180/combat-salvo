# Homogeneous Salvo Model

class Force:

	"""A class to represent a either the blue or red force in a homogeneous salvo model

	...
	
	Attributes
    ----------
	name: str
		unit's name
	num_units: int
		number of units in force.
	aimed_offense int:
		the number of well-aimed missiles fired by each unit per salvo.
	num_missiles int:
		 the total number missiles available for each unit
	defense_capability int:
		 number of well-aimed attacking missiles eliminated by each unit per salvo.
	defense_staying int:
		 number of missiles required to place an unit out of action.
	scouting num:
		 scouting effectiveness of force [0,1].
	alertness num:
		 defender alertness for force [0,1].
	training num:
		training effectiveness for force [0,1].
	distraction num:
		distraction factor for force [0,1].
	
	Methods
     -------
	__gt__(self, other):
		greater than operator for the number of units between two force class objects

	__lt__(self, other):
		less than operator for the number of units between two force class objects
	
	__eq__(self, other):
		equals operator for the number of units between two force class objects
	"""
	def __init__(self,name, num_units, aimed_offense,
				num_missiles, defense_capability, 
				defense_staying, scouting =1, alertness =1,
				training = 1, distraction = 1):
		self.name = name
		self.num_units = num_units
		self.aimed_offense = aimed_offense
		self.num_missiles = num_missiles
		self.defense_capability = defense_capability
		self.defense_staying = defense_staying
		self.scouting = scouting
		self.training = training
		self.distraction = distraction
		
	@property
	def offense_shots_available(self):
		return self.num_units * self.num_missiles
	
	def __gt__(self, other):
		if(self.num_units > other):
			return True
		else:
			return False
			
	def __lt__(self, other):
		if(self.num_units < other):
			return True
		else:
			return False

	def __eq__(self, other):
		if(self.num_units == other):
			return True
		else:
			return False

	def __repr__(self):
		return f"{self.name} -- {self.num_units}"

		
class Engagement:
	def __init__(self, force_a, force_b):
		self.a = force_a
		self.b = force_b
		self.iter = 0
	
	def get_salvos_fired(self):
		return self.iter
	
	def salvo_engagement(self):
		'''simultaneous enagagement both A and B fire at the same time'''
		# B fires at A, damage to A is calculated
		delta_a = ((self.b.aimed_offense*self.b.num_units) - (self.a.defense_capability * self.a.num_units)) \
				/ self.a.defense_staying
		# A fires at B, damage to B is calculated
		delta_b = ((self.a.aimed_offense*self.a.num_units) - (self.b.defense_capability * self.b.num_units)) \
				/ self.b.defense_staying
		self.a.num_units -= max(delta_a,0)
		self.b.num_units -= max(delta_b,0)
		self.iter += 1
	
	def wining_force(self):
		if self.a > self.b:
			return self.a.name
		if self.a < self.b:
			return self.b.name
		else:
			return "Stalemate"
	
	def iter_engagement(self, print_results = False):
		while self.a > 0 and self.b > 0:
			self.salvo_engagement()
		if print_results:
			nl = "\n"
			return print(
			f"{nl} Battle complete after {self.iter} iterations. The winner is {self.wining_force()}{nl}. \
			Remaing combat power:{nl} \
			{self.a.name}: {self.a.num_units} {nl} \
			{self.b.name}: {self.b.num_units}" )

	
if __name__ == "__main__":
	a = Force(name="side A",num_units= 6,
			aimed_offense = 1,
			num_missiles = 10,
			defense_capability =1,
			defense_staying =1)

	b = Force(name="side B",num_units= 3,
			aimed_offense = 3,
			num_missiles = 10,
			defense_capability =2,
			defense_staying =2)

	battle_1 = Engagement(a,b)
	print(a.num_units, b.num_units)
	battle_1.iter_engagement()
