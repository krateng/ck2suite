# class to represent arbitrary ck2 data

import io
import collections.abc

import yaml


pdx_conversions = {
	True:"yes",
	False:"no"
}

class CK2Definition:

	"""
	Each scope is represented by a list. Its entries are 
	1) tuples of three (for scope / expression, e.g. diplomacy = 2 or trait = patient or ROOT = {...} ) whereas the third part of the tuple (the expression) can be another list of that sort
	2) pure expressions, for lists like on_action = { on_siege = { events = { 13 14 15 } } }


	"""


	def __init__(self,inp,format=None):
	
		# FILE REFERENCE -> Guess format, get File handle
		if isinstance(inp,str):
			formats = {
				"txt":"ck2",
				"yml":"yml",
				"yaml":"yml"
			}
			ext = inp.split(".")[-1].lower()
			if format is None:
				if ext in formats:
					format = formats[ext]
			with open(inp,"r") as fi:
				self.__init__(fi,format=format)
				
		# FILE HANDLE -> Extract Object
		elif isinstance(inp,io.IOBase):
			raw = inp.read()

			if format == "ck2":
				tokens = _tokenize(raw)
				nested = _nested_tokens(tokens)
				self.__init__(_parse(nested))
			elif format == "yml":
				self.__init__(yaml.safe_load(raw))
		
		# OBJECT -> covert to native list
		elif isinstance(inp,collections.abc.Mapping):
			self.data = _dict_convert(inp)
			
		elif isinstance(inp,collections.abc.Iterable):
			self.data = inp

	def write(self,f,format="ck2"):
		if isinstance(f,str):
			with open(f,"w") as fi:
				self.write(fi,format=format)
		elif isinstance(f,io.IOBase):
			f.write(self.generate(format))
			
	def print(self,format="ck2"):
		print(self.generate(format=format))
			
	def generate(self,format="ck2"):
		formats = {
			"ck2":CK2Definition._topdx
		}
		return formats[format](self.data)
	
	
		
	def _topdx(data,indent=0):
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
					raw += CK2Definition._topdx(t[2],indent=indent+1)
					raw += "\t" * indent
					raw += "}"
				raw += "\n"
				
			else:
				raw += t
				raw += "\n"
		
		return raw
		
		
	def getall(self,scope):
		entries = [element for element in self.data if element[0] == scope]
		return CK2Definition(entries)
		
	def getfirst(self,scope):
		entries = [element for element in self.data if element[0] == scope]
		try:
			first = entries[0]
			if isinstance(first[2],list):
				return CK2Definition(first[2])
			else:
				return first[1],first[2]
		except:
			return None
		
		



# PDX FILE
	
def _parse(tokens):
	
	l = []
	
	while len(tokens) >= 3:
		if tokens[1] in ("=","==","<=","=<","<",">",">=","=>"):
			l.append((tokens[0],tokens[1],tokens[2] if isinstance(tokens[2],str) else _parse(tokens[2])))
			tokens = tokens[3:]
		else:
			l.append(tokens[0])
			tokens = tokens[1:]
	
	return l
	
def _nested_tokens(tokens):
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
	
def _tokenize(txt):
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
	
	
# DICT

# takes dict and unpacks list etc according to pdx script rules
def _dict_convert(d,keeplists=[]):
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
