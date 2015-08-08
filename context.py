from devhelper import pykodi
from devhelper.pykodi import log

def main():
    path = pykodi.get_infolabel('ListItem.FolderPath')
    if pykodi.get_conditional('Window.IsVisible(MyVideoNav.xml)'):
        media = 'video'
    elif pykodi.get_conditional('Window.IsVisible(MyMusicNav.xml)') or pykodi.get_conditional('Window.IsVisible(MyMusicSongs.xml)'):
        media = 'music'
    else:
        media = None
        log("Don't know what media type to pass for path '%s'" % path, xbmc.LOGWARNING)

    if media:
        builtin = 'RunScript(script.playrandom, "%s", %s)' % (path, media)
    else:
        builtin = 'RunScript(script.playrandom, "%s")' % path

    pykodi.execute_builtin(builtin)

if __name__ == '__main__':
    main()
