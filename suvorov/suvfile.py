import re	

def suv_eval(content,data):
	
	for scope,operator,expression in content:
		
		scope = sub_vars(scope,data)
		expression = sub_vars(expression,data)
				
		if scope.startswith("@"):
			cmd = scope[1:]
			if cmd == "forin":
				_for = [e[2] for e in expression if e[0] == "@for"][0]
				_in = [e[2] for e in expression if e[0] == "@in"][0]
				_in = sub_vars(_in,data)
				expression = [e for e in expression if e[0] not in ("@for","@in")]
				for entry in get_var(_in,data):
					data.push({_for:entry})
					yield from suv_eval(expression,data)
					data.pop()
		
		else:
			if isinstance(expression,list):
				expression = list(suv_eval(expression,data))
			
			yield scope,operator,expression
	

def get_var(name,data):
	parts = name.split(".")
	result = data
	for p in parts:
		result = result[p]
	return result
def sub_vars(name,data):
	if isinstance(name,str):
		l = re.split(r"\$(.*);?",name)
		for n in range(1,len(l),2):
			l[n] = get_var(l[n],data)
		return "".join(l)
	else:
		return name	
