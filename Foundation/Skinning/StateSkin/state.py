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

from Foundation.Skinning import SkinObject
from Foundation.SubjectObserver import StateMachine
from Foundation.Utilities import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Class Initialization 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

class state(SkinObject.SkinObject):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_settings = SkinObject.SkinObject.default_settings.copy()
    default_settings.update({
        #'name': '',
        'value': '0', 
        'incvalue': '1', 
        'autoset': '1', 
        'operator': 'and'})

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SkinInitialize(self):
        if self.settings['operator'] == 'or':
            InfluxState = StateMachine.OrStateList
        else: #elif self.settings['operator'] == 'and':
            InfluxState = StateMachine.AndStateList

        self.settings['value'] = int(self.settings['value'])
        self.settings['incvalue'] = int(self.settings['incvalue'])
        self.object = StateMachine.StateSubject(InfluxState, **self.local_settings)

        if int(self.settings['autoset']):
            self.object.AddObserver('precondition', self._DoSetState)

        # Add this state to the state machine's state map
        self.context.statemap[self.settings['name']] = self.object

    def _DoSetState(self, subject, precondition):
        if precondition and subject._Influxs:
            subject.SetState()

    def _addData(self, data):
        self.object.description += data

    def SkinFinalize(self):
        pass
