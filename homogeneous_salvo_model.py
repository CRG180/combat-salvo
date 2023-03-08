
# Homogeneous Salvo Model
#num_units = number of units in force.
#aimed_offense = the number of well-aimed missiles fired by each unit per salvo.
#num_missiles = the total number missiles available for each unit
#defense_capability = number of well-aimed attacking missiles eliminated by each unit per salvo.
#defense_staying = number of missiles required to place an unit out of action.
#scouting = Scouting effectiveness of force.
#alertness = Defender alertness for force.
#training = Training effectiveness for force.
#distraction = Distraction factor for force.
#force_delta = number of units put out of action from enemys's salvo.



class force:
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
		
		
class engagement:
	def __init__(self, force_a, force_b):
		self.a = force_a
		self.b = force_b
		self.iter = 0
	
	def salvo_engagement(self):
		delta_a = ((self.b.aimed_offense*self.b.num_units) - (self.a.defense_capability * self.a.num_units)) / self.a.defense_staying
		delta_b = ((self.a.aimed_offense*self.a.num_units) - (self.b.defense_capability * self.b.num_units)) / self.b.defense_staying
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
	
	def iter_engagement(self):
		while self.a > 0 and self.b > 0:
			self.salvo_engagement()
			print(self.a.name, self.a.num_units)
			print(self.b.name, self.b.num_units)
		nl = "\n"
		return print(
		f"{nl} Battle complete after {self.iter} iterations. The winner is {self.wining_force()}{nl}. \
		Remaing combat power:{nl} \
		{self.a.name}: {self.a.num_units} {nl} \
		{self.b.name}: {self.b.num_units}" )
	
		
a = force(name="side A",num_units= 6,
		  aimed_offense = 1,
		  num_missiles = 10,
		  defense_capability =1,
		 defense_staying =1)

b = force(name="side B",num_units= 3,
		  aimed_offense = 3,
		  num_missiles = 10,
		  defense_capability =2,
		 defense_staying =2)

		
battle_1 = engagement(a,b)
print(a.num_units, b.num_units)
battle_1.iter_engagement()
