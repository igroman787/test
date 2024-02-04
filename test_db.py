#!/usr/bin/env python3
# -*- coding: utf_8 -*-

import os
import time
import json
import threading


db = None
old_db = None
db_path = "mytoncore.db"

class Dict(dict):
	def __init__(self, *args, **kwargs):
		for item in args:
			self._parse_dict(item)
		self._parse_dict(kwargs)
	#end define

	def _parse_dict(self, d):
		for key, value in d.items():
			if type(value) in [dict, Dict]:
				value = Dict(value)
			if type(value) == list:
				value = self._parse_list(value)
			self[key] = value
	#end define

	def _parse_list(self, lst):
		result = list()
		for value in lst:
			if type(value) in [dict, Dict]:
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

def read_file(path):
	with open(path, 'rt') as file:
		text = file.read()
	return text
#end define

def write_file(path, text=""):
	with open(path, 'wt') as file:
		file.write(text)
#end define

def read_db(db_path):
	err = None
	for i in range(10):
		try:
			return read_db_process(db_path)
		except Exception as ex:
			err = ex
			time.sleep(0.1)
	raise Exception(f"read_db error: {err}")
#end define

def read_db_process(db_path):
	text = read_file(db_path)
	data = json.loads(text)
	return Dict(data)
#end define

def write_db(data):
	text = json.dumps(data, indent=4)
	lock_file(db_path)
	write_file(db_path, text)
	unlock_file(db_path)
#end define

def lock_file(path):
	pid_path = path + ".lock"
	for i in range(300):
		if os.path.isfile(pid_path):
			time.sleep(0.01)
		else:
			write_file(pid_path)
			return
	raise Exception("lock_file error: time out.")
#end define

def unlock_file(path):
	pid_path = path + ".lock"
	try:
		os.remove(pid_path)
	except:
		print("Wow. You are faster than me")
#end define

def merge_three_dicts(local_data, file_data, old_file_data):
	if (id(local_data) == id(file_data) or
		id(file_data) == id(old_file_data) or
		id(local_data) == id(old_file_data)):
		print(local_data.keys())
		print(file_data.keys())
		raise Exception(f"merge_three_dicts error: merge the same object")
	#end if
	
	need_write_local_data = False
	if local_data == file_data and file_data == old_file_data:
		return need_write_local_data
	#end if

	dict_keys = list()
	dict_keys += [key for key in local_data if key not in dict_keys]
	dict_keys += [key for key in file_data if key not in dict_keys]
	for key in dict_keys:
		buff = merge_three_dicts_process(key, local_data, file_data, old_file_data)
		if buff is True:
			need_write_local_data = True
	return need_write_local_data
#end define

def merge_three_dicts_process(key, local_data, file_data, old_file_data):
	need_write_local_data = False
	tmp = mtdp_get_tmp(key, local_data, file_data, old_file_data)
	if tmp.local_item != tmp.file_item and tmp.file_item == tmp.old_file_item:
		# find local change
		mtdp_flc(key, local_data, file_data, old_file_data)
		need_write_local_data = True
	elif tmp.file_item != tmp.old_file_item:
		# find config file change
		mtdp_fcfc(key, local_data, file_data, old_file_data)
	return need_write_local_data
#end define

def mtdp_get_tmp(key, local_data, file_data, old_file_data):
	tmp = Dict()
	tmp.local_item = local_data.get(key)
	tmp.file_item = file_data.get(key)
	tmp.old_file_item = old_file_data.get(key)
	tmp.local_item_type = type(tmp.local_item)
	tmp.file_item_type = type(tmp.file_item)
	tmp.old_file_item_type = type(tmp.old_file_item)
	return tmp
#end define

def mtdp_flc(key, local_data, file_data, old_file_data):
	dict_types = [dict, Dict]
	tmp = mtdp_get_tmp(key, local_data, file_data, old_file_data)
	if tmp.local_item_type in dict_types and tmp.file_item_type in dict_types and tmp.old_file_item_type in dict_types:
		merge_three_dicts(tmp.local_item, tmp.file_item, tmp.old_file_item)
	elif tmp.local_item is None:
		print(f"find local change {key} -> {tmp.local_item}")
		pass
	elif tmp.local_item_type not in dict_types:
		print(f"find local change {key}: {tmp.old_file_item} -> {tmp.local_item}")
		pass
	elif tmp.local_item_type in dict_types:
		print(f"find local change {key}: {tmp.old_file_item} -> {tmp.local_item}")
		pass
	else:
		raise Exception(f"mtdp_flc error: {key} -> {tmp.local_item_type}, {tmp.file_item_type}, {tmp.old_file_item_type}")
#end define

def mtdp_fcfc(key, local_data, file_data, old_file_data):
	dict_types = [dict, Dict]
	tmp = mtdp_get_tmp(key, local_data, file_data, old_file_data)
	if tmp.local_item_type in dict_types and tmp.file_item_type in dict_types and tmp.old_file_item_type in dict_types:
		merge_three_dicts(tmp.local_item, tmp.file_item, tmp.old_file_item)
	elif tmp.file_item is None:
		print(f"find config file change {key} -> {tmp.file_item}")
		local_data.pop(key)
	elif tmp.file_item_type not in dict_types:
		print(f"find config file change {key}: {tmp.old_file_item} -> {tmp.file_item}")
		local_data[key] = tmp.file_item
	elif tmp.file_item_type in dict_types:
		print(f"find config file change {key}: {tmp.old_file_item} -> {tmp.file_item}")
		local_data[key] = Dict(tmp.file_item)
	else:
		raise Exception(f"mtdp_fcfc error: {key} -> {tmp.local_item_type}, {tmp.file_item_type}, {tmp.old_file_item_type}")
#end define

def save_db():
	global db, old_db
	file_data = read_db(db_path)
	need_write_local_data = merge_three_dicts(db, file_data, old_db)
	old_db = Dict(db)
	if need_write_local_data is True:
		write_db(db)
#end define

def db_saving():
	while True:
		time.sleep(3)
		save_db()
#end define

def input_working():
	global db, old_db
	while True:
		time.sleep(1)
		buff = input("print key and value:")
		data = buff.split(' ')
		key = data[0]
		value = data[1]
		db[key] = value
		print(f"set {key}:{value}")
#end define

def test():
	global db, old_db
	data = read_db(db_path)
	db = data.copy()
	old_db = data.copy()
	thr = threading.Thread(target=db_saving, 
		name="db_saving", 
		daemon=True)
	thr.start()
	input_working()
#end define

test()
