

import sys
import urllib
import os
import json
import xbmc
import xbmcgui
import xbmcplugin
import control
from BeautifulSoup import SoupStrainer
from BeautifulSoup import BeautifulSoup
import http_request
from datetime import timedelta

# https://github.com/4chan/4chan-API

url_root = "https://a.4cdn.org/"
url_boards = "%s/boards.json"
url_board = "%s%s/%s.json" # url root, board, page
url_thread = "%s%s/thread/%s.json" # url root, board, thread_id

url_thumb = "https://t.4cdn.org/%s/%ss.jpg"
url_image = "https://i.4cdn.org/%s/%s%s"

icon_folder = os.path.join(control.imagesPath, "folder.png")
icon_search = os.path.join(control.imagesPath, "search.png")
icon_next = os.path.join(control.imagesPath, "next-page.png")
icon_settings = os.path.join(control.imagesPath, "settings.png")

image_ext = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]

text_green = "[B][COLOR green][UPPERCASE]%s[/UPPERCASE][/COLOR][/B]"


def add_directory(text, icon, thumbnail, url):
    list_item = xbmcgui.ListItem(text, iconImage=icon, thumbnailImage=thumbnail)
    list_item.setArt({"thumb": thumbnail, "fanart": thumbnail, "landscape": thumbnail, "poster": thumbnail})
    control.addItem(handle=int(sys.argv[1]), url=url, listitem=list_item, isFolder=True)
    return


def add_video(title, thumbnail, video_url):
    list_item = control.item(title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
    list_item.setInfo("video", {"Title": title, "Studio": "4Chan"})
    list_item.setProperty("ListItem.IsResumable", "true")
    list_item.setArt({"thumb": thumbnail, "fanart": thumbnail, "landscape": thumbnail, "poster": thumbnail})
    plugin_play_url = '%s?action=play&video_url=%s' % (sys.argv[0], urllib.quote_plus(video_url))
    control.addItem(handle=int(sys.argv[1]), url=plugin_play_url, listitem=list_item, isFolder=False)


def add_image(title, thumbnail, image_url):
    list_item = control.item(title, iconImage="DefaultImage.png", thumbnailImage=thumbnail)
    list_item.setArt({"thumb": thumbnail})
    # plugin_play_url = '%s?action=view&image_url=%s' % (sys.argv[0], urllib.quote_plus(image_url))
    control.addItem(handle=int(sys.argv[1]), url=image_url, listitem=list_item, isFolder=False)


def add_next_page(item_url, page):
    list_item = control.item(text_green % (control.lang(30500) % page),
                             iconImage=icon_next, thumbnailImage=icon_next)
    control.addItem(handle=int(sys.argv[1]), url=item_url, listitem=list_item, isFolder=True)
    return


def get_boards():
    url = url_boards % url_root

    # ws_board: 0 == adult
    result = http_request.get(url)
    json_obj = json.loads(result)

    return {"boards": json_obj["boards"], "totalResultCount": len(json_obj["boards"]) }


def get_board(board=None, page=1):
    url = url_board % (url_root, board, page)
    result = http_request.get(url)
    json_obj = json.loads(result)

    return {"threads": json_obj["threads"], "totalResultCount": len(json_obj["threads"])}


def get_thread(board=None,thread_id=None):
    url = url_thread % (url_root, board, thread_id)
    result = http_request.get(url)
    json_obj = json.loads(result)

    return {"posts": json_obj["posts"], "totalResultCount": len(json_obj["posts"])}


def get_thumb_url(board, tim):
    return url_thumb % (board, tim)


def get_image_url(board, tim, ext):
    return url_image % (board, tim, ext)


def set_no_sort():
    control.sort(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_NONE)
    return
