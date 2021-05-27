import const
import xbmc
import xbmcaddon
import platform


from traceback import format_exc, print_exc



def addon_log(debug,string):
    if debug:
        addon = xbmcaddon.Addon(id=const.PLUGINNAME)   
        addon_version = addon.getAddonInfo('version')
        try:
            if not isinstance(string, str):
                string = str(string)
            msg = string.decode("utf-8", 'ignore')
            xbmc.log("[%s-%s]: %s "  %(const.PLUGINNAME,addon_version, msg.encode('utf-8', 'ignore')), level=xbmc.LOGNOTICE)
        except:
            print_exc() 

def localise(stringId):
    __addon__ = xbmcaddon.Addon(id=const.PLUGINNAME)
    string = __addon__.getLocalizedString(stringId).encode( 'utf-8', 'ignore' )
    return string    