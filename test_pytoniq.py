import asyncio

from pytoniq import LiteClient, BlockIdExt
from multiprocessing import Process, Manager

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


async def atest1():
	client = LiteClient.from_mainnet_config(ls_i=0, trust_level=2)

	await client.connect()

	data = await client.get_time()
	print("get_time:", data)

	mc_info = await client.get_masterchain_info()
	mc_info = Dict(mc_info)
	print("get_masterchain_info:", mc_info)
	print("mc_info.last.seqno:", mc_info.last.seqno)
	print("mc_info.last.root_hash:", mc_info.last.root_hash)
	
	'''
	data = await client.get_account_state("EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N")
	print("get_account_state:", data)
	
	data = await client.run_get_method("EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N", "seqno", [])
	print("run_get_method:", data)

	data = await client.raw_get_all_shards_info()
	print("raw_get_all_shards_info:", data)
	
	data = await client.get_config_params([4])
	print("get_config_params:", data)
	
	#data = await client.get_block_header(mc_info.last.workchain, mc_info.last.shard, mc_info.last.seqno, mc_info.last.root_hash, mc_info.last.file_hash)
	#print("get_block_header:", data)
	
	#data = await client.get_block(mc_info.last.workchain, mc_info.last.shard, mc_info.last.seqno, mc_info.last.root_hash, mc_info.last.file_hash)
	#print("get_block:", data)
	
	data = await client.get_transactions(address='EQBvW8Z5huBkMJYdnfAEM5JqTNkuWX3diqYENkWsIL0XggGG', count=1)
	print("get_transactions:", data)
	
	block_trans = await client.raw_get_block_transactions(BlockIdExt.from_dict(mc_info.last))
	print("get_block_transactions:", block_trans)
	
	tr = Dict(block_trans[0])
	data = await client.get_one_transaction(tr.account, tr.lt, BlockIdExt.from_dict(mc_info.last))
	print("get_one_transaction:", data)
	
	body = bytes.fromhex("b5ee9c7241010101000e0000180000000400000000628f328d83ad456c")
	data = await client.raw_send_message(body)
	print("raw_send_message:", data)

	await client.close()
	'''
#end define

def start_process(*args, **kwargs):
	p = Process(target=process_work, args=args, kwargs=kwargs)
	p.start()
	return p
#end define

def process_work(return_dict, procnum, func, *args, **kwargs):

	return_dict[procnum] = asyncio.run(func(*args, **kwargs))
#end define

def test1():
	manager = Manager()
	return_dict = manager.dict()

	client = LiteClient.from_mainnet_config(ls_i=0, trust_level=2)
	asyncio.run(client.connect())

	p1 = start_process(return_dict, procnum=1, func=client.get_time)
	p2 = start_process(return_dict, procnum=1, func=client.get_masterchain_info)
	p1.join()
	p2.join()
	print(return_dict)
#end define



if __name__ == '__main__':
	asyncio.run(atest1())
	test1()
#end define
