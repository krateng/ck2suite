# class to represent arbitrary ck2 data

import io
import collections.abc
import os

import yaml

from . import functions as funcs


ck2enc = "cp1252"



class CK2Base:
	def __init__(self,inp,format=None):

		# FILE REFERENCE -> Guess format, get File handle
		if isinstance(inp,str) and os.path.isfile(inp):
			ext = inp.split(".")[-1].lower()
			if format is None:
				format = self.__class__.defaultformat
				for f in self.__class__.formats:
					if ext in self.__class__.formats[f]["extensions"]:
						format = f
			with open(inp,"r",encoding=ck2enc) as fi:
				self.__init__(fi,format=format)

		# FILE HANDLE -> Extract String
		elif isinstance(inp,io.TextIOBase):
			if format is None: format = self.__class__.defaultformat
			raw = inp.read()
			self.__init__(raw,format=format)

		# RAW TEXT -> handle
		elif isinstance(inp,str):
			if format is None: format = self.__class__.defaultformat
			parsed = self.__class__.formats[format]["handler"](inp)
			self.__init__(parsed)

		# OBJECT -> convert
		else:
			if isinstance(inp,collections.abc.Mapping):
				self.__init_from_mapping__(inp)
			elif isinstance(inp,collections.abc.Sequence):
				self.__init_from_sequence__(inp)

	def write(self,outp,format=None):
		if isinstance(outp,str):
			ext = outp.split(".")[-1].lower()
			if format is None:
				for f in self.__class__.formats:
					if ext in self.__class__.formats[f]["extensions"]:
						format = f
			with open(outp,"w",encoding=ck2enc) as fi:
				self.write(fi,format=format)
		elif isinstance(outp,io.TextIOBase):
			outp.write(self.generate(format=format))


	def print(self,format=None):
		print(self.generate(format=format))

	def generate(self,format=None):
		if format is None: format = self.__class__.defaultformat
		return self.__class__.formats[format]["generator"](self.data)


class CK2Definition(CK2Base):

	"""
	Each scope is represented by a list. Its entries are
	1) tuples of three (for scope / expression, e.g. diplomacy = 2 or trait = patient or ROOT = {...} ) whereas the third part of the tuple (the expression) can be another list of that sort
	2) pure expressions, for lists like on_action = { on_siege = { events = { 13 14 15 } } }


	"""

	formats = {
		"ck2":{"extensions":["txt","suv"],"handler":funcs.parse_ck2,"generator":funcs.topdx },		# ck2 text files
		"yml":{"extensions":["yml","yaml"],"handler":yaml.safe_load},					# yaml file
	}
	defaultformat = "ck2"

	def __init_from_mapping__(self,inp):
		self.data = funcs.dict_convert(inp)

	def __init_from_sequence__(self,inp):
		self.data = inp




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

	def separate_top_scopes(self):
		result = {}
		for element in self.data:
			result.setdefault(element[0],CK2Definition([])).data += element[2]
		return result



class CK2Localisation(CK2Base):

	formats = {
		"ck2csv":{"extensions":["csv"],"handler":funcs.csv_to_internal,"generator":funcs.internal_to_csv},	# normal ck2 csv with ; delimiters and x in last row
	}
	defaultformat = "ck2csv"
	languages = ("english","french","german",None,"spanish",None,None,None,None,None,None,None,None)



	def __init_from_mapping__(self,inp,language="english"):

		if any(isinstance(inp[key],tuple) for key in inp):
			# internal dict structure
			self.data = inp
		else:
			# simple mapping from key to text
			self.data = {key: tuple((inp[key] if l==language else "") for l in CK2Localisation.languages) for key in inp}

	def __init_from_sequence__(self,inp):
		if all (isinstance(e,collections.abc.Mapping) for e in inp):
			self.data = {e["key"]: tuple(e.get(l,"") for l in CK2Localisation.languages) for e in inp}

		elif all (isinstance(e,collections.abc.Iterable) for e in inp):
			self.data = {row[0]: tuple(row[1:]) for row in inp}


	def get_localisation(self,key,language="english"):
		row = self.data.get(key)
		loc = row[CK2Localisation.languages.index(language)]
		if loc == "": loc = row[0]
		return loc
