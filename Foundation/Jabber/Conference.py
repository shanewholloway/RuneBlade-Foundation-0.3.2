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

"""Conference implementation for Jabber conferencing

The Jabber protocol can be found at http://jabber.org, 
and at the time of writting, specifically at 
http://docs.jabber.org/general/html/protocol.html

Specifically, this module relates to jabber:iq:conference.
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import weakref
from Foundation.Jabber.JabberSubject import JabberSubjectBase
from Foundation.Jabber import JID
from Foundation.Jabber import JabberObserver as JObs
from Foundation.SubjectObserver.Observer import Observer
from Foundation.SubjectObserver.AttributedSubject import AttributedSubject

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Conference(JabberSubjectBase):
    """Sets up a Jabber conference at a specific conference JID.

    Note that conferencing is a Jabber module, and as such, needs to
    be enabled on the Jabber server itself.
    """
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, JC, ConferenceJID):
        JabberSubjectBase.__init__(self)
        # Save the conference JID
        self.ConferenceJID = JID.JID(ConferenceJID).nominal()

        # Save the Jabber Client
        self.JC = weakref.ref(JC)

        # Pretend like we are a Jabber.Client
        self.stream = weakref.proxy(self)
        # Insert our greedy little meathooks...
        obs = Observer(self._CallConference, self._BidConference)
        JC.stream.AddObserver('message', obs)
        JC.stream.AddObserver('presence', obs)
        JC.stream.AddObserver('iq', obs)

        # Prepare to get the conference roster
        self.roster = AttributedSubject()
        obs = JObs.JabberObserver(self._OnIQBrowseSets, BidValue=0.1)
        obs.AddRule(JObs.MatchAttributes(type='set', from_=self.ConferenceJID.nominal()))
        obs.AddRule(JObs.MatchHasChildNamespace('jabber:iq:browse'))
        self.stream.AddObserver('iq', obs)

    def __del__(self):
        """Disconnects from the conference if the Jabber Client still exists"""
        if self.JC(): self.Presence(type='unavailable')

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _CallConference(self, subject, **UpdateDict):
        """Dummy method to place in the stream Observer.  Should never be called."""
        assert 0

    def _BidConference(self, subject, **UpdateDict):
        """Selects only the messages off the jabber stream that are pertinate to the conference JID"""
        for each in UpdateDict.itervalues():
            if each.from_ not in self.ConferenceJID:
                # This 'subject' is defined to be from JIDs in the conference
                return 0
        return self.__super.Bid(subject, **UpdateDict)
        
    def _OnIQBrowseSets(self, subject, iq):
        users = getattr(iq, 'user', [])
        for conference in getattr(iq, 'conference', []):
            users.extend(getattr(conference, 'user', []))

        for user in users:
            if getattr(user, 'type', '') == 'remove':
                del self.roster[user.jid]
            else: 
                self.roster[user.jid] = getattr(user, 'name', user.jid)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def Disconnect(self):
        """Disconnects from the conference by sending and unavailable presence"""
        return self.Presence(type='unavailable')

    def GetInformation(self, callback):
        """Requests information about the conference in question.  
        
        Returns iqQuery object."""
        return self.JC().Query('jabber:iq:conference', toJID=self.ConferenceJID, type='get', callback=callback)

    def JoinAs(self, Nick, Secret='', Privacy=0, callback=None):
        """Joins the conference using Nick(s), and Secret if need be.  
        
        Returns iqQuery object."""
        xml = ''
        if Nick:
            if not isinstance(Nick, (list, tuple)): Nick = (Nick,)
            xml = ''.join(['<nick>%s</nick>' % x for x in Nick])
        if Secret: xml += '<secret>%s</secret>' % Secret
        if Privacy: xml += '<privacy/>'

        self.Presence()

        return self.JC().Query('jabber:iq:conference', toJID=self.ConferenceJID, type='set', xml=xml, callback=callback)

    def ChangeNick(self, Nick, callback=None):
        """Changes the nickname of the conference connection"""
        newjid = self.ConferenceJID.join(self.ConferenceJID.split(1,3) + [Nick])
        return self.JC().Presence(newjid)
        
    def Invite(self, *args, **kw):
        """Invites a JID to join the conference"""
        kw['xml'] = kw.get('xml', '') + '<x xmlns="jabber:x:conference" jid="%s"/>' % self.ConferenceJID
        return self.JC().Message(*args, **kw)

    def Message(self, body='', subject='', type='groupchat', id=None, xml=''):
        """Sends a message to the conference"""
        return self.JC().Message(self.ConferenceJID, body=body, subject=subject, type=type, id=id, xml=xml)

    def Presence(self, *args, **kw):
        """Sends a presence to the conference"""
        return self.JC().Presence(self.ConferenceJID, *args, **kw)

Conference._Conference__super = super(Conference)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    print "Testing..."
    import Client

    def PrintRoster(roster, **kw):
        print kw.values(), 'is now in', roster.values()

    def PrintStuff(stream, **kw):
        for each in kw.itervalues():
            print each._toXML()
    jc = Client.Client('www.runeblade.com', fileIn=open('conf.in','w'), fileOut=open('conf.out','w'))
    jc.Authenticate('shane.test1', 'testing', 'PyConferenceTest')
    conf = Conference(jc, 'shane.conf@private.www.runeblade.com')
    conf.roster.AddObserver(PrintRoster)
    #conf.AddObserver('message', PrintStuff)
    #conf.AddObserver('presence', PrintStuff)
    #conf.AddObserver('iq', PrintStuff)
    conf.JoinAs('RuneBlade.Development')
    conf.Message('Hello from RB development!!!')
    conf.ChangeNick('shane.test1')
    conf.Message('Why, isnt this fun?')
    #conf.Invite('shane.holloway@www.runeblade.com', subject='Please join me!', body='Please join me in shane.conf@private.www.runeblade.com')
    jc.ProcessPending(1.0)
    try: 
        while 1: jc.Process(1.0)
    except KeyboardInterrupt: pass
    print "Test complete."


