import wx.adv
import wx
import pkg_resources
import logging

try:
    loc = pkg_resources.resource_filename(__name__, '../../data/')
except NotImplementedError:  # thrown when package is a zip and not an egg folder (py2app)
    loc = './data/'

TOOLTIP_STOPPED = 'ActivityTracker: Stopped'
TOOLTIP_RUNNING = 'ActivityTracker: Running'
ICON_STOPPED = loc + 'idle32x32.png'
ICON_RUNNING = loc + 'tracking32x32.png' 
_LOGGER = logging.getLogger(__name__)


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class ActivityToolbar(wx.adv.TaskBarIcon):

    def __init__(self, frame, target):
        self.frame = frame
        self.target = target
        super(ActivityToolbar, self).__init__()
        self.set_icon(ICON_STOPPED, TOOLTIP_STOPPED)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Show Log', self.on_show_log)
        menu.AppendSeparator()
        create_menu_item(menu, 'Preferences', self.on_show_settings)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, icon_path, tooltip):
        icon = wx.Icon(icon_path)
        self.SetIcon(icon, tooltip)

    def on_show_log(self, event):
        self.target.show_log()

    def on_show_settings(self, event):
        self.target.show_config()

    def on_left_down(self, event):
        if self.target.running:
            self.target.stop()
            self.set_icon(ICON_STOPPED, TOOLTIP_STOPPED)
        else:
            _LOGGER.debug("Starting runner")
            self.target.start()
            self.set_icon(ICON_RUNNING, TOOLTIP_RUNNING)

    def on_exit(self, event):
        if self.target.running:
            _LOGGER.info("Shutting down active runner")
            self.target.stop()
        wx.CallAfter(self.Destroy)
        self.frame.Close()

class ToolbarApp(wx.App):

    def run(self, runner):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        ActivityToolbar(frame, runner)
        self.MainLoop()
