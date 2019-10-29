import rumps
import logging

_LOGGER = logging.getLogger(__name__)


class ActivityToolbar(rumps.App):

    def __init__(self, *args, **kwargs):
        self.target = None
        super(ActivityToolbar, self).__init__(*args, **kwargs)

    @rumps.clicked("Start tracking")
    def onoff(self, sender):
        _LOGGER.debug("Target state running: %s", self.target.running)
        if self.target.running:
            self.target.stop()
            self.title = "Idle"
            sender.title = "Start"
        else:
            _LOGGER.debug("Starting runner")
            self.target.start()
            self.title = "Tracking"
            sender.title = "Stop"

    @rumps.clicked("Show log")
    def show_log(self, _):
        self.target.show_log()

    @rumps.clicked("Quit")
    def quit(self, _):
        _LOGGER.debug("Quit triggered")
        if self.target.running:
            _LOGGER.info("Shutting down active runner")
            self.target.stop()
        _LOGGER.info("Quit application")
        rumps.quit_application()

class ToolbarApp:

    def __init__(self):
        self.tb = ActivityToolbar("Idle", quit_button=None)

    def run(self, runner):
        self.tb.target = runner
        self.tb.run()
