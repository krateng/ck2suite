from .config import GLOBALCONFIG
from math import inf


ranges = GLOBALCONFIG["AGE_RANGES"]

aliases = {}

for r in ranges:
	for a in ranges[r]["aliases"]:
		aliases[a] = ranges[r]
sorted_aliases = sorted((a for a in aliases),key=len,reverse=True)



#def interpret_age(inputstring):
#
#	ranges = []
#	while inputstring != "":
#		for a in sorted_aliases:
#			if inputstring.startswith(a):
#				ranges.append(aliases[a])
#				inputstring = inputstring[len(a):]
				
	
def interpret(inp):
	if "-" in inp:
		minage,maxage = inp.split("-")
		try: minage = int(minage)
		except: minage = None
		try: maxage = int(maxage)
		except: maxage = None
		agerange = (minage,maxage)
		portrait_ages = get_closest_match(agerange)["portrait_age_range"]
		return (agerange,portrait_ages)
	else:
		inp = inp.lower()
		for r in ranges:
			if inp in ranges[r]["aliases"]:
				agerange = ranges[r]["range"]
				portrait_ages = ranges[r]["portrait_age_range"]
				return (agerange,portrait_ages)
				
		return (ranges["full"]["range"],ranges["full"]["portrait_age_range"])
			


def get_closest_match(agerange):
	minage,maxage = agerange
	if minage is None: minage = 0
	if maxage is None: maxage = 100
	
	bestmatch,difference = None,inf
	
	for r in ranges:
		minage_,maxage_ = ranges[r]["range"]
		if minage_ is None: minage_ = 0
		if maxage_ is None: maxage_ = 100
	#	if minage_ is None and minage is not None:
	#		continue
	#	if maxage_ is None and maxage is not None:
	#		continue
	#	if minage_ is not None and minage is None:
	#		continue
	#	if maxage_ is not None and maxage is None:
	#		continue
			
	#	diffmin = 0 if minage is None else abs(minage_ - minage)
	#	diffmax = 0 if maxage is None else abs(maxage_ - maxage)
		diffmin = abs(minage_ - minage)
		diffmax = abs(maxage_ - maxage)
		
		totaldiff = diffmin + diffmax
		
		if totaldiff < difference:
			bestmatch, difference = ranges[r], totaldiff
			
	
	return bestmatch
