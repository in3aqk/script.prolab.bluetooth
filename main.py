import xbmc
import xbmcaddon
import xbmcgui

import os
import socket
import urllib2
import json
import const
from utils import addon_log
from utils import getHwAddr,get_ip_address


__addon__ = xbmcaddon.Addon(id=const.PLUGINNAME)
__icon__ = __addon__.getAddonInfo('icon')
__lang__ = __addon__.getLocalizedString   




class Info(xbmcgui.WindowXML):
    """
    Get flights from the web service
    Reender flights list
    Select a flight to be monitored
    """

    _lang = const.LANG
    _debug = False
    _jsonObj = object

    def __init__(self, *args, **kwargs):
        addon_log(self._debug, 'Init')
        xbmcgui.WindowXML.__init__(self)

        if kwargs:
            self._mac = getHwAddr("eth0")
            self._ip = get_ip_address("eth0")
            self._serverIp = kwargs.get('_serverIp')
            self._installId = kwargs.get('_installId')
            self._debug = kwargs.get('_debug')


            addon_log(self._debug, 'kwargs %s %s %s %s' % (self._serverIp, self._mac, self._installId, self._debug))

    def onInit(self):

        """Window Init"""
        addon_log(self._debug, 'onInit')
        self.localize()
        self.getInfos(self._debug)
        self._window = xbmcgui.getCurrentWindowId();
        # set window name in order to identify it from when sending action from services (script.quasar.message)
        xbmcgui.Window(self._window).setProperty("windowName", "getinfo")

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

        self.getControl(60001).setLabel(__lang__(91200))
        self.getControl(60002).setLabel(__lang__(91201))
        self.getControl(60004).setLabel(__lang__(91202))
        self.getControl(60006).setLabel(__lang__(91203))
        self.getControl(60008).setLabel(__lang__(91204))
        self.getControl(60009).setLabel(__lang__(91205))

    def onAction(self, action):

        """When action is performed"""
        buttonCode = action.getButtonCode()
        actionID = action.getId()
        addon_log(self._debug, "onAction(): control %i" % actionID)


        if actionID == const.ACTION_PARENT_DIR or actionID == const.ACTION_PREVIOUS_MENU:
            addon_log(self._debug, "Trying to close")
            self.doClose()
            return True

    def onClick(self, controlID):
        """When control is clicked"""
        addon_log(self._debug, "onClick(): control %i" % controlID)
        if controlID == 60008:
            roomName = self.getControl(60007).getText().strip()
            self.setRoom(roomName, self._debug)
            addon_log(self._debug, "New Room %s" % roomName)
        if controlID == 60009:
            self.EXIT()



    def onFocus(self, controlID):
        """On focus change"""
        self._controlId = controlID
        addon_log(self._debug, "onFocus(): control %i" % controlID)

    def doClose(self):
        """Close  the window and exit"""
        #self.close()
        self.EXIT()


    def getInfos(self, debug):

        getInfoUrl = "http://%s/magellano/stb/getinfo/%s/%s" % (self._serverIp, self._mac, self._installId)

        addon_log(debug, 'getInfos....')

        self._jsonObj = json.loads(self.serverRequest(getInfoUrl,debug))


    def setRoom(self, roomName, debug):

        setRoomUrl = "http://%s/magellano/stb/setRoom/%s/%s/%s" % (self._serverIp, self._mac, self._installId,roomName)

        addon_log(debug, 'setRoom....')

        jsonResultObj = json.loads(self.serverRequest(setRoomUrl,debug))

        addon_log(debug, 'setRoom:%s' % jsonResultObj)

        dialog = xbmcgui.Dialog()
        if jsonResultObj['status'] == 0:
            dialog.ok("Save result","Wrong room!!")
        else:
            dialog.ok("Save result","Room saved")
            os.system("reboot")



    def serverRequest(self,requestUrl,debug):

        try:
            req = urllib2.Request(requestUrl)
            response = urllib2.urlopen(req)
            if response.geturl() != requestUrl:
                addon_log(debug, 'Redirect URL: %s' % response.geturl())
            jsonData = response.read()

            response.close()
        except urllib2.URLError, e:
            addon_log(debug, 'We failed to open "%s".' % requestUrl)
            if hasattr(e, 'reason'):
                addon_log(debug, 'We failed to reach a server.')
                addon_log(debug, 'Reason: %s' % e.reason)
            if hasattr(e, 'code'):
                addon_log(debug, 'We failed with error code - %s.' % e.code)
            jsonData = None

        except socket.timeout as e:
            addon_log(self._debug, "Timeout error: %r" % e)
            jsonData = None
        addon_log(debug, jsonData)
        return jsonData



    def setLabels(self):
        self.getControl(60003).setLabel(self._mac)
        self.getControl(60005).setLabel(self._ip)
        self.getControl(60007).setText(self._jsonObj["room"])

    def EXIT(self):
        xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
        xbmc.executebuiltin("XBMC.ActivateWindow(Home)")

def main():
    
    
    """Read app settings"""
    setting = xbmcaddon.Addon(id=const.PLUGINNAME)

    scriptDebug = setting.getSetting("debug") == "true"
    
    serverIp = setting.getSetting("serverIp")  # get server domain or ip from the config
    installId = setting.getSetting("installId")  # get installId
    
    mac = getHwAddr("eth0")

    """Open the window create an instance of windowXML"""

    fallBackXmlPath = xbmc.translatePath(__addon__.getAddonInfo('path'))
    addon_log(scriptDebug, 'Fall Back Path %s' % fallBackXmlPath)
    infoRoom = Info('script.quasar.getinfo.main.xml', fallBackXmlPath, _debug=scriptDebug,_serverIp=serverIp,_installId=installId)

    infoRoom.doModal()

    del infoRoom