

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
    ''' "boards": [{
"board": "3",
"title": "3DCG",
"ws_board": 1,
"per_page": 15,
"pages": 10,
"max_filesize": 4194304,
"max_webm_filesize": 3145728,
"max_comment_chars": 2000,
"max_webm_duration": 120,
"bump_limit": 310,
"image_limit": 150,
"cooldowns": {
"threads": 600,
"replies": 60,
"images": 60
},
"meta_description": "&quot;/3/ - 3DCG&quot; is 4chan's board for 3D modeling and imagery.",
"is_archived": 1
}]'''

    result = http_request.get(url)
    json_obj = json.loads(result)

    return {"boards": json_obj["boards"], "totalResultCount": len(json_obj["boards"]) }


def get_board(board=None, page=1):
    url = url_board % (url_root, board, page)

    # ws_board: 0 == adult
    '''{
"no": 539133,
"now": "10/23/16(Sun)18:56:46",
"name": "Anonymous",
"sub": "Questions That Don&#039;t Deserve Their Own Thread Thread",
"com": "No QTDDTOTT so I thought I&#039;d make one.<br><br>I&#039;m using 2500 samples - why is my image still grainy in the shadows?",
"filename": "JapaneseRoomTestRender_Grain",
"ext": ".jpg",
"w": 1650,
"h": 960,
"tn_w": 250,
"tn_h": 145,
"tim": 1477263406597,
"time": 1477263406,
"md5": "KZclga6TXHSWQTe8R0er2w==",
"fsize": 206622,
"resto": 0,
"bumplimit": 0,
"imagelimit": 0,
"semantic_url": "questions-that-dont-deserve-their-own-thread",
"replies": 113,
"images": 23,
"omitted_posts": 108,
"omitted_images": 23
}'''

    result = http_request.get(url)
    json_obj = json.loads(result)

    return {"threads": json_obj["threads"], "totalResultCount": len(json_obj["threads"])}


def get_thread(board=None,thread_id=None):
    url = url_thread % (url_root, board, thread_id)

    '''
    posts: [{
"no": 712776288,
"now": "11/23/16(Wed)17:27:02",
"name": "Anonymous",
"com": "My girlfriend just told me im too sexual with her and she would like to hang out together more as friends and not concentrate on sex<br><br>I swear she is asexual. <br><br>Am I a dick if i tell her if she wants to hang out as friends, then consider yourself NOT in a relationship with me anymore, since you just want a friendship?<br><br>Cunt",
"filename": "pizza 2",
"ext": ".jpg",
"w": 326,
"h": 326,
"tn_w": 250,
"tn_h": 250,
"tim": 1479940022719,
"time": 1479940022,
"md5": "8V9Ih4iE4si5Q2vZZembJw==",
"fsize": 22876,
"resto": 0,
"bumplimit": 0,
"imagelimit": 0,
"semantic_url": "my-girlfriend-just-told-me-im-too-sexual-with-her",
"replies": 41,
"images": 0,
"unique_ips": 18
},
...
]
    '''
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
