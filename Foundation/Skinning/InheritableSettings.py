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

from Foundation.ChainedDict import ChainedDict
from Foundation.Utilities import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class InheritSettingsMixin(object):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    BaseNamespace = 'http://namespaces.runeblade.com/skin'

    BaseSettingPrefix = "SkinSettings"
    BaseSettingsSave = (BaseNamespace, 'save')
    BaseSettingsInherit = (BaseNamespace, 'inherit')
    BaseSettingsLevel = (BaseNamespace, 'level')
    BaseSettingsRoot = (BaseNamespace, 'root')

    default_settings = {
        BaseSettingsSave:'',
        BaseSettingsInherit:'',
        BaseSettingsLevel:'0',
        BaseSettingsRoot:'0',
        }

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _InheritSettings(self, settings, InheritList, SettingPrefix=None, Resilliant=0):
        SettingPrefix = SettingPrefix or self.BaseSettingPrefix
        InheritList.reverse()
        for SettingName in InheritList:
            SettingName = SettingPrefix + SettingName
            try: InheritedSettings = getattr(self.context, SettingName, None)
            except AttributeError:
                if not Resilliant: raise
            if InheritedSettings is not None:
                settings.update(InheritedSettings)
        return settings

    def _SaveSettingsAdv(self, SettingName, settings=None, SettingPrefix=None, SettingLevel=None):
        settings = settings or self.local_settings

        # Save settings to be inherited 
        SettingPrefix = SettingPrefix or self.BaseSettingPrefix
        SettingName = SettingPrefix + SettingName

        if SettingLevel is not None:
            ctx = self.context._GetContext(SettingLevel)
        else: ctx = self.context._OwnerContext(self.BaseSettingsRoot, returnLast=1)

        return setattr(ctx, SettingName, settings)

    def _SaveSettings(self, settings=None, SettingPrefix=None):
        settings = settings or self.local_settings
        if self.BaseSettingsLevel in settings:
            SettingLevel = int(settings[self.BaseSettingsLevel])
            del settings[self.BaseSettingsLevel]
        else: SettingLevel = None
        if self.BaseSettingsSave in settings:
            SettingName = settings[self.BaseSettingsSave]
            del settings[self.BaseSettingsSave]
            return self._SaveSettingsAdv(SettingName, settings, SettingPrefix, SettingLevel)

    def _InitSettings(self, settings, bAllowInheritance=1):
        if not bAllowInheritance:
            newsettings = settings
        else:
            # Get inherited settings
            newsettings = {}
            BaseSettingsList = self.default_settings.get(self.BaseSettingsInherit, '')
            if BaseSettingsList: self._InheritSettings(newsettings, strtolist(BaseSettingsList), Resilliant=1)
            BaseSettingsList = settings.get(self.BaseSettingsInherit, '')
            if BaseSettingsList: self._InheritSettings(newsettings, strtolist(BaseSettingsList))

            # Merge the two settings
            if newsettings: newsettings.update(settings)
            else: newsettings = settings

            if self.BaseSettingsInherit in newsettings: 
                del newsettings[self.BaseSettingsInherit]

            self._SaveSettings(newsettings)

        # now set our settings to be a chained grouping of
        # the modified incoming settings, and the chained settings
        self.settings = ChainedDict(newsettings)
        self.settings.chained = self.default_settings

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Properties
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _GetLocalSettings(self):
        try:
            result = {}
            for each in self.settings:
                if not isinstance(each, tuple):
                    result[each] = self.settings[each]
            return result
        except AttributeError: return {}
    local_settings = property(fget=_GetLocalSettings)

    def _GetSourceSettings(self):
        try: return self.settings.source
        except AttributeError: return self.settings
    source_settings = property(fget=_GetSourceSettings)

