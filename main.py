import xbmc
import xbmcaddon
import xbmcgui

import os
import socket
import urllib2
import json
import const
from utils import addon_log


__addon__ = xbmcaddon.Addon(id=const.PLUGINNAME)
__icon__ = __addon__.getAddonInfo('icon')
__lang__ = __addon__.getLocalizedString   


class BT_Manager(xbmcgui.WindowXML):
    

    _lang = const.LANG
    _debug = False
    _jsonObj = object

    def __init__(self, *args, **kwargs):
        addon_log(self._debug, 'Init')
        xbmcgui.WindowXML.__init__(self)

        if kwargs:           
            self._debug = kwargs.get('_debug')
            addon_log(self._debug, 'kwargs %s ' % (self._debug))

    def onInit(self):

        """Window Init"""
        addon_log(self._debug, 'onInit')
        self.localize()        
        self._window = xbmcgui.getCurrentWindowId();
        # set window name in order to identify it from when sending action from services 
        xbmcgui.Window(self._window).setProperty("windowName", "bt_manager")

        self.setLabels()
        xbmc.executebuiltin("Dialog.Close(busydialog)")

    def exit(self):
        addon_log(self._debug, 'Exiting ...')

        # cancel timers
        # self._cancel_timers()
        self.close()

    def localize(self):
        """
        Localize interface strings
        :return:
        """
        pass
        """
        self.getControl(60001).setLabel(__lang__(91200))
        self.getControl(60002).setLabel(__lang__(91201))
        self.getControl(60004).setLabel(__lang__(91202))
        self.getControl(60006).setLabel(__lang__(91203))
        self.getControl(60008).setLabel(__lang__(91204))
        self.getControl(60009).setLabel(__lang__(91205))
        """

    def onAction(self, action):

        """When action is performed"""
        buttonCode = action.getButtonCode()
        actionID = action.getId()
        addon_log(self._debug, "onAction(): control %i" % actionID)

        """
        if actionID == const.ACTION_PARENT_DIR or actionID == const.ACTION_PREVIOUS_MENU:
            addon_log(self._debug, "Trying to close")
            self.doClose()
            return True
        """

    def onClick(self, controlID):
        """When control is clicked"""
        addon_log(self._debug, "onClick(): control %i" % controlID)
        """
        if controlID == 60008:
            roomName = self.getControl(60007).getText().strip()
            self.setRoom(roomName, self._debug)
            addon_log(self._debug, "New Room %s" % roomName)
        if controlID == 60009:
            self.EXIT()
        """

    def onFocus(self, controlID):
        """On focus change"""
        self._controlId = controlID
        addon_log(self._debug, "onFocus(): control %i" % controlID)

    def doClose(self):
        """Close  the window and exit"""
        #self.close()
        self.EXIT()

    def EXIT(self):
        xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
        xbmc.executebuiltin("XBMC.ActivateWindow(Home)")

def main():

    """Read app settings"""
    setting = xbmcaddon.Addon(id=const.PLUGINNAME)

    scriptDebug = setting.getSetting("debug") == "true"
    
   
    """Open the window create an instance of windowXML"""

    fallBackXmlPath = xbmc.translatePath(__addon__.getAddonInfo('path'))
    addon_log(scriptDebug, 'Fall Back Path %s' % fallBackXmlPath)
    bluetooth_page = BT_Manager('script.prolab.bluetooth.main.xml', fallBackXmlPath, _debug=scriptDebug)

    bluetooth_page.doModal()

    del bluetooth_page