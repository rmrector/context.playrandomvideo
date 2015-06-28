# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Philipp Temminghoff
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

import xbmc
import xbmcgui
import json

def main():
    if xbmc.getCondVisibility("Container.Content(tvshows)"):
        tvshowid = xbmc.getInfoLabel("ListItem.DBID")
        
        rawJsonEpisodes = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"tvshowid": %s, "properties": ["file", "episode", "season", "plot"], "sort": {"method": "random"}, "limits": {"end": 20}}, "id": 1}' % tvshowid)
        jsonEpisodes = json.loads(rawJsonEpisodes)
        
        print rawJsonEpisodes
        
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        for episode in jsonEpisodes["result"]["episodes"]:
            listItem = xbmcgui.ListItem(episode["label"])
            playlist.add(episode["file"], listItem)
        
        episodeCount = jsonEpisodes["result"]["limits"]["total"]
        
        message = "TV Show: %s (%s)" % (tvshowid, episodeCount)
        
        xbmc.Player().play(playlist)
    else:
        path = urllib.unquote(xbmc.getInfoLabel("ListItem.FolderPath"))
        message = "Unsupported path!: %s" % path
        
    xbmc.executebuiltin("Skin.SetString(debug.message, \"%s\")" % message)
    xbmc.log("RECTOR: %s" % message)
    
    return
    if xbmc.getCondVisibility("Container.Content(movies)"):
        xbmc.executebuiltin("RunScript(script.extendedinfo,info=extendedinfo,dbid=%s,id=%s)" % (xbmc.getInfoLabel("ListItem.DBID"), xbmc.getInfoLabel("ListItem.Property(id)")))
    elif xbmc.getCondVisibility("Container.Content(tvshows)"):
        xbmc.executebuiltin("RunScript(script.extendedinfo,info=extendedtvinfo,dbid=%s,id=%s)" % (xbmc.getInfoLabel("ListItem.DBID"), xbmc.getInfoLabel("ListItem.Property(id)")))
    elif xbmc.getCondVisibility("Container.Content(seasons)"):
        xbmc.executebuiltin("RunScript(script.extendedinfo,info=seasoninfo,tvshow=%s,season=%s)" % (xbmc.getInfoLabel("ListItem.TVShowTitle"), xbmc.getInfoLabel("ListItem.Season")))
    elif xbmc.getCondVisibility("Container.Content(actors) | Container.Content(directors)"):
        xbmc.executebuiltin("RunScript(script.extendedinfo,info=extendedactorinfo,name=%s)" % (xbmc.getInfoLabel("ListItem.Label")))

if __name__ == '__main__':
    main()
