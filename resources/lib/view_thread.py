import sys
import control
import utils
import urllib
import xbmc
import json

class Main:
    def __init__(self):
        params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        self.action = params.get("action", 'board')
        self.board = urllib.unquote_plus(params.get("board", ''))
        self.threadId = int(urllib.unquote_plus(params.get("id", '0')))
        utils.set_no_sort()
        self.browse()
        return

    def browse(self):
        posts = utils.get_thread(self.board, self.threadId)["posts"]

        for p in posts:
            if ('ext' not in p) or ("filename" not in p):
                continue

            if p["ext"] in utils.image_ext:
                thumb = utils.get_thumb_url(self.board, p["tim"])
                img_url = utils.get_image_url(self.board, p["tim"], p["ext"])
                utils.add_image(p['filename'], thumb, img_url)
            else:
                thumb = utils.get_thumb_url(self.board, p["tim"])
                vid_url = utils.get_image_url(self.board, p["tim"], p["ext"])
                utils.add_video(p['filename'], thumb, vid_url)



        utils.add_directory(utils.text_green % control.lang(30502), utils.icon_settings, None,
                            "%s?action=settings" % (sys.argv[0]))

        control.directory_end()
        return
