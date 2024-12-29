import sublime
import sublime_plugin
from os import path


class MdOpenerCommand(sublime_plugin.WindowCommand):

    def run(self):
        theView = self.window.active_view()
        selection = theView.sel()[0] # just use the most recent cursor
        text = theView.substr(selection)

        #normalize a and b with begin and end
        start = selection.begin()
        end = selection.end()
        selection.a = start
        selection.b = end

        while not text.startswith("[") and "\n" not in text:
            selection.a -= 1
            text = theView.substr(selection)
            if selection.a < 0 or len(text) > 300:
                break

        if text.startswith("["):
            while not text.endswith(")") and "\n" not in text:
                selection.b += 1
                text = theView.substr(selection)
                if len(text) > 300:
                    break

        text = text.rstrip()

        #if it matches markdown link format - get it
        if text.startswith("[") and text.endswith(")") and "](" in text:
            pieces = text.split("](")
            link = pieces[1]
            link = link.rstrip(")")
            #only try to open it if it is a relative link
            if not link.startswith("https://") and not link.startswith("http://"):
                self.window.open_file(link)