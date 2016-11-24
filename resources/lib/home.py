import sys
import control
import utils
import urllib
import xbmc

class Main:
    def __init__(self):
        utils.set_no_sort()

        utils.add_directory(utils.text_green % control.lang(30502), utils.icon_settings, None,
                            "%s?action=settings" % (sys.argv[0]))

        boards = utils.get_boards()["boards"]
        nsfw = control.setting("enable_nsfw") == 'true'
        for b in boards:
            if not nsfw and (b["ws_board"] == 0):
                continue
            title = "/%s/ (%s)" % (b["board"], b["title"])
            utils.add_directory(title, None, None,
                                "%s?action=board&board=%s&total_pages=%s" % (sys.argv[0],
                                                                             urllib.quote_plus(b["board"]),
                                                                             b["pages"]))

        control.directory_end()
        return
