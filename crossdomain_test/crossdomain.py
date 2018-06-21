import clr
clr.AddReference("WebsocketClient.exe")
from WebsocketClient import *
def check_conn(origin):
    print "Testing origin - " + origin
    ws = SyncWebsockClient()
    ws.Connect(host, origin, "JSESSIONID=54E9DFF1B747E86837C7ED3B41AEFC3E")
    ws.Send("first message to send")
    msg = ws.Read()
    ws.Close()
    if msg == "message that is part of valid session":
      print "Connection successful!!"
      return True
    else:
      return False
def check_nw():
  for nws in ["192.168.0.0/16", "172.16.0.0/12", "10.0.0.0/8"]:
    for ip in Tools.NwToIp(nws):
      if check_conn("http://" + ip):
        break
check_nw()