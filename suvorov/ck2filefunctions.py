import csv
import io
import collections.abc

def parse_ck2(txt):
	tokens = tokenize(inp)
	nested = nested_tokens(tokens)
	return parse(nested)
	
	
def id(x):
	return x
	
	


# PDX FILE
def parse(tokens):
	
	l = []
	
	while len(tokens) >= 3:
		if tokens[1] in ("=","==","<=","=<","<",">",">=","=>"):
			l.append((tokens[0],tokens[1],tokens[2] if isinstance(tokens[2],str) else parse(tokens[2])))
			tokens = tokens[3:]
		else:
			l.append(tokens[0])
			tokens = tokens[1:]
	
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
	string = False
	for char in txt:
		# eol ends comment
		if comment and char in ["\n"]:
			comment = False
		# skip all comment content
		elif comment:
			pass
		# string end
		elif char == string:
			string = False
		# in string, just add all characters
		elif string:
			buffer += char
		# comment begin
		elif char in ["#"]:
			comment = True
		# string begin
		elif char in ["'",'"'] and not string:
			string = char
		# delimiter
		elif char in [" ","\t","\n"]:
			if buffer != "": yield buffer
			buffer = ""
		# delimiter, but also a token
		elif char in ["{","}"]:
			if buffer != "": yield buffer
			buffer = ""
			yield char
		
		else:
			buffer += char
			
	if buffer != "": yield buffer
	
	

# DICT

# takes dict and unpacks list etc according to pdx script rules
def dict_convert(d,keeplists=[]):
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
	
	
pdx_conversions = {
	True:"yes",
	False:"no"
}


def topdx(data,indent=0):
	raw = ""

	for t in data:
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
			elif isinstance(t[2],collections.abc.Iterable):
				raw +=  "{\n"
				raw += topdx(t[2],indent=indent+1)
				raw += "\t" * indent
				raw += "}"
			raw += "\n"
			
		else:
			raw += t
			raw += "\n"
	
	return raw
	
	
	
# CSV

def csv_to_internal(inp):
	l = csv_to_list(inp)
	d = {row[0]: tuple(row[1:-1]) for row in l}
	return d
	
def internal_to_csv(d):
	l = [(k,) + d[k] + ("x",) for k in d]
	return list_to_csv(l)
	
def csv_to_list(inp):
	pseudo_file = io.StringIO()
	pseudo_file.write(inp)
	pseudo_file.seek(0)
	reader = csv.reader(pseudo_file,delimiter=";")
	return [tuple(row) for row in reader]
	
def list_to_csv(l):
	pseudo_file = io.StringIO()
	writer = csv.writer(pseudo_file,delimiter=";")
	for t in l:
		writer.writerow(t)
	pseudo_file.seek(0)
	return pseudo_file.read()
