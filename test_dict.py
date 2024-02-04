#!/usr/bin/env python3
# -*- coding: utf_8 -*-

class Dict(dict):
	def __init__(self, *args, **kwargs):
		for item in args:
			self._parse_dict(item)
		self._parse_dict(kwargs)
	#end define
	
	def _parse_dict(self, d):
		for key, value in d.items():
			if type(value) == dict:
				value = Dict(value)
			if type(value) == list:
				value = self._parse_list(value)
			self[key] = value
	#end define
	
	def _parse_list(self, l):
		result = list()
		for value in l:
			if type(value) == dict:
				value = Dict(value)
			result.append(value)
		return result
	#end define
	
	def __setattr__(self, key, value):
		self[key] = value
	#end define
	
	def __getattr__(self, key):
		return self.get(key)
	#end define
#end class

d = Dict()
d.a = 1
print(d)
print(d.a)
