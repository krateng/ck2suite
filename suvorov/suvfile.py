import re
import random

def suv_eval(content,data,loc_keys=None,parent=None):

	if loc_keys is None: loc_keys = {}
	

	
	# normal expressions
	try:	
		for scope,operator,expression in content:
			
			scope = sub_vars(scope,data)
			expression = sub_vars(expression,data)
			
			
			# localisation
			if operator == "=" and not isinstance(expression,list) and expression.startswith("@loc:"):
				key = "suvorovloc" + str(random.randint(1000000000,9999999999))
				while key in loc_keys:
					key = "suvorovloc" + str(random.randint(1000000000,9999999999))
				loc_keys[key] = expression[5:]
				expression = key
			
					
					
			# data logic
			if scope.startswith("@"):
				cmd = scope[1:]
				if cmd == "forin":
					_for = [e[2] for e in expression if e[0] == "@for"][0]
					_in = [e[2] for e in expression if e[0] == "@in"][0]
					_in = sub_vars(_in,data)
					expression = [e for e in expression if e[0] not in ("@for","@in")]
					for entry in get_var(_in,data):
						data.push({_for:entry})
						#print(data)
						yield from suv_eval(expression,data,loc_keys=loc_keys)
						data.pop()
				elif cmd.startswith("loc:"):
					# different than above! direct localisation of a given key
					key = cmd[4:]
					loc_keys[key] = expression
				elif cmd.startswith("loc"):
					# localisation of this scope directly by name
					key = parent + cmd[3:]
					loc_keys[key] = expression
					
			else:
				if isinstance(expression,list):
					expression = list(suv_eval(expression,data,loc_keys=loc_keys,parent=scope))
				
				yield scope,operator,expression
	
	# lists
	except:
		for element in content:
			yield element
			
	#print(loc_keys)
	

def get_var(name,data):
	parts = name.split(".")
	result = data
	for p in parts:
		result = result.get(p) or []
	return result
def sub_vars(name,data):
	if isinstance(name,str):
		l = re.split(r"\$\$([\.A-Za-z]*);?",name)
		#print(name,"found",l)
		for n in range(1,len(l),2):
			l[n] = get_var(l[n],data)
		return "".join(str(e) for e in l)
	else:
		return name	
