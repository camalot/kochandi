import sys
import control
import utils
import urllib
import json
import xbmc


class Main:
    def __init__(self):
        params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        self.action = params.get("action", 'board')
        self.board = urllib.unquote_plus(params.get("board", ''))
        self.page = int(urllib.unquote_plus(params.get("page", '1')))
        self.totalPages = int(urllib.unquote_plus((params.get("total_pages", '10'))))
        utils.set_no_sort()
        self.browse()
        return

    def browse(self):
        threads = utils.get_board(self.board, self.page)["threads"]
        for t in threads:
            post = t["posts"][0]
            if int(post["images"]) <= 0:
                continue

            if hasattr(post, "sub"):
                title = "%s | images: %s" % (post["sub"], post["images"])
            elif hasattr(post, "com"):
                title = "%s | images:  %s" % (post["com"], post["images"])
            else:
                title = "%s | images: %s" % (post["filename"], post["images"])
            icon = utils.get_thumb_url(self.board, post["tim"])
            utils.add_directory(title, icon, icon,
                                "%s?action=thread&board=%s&id=%s" % (sys.argv[0], urllib.quote_plus(self.board),
                                                                     post["no"]))

        if self.page < self.totalPages:
            next_page = self.page + 1
            utils.add_next_page("%s?action=%s&page=%s&total_pages=%s&board=%s" % (sys.argv[0], self.action,
                                                                                  next_page, self.totalPages,
                                                                                  self.board), next_page)
        control.directory_end()
        return
