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
            


def getHwAddr(ifname):
 
    addon_log("pinger",platform.system())
    import fcntl, socket, struct
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]

def get_ip_address(ifname):
    import fcntl, socket, struct
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915, struct.pack('256s', ifname[:15]))[20:24])



def localise(stringId):
    __addon__ = xbmcaddon.Addon(id=const.PLUGINNAME)
    string = __addon__.getLocalizedString(stringId).encode( 'utf-8', 'ignore' )
    return string    