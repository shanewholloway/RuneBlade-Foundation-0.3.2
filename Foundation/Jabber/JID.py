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

"""JID class and convenience functions.

Dependencies:
    re
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import re

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = ['reJabberURL', 'reJabberJID', 'JID']

_restrID = '''[\w-]+(?:[\w\.-]+[\w-]+)?'''
_restrServer = '''[\w-]+(?:[\w\.-]+[\w-]+)?(?::[0-9]+)?'''
_restrResource = '''\S+'''
reJabberURL = re.compile('''(?:jabber://)?(%s)''' % (_restrServer))
reJabberJID = re.compile('''(?:(%s)@)?(%s)(?:/(%s))?''' % (_restrID, _restrServer, _restrResource))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def splitnorm(strJID, start=1, end=4):
    """Splits username@server/resource into [username, server, resource], 
    and normalizes username and server.  Returns a start to end-1 of the list"""
    result = reJabberJID.split(strJID)[start:end]
    return [x and x.lower() or x for x in result[1-start:3-start]] + result[3-start:]

def split(strJID, start=1, end=4):
    """Splits username@server/resource into [username, server, resource].  
    Returns a start to end-1 of the list"""
    return reJabberJID.split(strJID)[start:end]

def splitex(strJID, start=1, end=4, normalize=0):
    """Uses normalize flag to choose between split and splitnorm."""
    if normalize: return splitnorm(strJID, start, end)
    else: return split(strJID, start, end)

def cmp_(strJIDa, strJIDb, resource=1):
    """Compares two JIDs, including resources if flag is set.  
    Note that case is insensitive in username and server, but IS sensitive in the resource."""
    jida = splitnorm(strJIDa, end=3+resource)
    jidb = splitnorm(strJIDb, end=3+resource)
    return cmp(jida, jidb)

def compare(*args, **kw):
    """Same as cmp_, except returns a python truth value instead of a cmp result."""
    return 0 == cmp_(*args, **kw)

def contains(strJIDa, strJIDb):
    """Returns true if strJIDb is strJIDb, or strJIDb is qualified by a resource.
    Will fail if strJIDa has a resource and is not the same JID as strJIDb."""
    jida = filter(None, splitnorm(strJIDa, end=4))
    jidb = filter(None, splitnorm(strJIDb, end=3))[-len(jida):]
    return jida == jidb or compare(strJIDa, strJIDb)

def join(*args):
    """Combines a (username, server, resource) into username@server/resource, but does so 
    in several different formats"""
    if isinstance(args[0], (tuple, list)):
        args = tuple(args[0])
    args = filter(None, args)
    if len(args) == 3:
        return JID('%s@%s/%s' % args)
    elif len(args) == 2:
        return JID('%s@%s' % args)
    elif len(args) == 1:
        return args[0]
    else: return ''

def username(strJID, normalize=0): 
    """Extracts the username from the JID"""
    return splitex(strJID, 1, 2, normalize)[0]
def server(strJID, normalize=0): 
    """Extracts the server from the JID"""
    return splitex(strJID, 2, 3, normalize)[0]
def resource(strJID, normalize=0): 
    """Extracts the resource from the JID"""
    return splitex(strJID, 3, 4, normalize)[0]
def noresource(strJID, normalize=0): 
    """Returns the JID without the resource qualification"""
    return join(splitex(strJID, 1, 3, normalize))
def nominal(strJID): 
    """Returns the JID with username and server lowercased, and no resource"""
    return join(splitnorm(strJID, 1, 3))
def normalize(strJID): 
    """Returns the JID with the username and server lowercased, but retaining the resource"""
    return join(splitnorm(strJID))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Class JID 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class JID(str):
    """An object-oriented way of dealing with JIDs"""

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    split = split
    splitnorm = splitnorm
    splitex = splitex
    
    normalize = normalize
    nominal = nominal
    compare = compare

    noresource = noresource
    username = username
    server = server
    resource = resource
 
    def join(Class, *args):
        return Class(join(*args))
    join = classmethod(join)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    __cmp__ = cmp_
    def __eq__(self, other): 
        return cmp_(self, other) == 0
    def __ne__(self, other): 
        return cmp_(self, other) != 0
    def __lt__(self, other): 
        return cmp_(self, other) < 0
    def __le__(self, other): 
        return cmp_(self, other) <= 0
    def __gt__(self, other): 
        return cmp_(self, other) > 0
    def __ge__(self, other): 
        return cmp_(self, other) >= 0

    def __contains__(self, other):
        return contains(self, other)
        
    def __hash__(self):
        return hash(tuple(self.splitnorm()))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Testing 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def _Test_JID():
    j1 = JID('user.name@jabber.org/Resource')
    j2 = JID('User.Name@Jabber.org/Resource')
    j3 = JID('User.Name@Jabber.org/ReSoUrCe')
    j4 = JID('conference.jabber.org')

    assert j1 in j1
    assert j1 in JID('user.name@Jabber.org')
    assert j3 in JID('JaBBer.org')
    assert j2 not in j3

    assert j4.normalize() == j4
    assert j4.username() is None
    assert j4.server() == j4
    assert j4.resource() is None
    assert j4.noresource() == j4

    assert j1 == j2
    assert j1 >= j2
    assert j1 <= j2
    assert j1 != j3
    assert j2 != j3
    assert j3 < j1
    assert j1 > j3
    assert j3 < j2
    assert j2 > j3
    assert j1.splitnorm() == j2.splitnorm() != j3.splitnorm()
    assert j1.splitnorm(1,3) == j2.splitnorm(1,3) == j3.splitnorm(1,3)
    assert hash(j1) == hash(j2)
    assert hash(j1) != hash(j3)
    assert hash(j2) != hash(j3)

    dictTest = {}
    dictTest[j1] = 1
    dictTest[j2] = 1
    dictTest[j3] = 1
    # Length should be 2 because j2 and j1s' hashes should be identical
    assert len(dictTest)==2
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    print "Testing..."
    _Test_JID() 
    print "Test complete."


