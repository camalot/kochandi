import sys
import control
import utils
import urllib
import json
import xbmc
import xbmcgui
from player import player


class Main:
    def __init__(self):
        params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        self.image_url = urllib.unquote_plus(params["image_url"])
        self.view_image()
        return


    def view_image(self):

        title = unicode(xbmc.getInfoLabel("ListItem.Title"), "utf-8")
        thumbnail = xbmc.getInfoImage("ListItem.Thumb")

        dialog_wait = xbmcgui.DialogProgress()
        dialog_wait.create(control.lang(30504), title)

        if self.image_url is None:
            # Close wait dialog...
            dialog_wait.close()
            del dialog_wait

            # Message...
            xbmcgui.Dialog().ok(control.lang(30000), control.lang(30505))
            return

        dialog_wait.close()
        del dialog_wait
        xbmc.log(self.image_url)
        player().view({"url": self.image_url, "thumb": thumbnail, "title": title})
        return
