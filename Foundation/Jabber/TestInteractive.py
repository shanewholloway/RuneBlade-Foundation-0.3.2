import sys
import Client

def CreateJC(server, username, password, resource='python-interactive'):
    jc = Client.Client(server, fileIn=sys.stdout, fileOut=sys.stdout)
    jc.Authenticate(username, password, resource)
    jc.Presence()
    return jc

