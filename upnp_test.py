import upnpclient

devices = upnpclient.discover()

l = list()
for d in devices:
	for s in d.services:
		if "WANIPConn1" == s.name:
			l.append(d)
#end for

d = l[0]
d.WANIPConn1.GetExternalIPAddress()
d.WANIPConn1.GetNATRSIPStatus()

d.WANIPConn1.AddPortMapping(
	NewRemoteHost='0.0.0.0',
	NewExternalPort=12345,
	NewProtocol='TCP',
	NewInternalPort=12345,
	NewInternalClient='192.168.0.10',
	NewEnabled='1',
	NewPortMappingDescription='Testing',
	NewLeaseDuration=10000)

d.WANIPConn1.AddPortMapping(
	NewRemoteHost=None,
	NewExternalPort=23456,
	NewProtocol='TCP',
	NewInternalPort=23456,
	NewInternalClient='192.168.0.20',
	NewEnabled='1',
	NewPortMappingDescription='Testing2',
	NewLeaseDuration=0)

d.WANIPConn1.DeletePortMapping(
	NewRemoteHost=None,
	NewExternalPort=49325,
	NewProtocol="TCP")
