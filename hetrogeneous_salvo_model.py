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
		return f"{self.name} -- {self.num_units} "


class Group:
    def __init__(self):
        self.container = []

    def add_unit(self, *args):
        units = [i for i in args]
        return self.container.extend(units)
    
    

if __name__ == "__main__":
    a = Force(name="MRC1",num_units= 6,
                aimed_offense = 1,
                num_missiles = 10,
                defense_capability =1,
                defense_staying =1)

    b = Force(name="MRC2",num_units= 3,
                aimed_offense = 3,
                num_missiles = 10,
                defense_capability =2,
                defense_staying =2)
    c = Force(name="EN1",num_units= 6,
                aimed_offense = 1,
                num_missiles = 10,
                defense_capability =1,
                defense_staying =1)

    d = Force(name="EN2",num_units= 3,
                aimed_offense = 3,
                num_missiles = 10,
                defense_capability =2,
                defense_staying =2)

    groupA = Group()
    groupB = Group()
    groupA.add_unit(a,b)
    groupB.add_unit(c,d)
    print(groupA.container)
    print(groupB.container)