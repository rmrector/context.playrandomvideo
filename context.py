# examples of URLs I need to handle
# videodb://movies/titles/6748
# videodb://movies/genres/
# videodb://movies/directors/
# videodb://movies/directors/9788/
# smb://CUBER/Other/Apps/
# special://profile/playlists/video/Buffy.xsp
# videodb://tvshows/titles/1396/?xsp={"order":{"direction":"ascending","ignorefolders":0,"method":"sorttitle"},"type":"tvshows"}
# library://video_flat/inprogressshows.xml/
# library://video_flat/recentlyaddedmovies.xml/
# library://video_flat/recentlyaddedepisodes.xml/
# videodb://tvshows/titles/1480/2/?tvshowid=1480&xsp={"order":{"direction":"ascending","ignorefolders":0,"method":"sorttitle"},"type":"tvshows"}
# videodb://tvshows/titles/1580/?filter={"rules":{"and":[{"field":"rating","operator":"between","value":["9.5","10"]}]},"type":"tvshows"}&xsp={"order":{"direction":"ascending","ignorefolders":0,"method":"sorttitle"},"type":"tvshows"}

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
__cwd__ = __addon__.getAddonInfo('path').decode("utf-8")
__resource__ = xbmc.translatePath(os.path.join(__cwd__, 'resources', 'lib')).decode("utf-8")

sys.path.append(__resource__)

import logger

LIMIT = 100
tvshowTitlesPath = "videodb://tvshows/titles/" # Frig. This can also not end with a slash /

def randomList(path):
    logger.debug("Found path: " + path)
    return

    playlistExtension = ".xsp"
    if (path.startswith(tvshowTitlesPath)):
        playTvShow(path)
    elif(path.endswith(playlistExtension)):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        playlistLoaded = False

        playlistXml = xbmcvfs.File(path, 'r')
        playlistXml = playlistXml.read()
        playlistXml = ET.fromstring(playlistXml)
        if playlistXml.tag == 'smartplaylist' and 'type' in playlistXml.attrib:
            if playlistXml.attrib['type'] == 'episodes':
                episodeIds = xbmcvfs.listdir(path)[1]
                for episodeId in episodeIds:
                    jsonRequest = {"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodeDetails", "id": 1}
                    jsonRequest["params"] = {"episodeid": int(episodeId), "properties": ["file"]}
                    episode = json.loads(xbmc.executeJSONRPC(json.dumps(jsonRequest)))
                    episode = episode["result"]["episodedetails"]
                    listItem = xbmcgui.ListItem(episode["label"])
                    playlist.add(episode["file"], listItem)
                    print episode["label"]
                playlistLoaded = True
            else:
                debugMessage = "[context.playrandom] Unsupported playlist! '%s'" % path
        else:
            debugMessage = "[context.playrandom] Unsupported playlist! '%s'" % path

        if playlistLoaded:
            playlist.shuffle()
            debugMessage = "[context.playrandom] Successfully random'd '%s'" % path
            xbmc.Player().play(playlist)
    else:
        debugMessage = "[context.playrandom] Unsupported path! %s" % path

def playTvShow(path):
    originalPath = path
    path = path[len(tvshowTitlesPath):].split('?')[0].split('/')

    tvshowId = path[0]
    season = path[1] if len(path) > 1 else None

    jsonRequest = {"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "id": 1}
    jsonRequest["params"] = {"properties": ["file"], "sort": {"method": "random"}, "limits": {"end": LIMIT}}

    if tvshowId:
        jsonRequest["params"]["tvshowid"] = int(tvshowId)
    if season:
        jsonRequest["params"]["season"] = int(season)

    jsonEpisodes = xbmc.executeJSONRPC(json.dumps(jsonRequest))
    jsonEpisodes = json.loads(jsonEpisodes)

    if len(jsonEpisodes["result"]["episodes"]):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        for episode in jsonEpisodes["result"]["episodes"]:
            listItem = xbmcgui.ListItem(episode["label"])
            playlist.add(episode["file"], listItem)

        xbmc.Player().play(playlist)
        debugMessage = "[context.playrandom] Successfully random'd '%s'" % originalPath
    else:
        debugMessage = "[context.playrandom] Couldn't find any episodes to random"

def main():
    randomList(urllib.unquote(xbmc.getInfoLabel("ListItem.FolderPath").decode("utf-8")))

if __name__ == '__main__':
    main()
