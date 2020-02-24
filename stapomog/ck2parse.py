import yaml


"""
Each scope is represented by a list. Its entries are 
1) tuples of three (for scope / expression, e.g. diplomacy = 2 or trait = patient or ROOT = {...} ) whereas the third part of the tuple (the expression) can be another list of that sort
2) pure expressions, for lists like on_action = { on_siege = { events = { 13 14 15 } } }


"""

def parse_pdx_file(fn):
	with open(fn,"r") as f:
		tokens = tokenize(f.read())
	nested = nested_tokens(tokens)
	return parse(nested)
	
def parse_yml_file(fn):
	with open(fn,"r") as f:
		d = yaml.safe_load(f.read())
	nested = dict_convert(d)
	return nested
		
def parse(tokens):
	
	l = []
	
	while len(tokens) >= 3:
		l.append((tokens[0],tokens[1],tokens[2] if isinstance(tokens[2],str) else parse(tokens[2])))
		tokens = tokens[3:]
	
	return l
	
def nested_tokens(tokens):
	stack = [[]]
	for token in tokens:
		if token == "{":
			stack.append([])
		elif token == "}":
			t = stack.pop()
			stack[-1].append(t)
		else:
			stack[-1].append(token)
			
		
	assert len(stack) == 1
	return stack[-1]
	
def tokenize(txt):
	buffer = ""
	comment = False
	for char in txt:
		if comment and char in ["\n"]:
			comment = False
		elif comment:
			pass
		elif char in ["#"]:
			comment = True
			
		elif char in [" ","\t","\n"]:
			if buffer != "": yield buffer
			buffer = ""
		elif char in ["{","}"]:
			if buffer != "": yield buffer
			buffer = ""
			yield char
		
		else:
			buffer += char
			
	if buffer != "": yield buffer
		
	
pdx_conversions = {
	True:"yes",
	False:"no"
}	
		

def topdx(parsed,indent=0):
	raw = ""
	

	
	for t in parsed:
		raw += "\t" * indent
		if isinstance(t,tuple):
			raw += t[0] + " " + t[1] + " "
			if any(isinstance(t[2],ty) for ty in [str,int,float,bool]):
				for k in pdx_conversions:
					if t[2] is k:
						# need to do this cause 0 and 1 count as False and True for dict lookup
						raw += pdx_conversions[t[2]]
						break
				else:
					raw += str(t[2])
			else:
				raw +=  "{\n"
				raw += topdx(t[2],indent=indent+1)
				raw += "\t" * indent
				raw += "}"
			raw += "\n"
			
		else:
			raw += t
			raw += "\n"
	
	return raw
	
	
keepaslist = [
	("on_actions",None,"events"),
	("traits",None,"opposites")
]


# takes dict and unpacks list etc according to pdx script rules
def dict_convert(d,keeplists=keepaslist):
	if not isinstance(d,dict): return d
	l = []
	for key,val in d.items():
		keep = [e[1:] for e in keeplists if len(e)>0 and e[0] == key or e[0] is None]
		if isinstance(val,list):
			if (key,) in keeplists:
				l.append((key,"=",val))
			else:
				# unfold list normally
				for entry in val:
					l.append((key,"=",dict_convert(entry,keeplists=keep)))
		else:
			l.append((key,"=",dict_convert(val,keeplists=keep)))
	return l
	
if __name__ == "__main__":
	import sys
	from pprint import pprint
	
	srcfile = sys.argv[1]
	
	if srcfile.endswith(".yml"):
		res = parse_yml_file(sys.argv[1])
	elif srcfile.endswith(".txt"):
		res = parse_pdx_file(sys.argv[1])
		
	pprint(res)	
	print("")
	print("")
	print("---")
	print("")
	print("")
	print(topdx(res))

