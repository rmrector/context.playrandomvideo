import json
import os
import urllib
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

import xml.etree.ElementTree as ET

__addon__ = xbmcaddon.Addon()
__addonid__ = __addon__.getAddonInfo('id')

try:
    # import visuallogger
    # logger = visuallogger.Logger()
    xbmcaddon.Addon('script.design.helper')
    loggerInstalled = True
except ExplicitException:
    # logger = None
    loggerInstalled = False


def log(message, logToGui=True, level=xbmc.LOGDEBUG):
    if loggerInstalled:
        # Yeah, this is ugly, so def want it to be a module
        builtin = "RunScript(script.design.helper, log, %s, \"%s\"" % (__addonid__, message)
        if logToGui:
            builtin += ', logToGui'
        builtin += ')'
        xbmc.executebuiltin(builtin)
    else:
        xbmc.log('[%s] %s' % (__addonid__, message), level)


def main():
    folderPath = urllib.unquote(xbmc.getInfoLabel("ListItem.FolderPath").decode("utf-8"))
    # randomPlayer.playRandomFromFolderPath(folderPath)
    builtin = 'RunScript(script.playrandom, "%s")' % folderPath
    xbmc.executebuiltin(builtin)


if __name__ == '__main__':
    main()
