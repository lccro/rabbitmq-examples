import sys
from typing import Optional

import cv2.cv2
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk, GLib, GdkPixbuf


@Gtk.Template.from_file('main.glade')
class MainWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'MainWindow'

    image: Gtk.Image = Gtk.Template.Child()
    dlg_about: Gtk.AboutDialog = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dlg_about.connect('delete-event', lambda d, r: d.hide_on_delete())

    def menu_about(self, *args):
        self.dlg_about.present()

    def do_delete_event(self, *args, **kwargs):
        cap.release()


class Application(Gtk.Application):
    window: Optional[Gtk.ApplicationWindow] = None

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            application_id='ai.cyberlabs.cyber.MQ',
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
            **kwargs)

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", lambda a, p: self.window.menu_about())
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", lambda a, p: self.quit())
        self.add_action(action)

    def do_activate(self):
        if not self.window:
            self.window = MainWindow(application=self, title="Cyberama OpenCV")
        self.window.present()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        # convert GVariantDict -> GVariant -> dict
        _options = options.end().unpack()

        self.activate()
        return 0


def show_frame():
    global app
    if app is None:
        return True
    if not cap.isOpened():
        return False

    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    if greyscale:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    pb = GdkPixbuf.Pixbuf.new_from_data(frame.tobytes(),
                                        GdkPixbuf.Colorspace.RGB,
                                        False,
                                        8,
                                        frame.shape[1],
                                        frame.shape[0],
                                        frame.shape[2] * frame.shape[1])
    app.window.image.set_from_pixbuf(pb.copy())
    return True


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)
    greyscale = False

    app = Application()
    GLib.idle_add(show_frame)
    app.run(sys.argv)
