import xbmc
import xbmcaddon
import xbmcgui

import os
import const
import subprocess
from utils import addon_log


__addon__ = xbmcaddon.Addon(id=const.PLUGINNAME)
__icon__ = __addon__.getAddonInfo('icon')
__lang__ = __addon__.getLocalizedString


class BT_Manager(xbmcgui.WindowXML):


    _lang = const.LANG
    _debug = False
    device_list = None
    device_arr = []
    device_name_arr = []
    selectedMac = -1

    def __init__(self, *args, **kwargs):
        addon_log(self._debug, 'Init')
        xbmcgui.WindowXML.__init__(self)
        selectedMac = -1

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

        devices = self.getPairedDevices()
        self.device_list =  self.getControl(50)
        self.reenderDevices(devices)

    def exit(self):
        addon_log(self._debug, 'Exiting ...')
        self.close()

    def localize(self):
        """
        Localize interface strings
        :return:
        """
        pass
        #self.getControl(60001).setLabel(__lang__(30000))


    def onAction(self, action):

        """When action is performed"""
        buttonCode = action.getButtonCode()
        actionID = action.getId()
        #addon_log(self._debug, "onAction(): control %i" % actionID)
        #addon_log(self._debug, "onAction(): buttonCode %i" % buttonCode)

    def onClick(self, controlID):
        """When control is clicked"""
        #addon_log(self._debug, "onClick(): control %i" % controlID)

        if controlID == 50:
            num = self.device_list.getSelectedPosition()
            #item = self.device_list.getSelectedItem()

            self.selectedMac = self.device_arr[num]
            xbmcgui.Dialog().notification('Bluetooth', 'Hai selezionato %s' % self.device_name_arr[num] , xbmcgui.NOTIFICATION_INFO, 2000)
            addon_log(self._debug, "selected %s " % (self.selectedMac))

        if controlID == 60008: #list refresh
            addon_log(self._debug, "List refresh")
            devices = self.getPairedDevices()
            self.reenderDevices(devices)

        if controlID == 60009: #connect
            addon_log(self._debug, "connect %s " % (self.selectedMac))
            if self.selectedMac != -1:
                self.enablePulseAudio()
                xbmcgui.Dialog().notification('Bluetooth', 'Tentativo di connessione in corso', xbmcgui.NOTIFICATION_INFO, 5000)
                self.command(self.selectedMac,'connect')
            else:
                xbmcgui.Dialog().notification('Bluetooth', 'Seleziona un device dalla lista', xbmcgui.NOTIFICATION_INFO, 3000)


        if controlID == 60010: #disconnect aka unpair/remove
            addon_log(self._debug, "remove %s " % (self.selectedMac))
            if self.selectedMac != -1:
                self.command(self.selectedMac,'remove')
                xbmcgui.Dialog().notification('Bluetooth', 'Eliminazione device in corso', xbmcgui.NOTIFICATION_INFO, 5000)
                self.reenderDevices()
            else:
                xbmcgui.Dialog().notification('Bluetooth', 'Seleziona un device dalla lista', xbmcgui.NOTIFICATION_INFO, 3000)



    def onFocus(self, controlID):
        """On focus change"""
        self._controlId = controlID
        #addon_log(self._debug, "onFocus(): control %i" % controlID)

    def doClose(self):
        """Close  the window and exit"""
        #self.close()
        self.EXIT()

    def EXIT(self):
        xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
        xbmc.executebuiltin("XBMC.ActivateWindow(Home)")


    def reenderDevices(self,devices):
        selectedMac = -1
        listitems = []
        self.device_list.reset()
        self.device_arr = []
        self.device_name_arr = []
        for device in devices:
            mac = device[7:24]
            name = device[25:]
            item = xbmcgui.ListItem()
            item.setLabel(name)
            listitems.append(item)
            self.device_arr.append(mac)
            self.device_name_arr.append(name)
        self.device_list.addItems(listitems)
        xbmcgui.Dialog().notification('Bluetooth', 'Seleziona il device da connettere', xbmcgui.NOTIFICATION_INFO, 3000)

    def getPairedDevices(self):
        process = subprocess.Popen(['/usr/bin/bluetoothctl', 'paired-devices'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        devicesArr = stdout.strip().split('\n')
        process.__del__()
        addon_log(self._debug, devicesArr)
        return devicesArr

    def command(self,mac,command):
        addon_log(self._debug,'command %s %s' % (mac,command))

        process = subprocess.Popen(['/usr/bin/bluetoothctl', command, mac],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()


    def enablePulseAudio(self):
        addon_log(self._debug,'enablePulseAudio')
        process = subprocess.Popen(['/usr/bin/pulseaudio', '--start'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()


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