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
            builtin += ', logToGui'
        builtin += ')'
        xbmc.executebuiltin(builtin.encode('utf-8'))
    else:
        xbmc.log('[%s] %s' % (__addonid__, message.encode('utf-8')), level)


def main():
    path = xbmc.getInfoLabel("ListItem.FolderPath").decode("utf-8")
    if xbmc.getCondVisibility('Window.IsVisible(MyVideoNav.xml)'):
        media = 'video'
    elif xbmc.getCondVisibility('Window.IsVisible(MyMusicNav.xml)') or xbmc.getCondVisibility('Window.IsVisible(MyMusicSongs.xml)'):
        media = 'music'
    else:
        media = None
        log("Don't know what media type to pass for path '%s'" % path)

    if media:
        builtin = 'RunScript(script.playrandom, "%s", %s)' % (path, media)
    else:
        builtin = 'RunScript(script.playrandom, "%s")' % path
    xbmc.executebuiltin(builtin.encode('utf-8'))


if __name__ == '__main__':
    main()
