#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ License 
##~ 
##- The RuneBlade Foundation library is intended to ease some 
##- aspects of writing intricate Jabber, XML, and User Interface (wxPython, etc.) 
##- applications, while providing the flexibility to modularly change the 
##- architecture. Enjoy.
##~ 
##~ Copyright (C) 2002  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~ 
##~ TechGame Networks, LLC can be reached at:
##~ 3578 E. Hartsel Drive #211
##~ Colorado Springs, Colorado, USA, 80920
##~
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import Client
import iqTimeResponse
import iqVersionResponse
import iqBrowseResponse
import SubscribeApproveResponse
import PresenceMap
import sys,socket

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def _test(server, username, password, resource='Foundation.Jabber.Test'):
    def PrintMe(*args, **kw):
        print "PrintMe:", args, kw
    try:
        jc = Client.Client(server)
        jc._SetDebug(sys.stdout, sys.stdout)

        #jc.Register(username, password)
        jc.Authenticate(username, password, resource, callback=PrintMe)
        
        pm = PresenceMap.PresenceMap(jc)

        jc.BrowseJID('cvs-holloways', None)
        jc.BrowseJID('sholloway@cvs-holloways', None)

        jc.Presence()

        jc.Roster = jc.QueryRoster()

        jc.Responses = []
        jc.Responses.append(iqTimeResponse.iqTimeResponse(jc))
        jc.Responses.append(iqVersionResponse.iqVersionResponse(jc, 'RuneBlade Foundation Jabber Test', '0.2'))
        jc.Responses.append(iqBrowseResponse.iqBrowseResponse(jc))
        jc.Responses.append(SubscribeApproveResponse.SubscribeApproveResponse(jc))
        
        while 1: 
            jc.Process(0.5)
    except KeyboardInterrupt:
        jc.SendXML('''<presence type="unavailable" />''')

    # Print out the roster
    print 
    print "Roster"
    print "~"*10
    for jid, rosteritem in jc.Roster.ByJID.iteritems():
        print jid, rosteritem.subscription
        print "    ", ''.join([x() for x in getattr(rosteritem, 'group', [])])
    print "~"*10
    print 

    # Print out the presence map
    print 
    print "Presence Map"
    print "~"*10
    for jid, resouces in pm.ByResource.iteritems():
        print jid
        for resource, presence in resouces.iteritems():
            print "    %s: %s (%s)" % (resource, getattr(presence, 'status', [''])[0], getattr(presence, 'show', [''])[0])
    print "~"*10
    print

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__': 
    import sys
    dictLogin = {'server':'cvs-holloways', 'username':'shane.test1', 'password':'testing'}
    strEval = ('","'.join(sys.argv[1:])).replace('=','":"')
    if strEval:
        strEval = ('{"%s"}'%strEval)
        dictLogin.update(eval(strEval, {}, {}))

    import time
    while 1:
        try:
            _test(**dictLogin)
            break
        except socket.error, info:
            print "Socket Error:", info
            time.sleep(5.0)
            print "Attempting Reconnect..."
        except KeyboardInterrupt:
            break

