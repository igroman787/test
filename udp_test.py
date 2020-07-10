import ipaddress
import socket
from mypylib.mypylib import *

local = MyPyClass(__file__)

def UdpServer():
	addr = ("0.0.0.0", 8888)
	server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server.settimeout(3)
	server.bind(addr)
	while True:
		try:
			result = server.recvfrom(1024)
		except socket.timeout: 
			continue
		data = result[0]
		addr = result[1]
		local.AddLog('Received data: ' + data.decode('utf-8'))
		local.AddLog('From: ' + str(addr))
		msg = "ok."
		server.sendto(msg.encode('utf-8'), addr)
	server.close()
#end define

def udpClient():
	# addr = ("10.20.34.25", 6302)
	result = GetRequest("https://ton.org/ton-global.config.json")
	buffer = json.loads(result)
	dht = buffer.get("dht")
	staticNodes = dht.get("static_nodes")
	nodes = staticNodes.get("nodes")
	# print(json.dumps(nodes, indent=4))
	for node in nodes:
		addrLists = node.get("addr_list")
		addrs = addrLists.get("addrs")
		addr = addrs[0]

		buffer = addr.get("ip")
		ip_int = abs(buffer)
		ip = str(ipaddress.IPv4Address(ip_int))
		port = addr.get("port")
		addr = (ip, port)

		msg = "Please help me deal with the ADNL and DHT protocol. I am trying to write an implementation of this protocol in Python. Thanks)"
		data = msg.encode("utf-8")

		local.TryFunction(UdpSend, args=(addr, data))
#end define

def UdpSend(addr, data):
	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	client.settimeout(3)

	dl = client.sendto(data, addr)
	local.AddLog(f"send to {addr} {dl} bytes")

	result = client.recvfrom(1024)
	data = result[0]
	addr = result[1]
	msg = data.decode("utf-8")
	local.AddLog('Server reply: ' + msg)
#end define

def Init():
	local.Run()
	local.db["config"]["logLevel"] = "debug"
#end define

def General():
	# local.AddLog("step 1")
	# local.StartThread(UdpServer)

	# addr = ("10.20.34.25", 6302)
	# local.TryFunction(UdpServer)

	local.AddLog("step 2")
	udpClient()
#end define


###
### Start of the program
###

if __name__ == "__main__":
	Init()
	while True:
		General()
#end if



