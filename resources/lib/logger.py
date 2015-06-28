import sys
import xbmc

watch_addon_filter = ['context.playrandom', None]

try:
    addonId = sys.modules['__main__'].__addonid__
except:
    addonId = None

def debug(message):
    displayId = addonId if addonId else 'unknown'
    message = '[%s] %s' % (displayId, message)
    xbmc.log(message.encode("utf-8"))

    if addonId not in watch_addon_filter:
        return

    fullDebugLog = xbmc.getInfoLabel('Window(50).Property(debug.message)')
    if fullDebugLog:
        fullDebugLog = fullDebugLog.split('[CR]')

        if len(fullDebugLog) > 19:
            fullDebugLog = fullDebugLog[-19:]

        fullDebugLog.append(message)

        fullDebugLog = '[CR]'.join(fullDebugLog)
    else:
        fullDebugLog = message

    xbmc.executebuiltin('SetProperty(debug.message, "%s", 50)' % fullDebugLog.encode("utf-8"))
