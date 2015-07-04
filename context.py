import xbmc
import xbmcaddon
import xbmcvfs

__addon__ = xbmcaddon.Addon()
__addonid__ = __addon__.getAddonInfo('id')

try:
    # import visuallogger
    # logger = visuallogger.Logger()
    xbmcaddon.Addon('script.design.helper')
    loggerInstalled = True
except:
    # logger = None
    loggerInstalled = False


def log(message, log_to_gui=True, level=xbmc.LOGDEBUG):
    if loggerInstalled:
        # Yeah, this is ugly, so def want it to be a module
        builtin = 'RunScript(script.design.helper, log, %s, "%s"' % (__addonid__, message)
        if log_to_gui:
            builtin += ', log_to_gui'
        builtin += ')'
        xbmc.executebuiltin(builtin.encode('utf-8'))
    else:
        xbmc.log('[%s] %s' % (__addonid__, message.encode('utf-8')), level)


def main():
    full_url = xbmc.getInfoLabel("ListItem.FolderPath").decode("utf-8")
    builtin = 'RunScript(script.playrandom, "%s")' % full_url
    xbmc.executebuiltin(builtin.encode('utf-8'))


if __name__ == '__main__':
    main()
