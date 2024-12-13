import os
import sys
import ctypes
import platform
import argparse
import logging
from qtpy import QtWidgets, QtGui, QtCore

from libreflow_launcher.model import Servers, Projects, Settings
from libreflow_launcher.controller import Controller
from libreflow_launcher.view import MainWindow


class SessionApp(QtWidgets.QApplication):

    def __init__(self, argv):
        super(SessionApp, self).__init__(argv)
        self.setApplicationName("Libreflow Launcher")

        self.parse_command_line_args(argv)

        QtGui.QFontDatabase.addApplicationFont(os.path.dirname(__file__)+'/ui/fonts/Asap-VariableFont_wdth,wght.ttf')
        self.setFont(QtGui.QFont('Asap', 9))

        QtCore.QDir.addSearchPath('icons.gui', os.path.dirname(__file__)+'/ui/icons/gui')

        css_file = os.path.dirname(__file__)+'/ui/styles/default/default_style.css'
        with open(css_file, 'r') as r:
            self.setStyleSheet(r.read())
        
        self.stream_formatter = logging.Formatter("%(name)s - %(levelname)s: %(message)s")
        self.logger = logging.getLogger('libreflow_launcher')
        self.logger.setLevel(logging.INFO)

        self.default_log_handler = logging.StreamHandler(sys.stdout)
        self.default_log_handler.setFormatter(self.stream_formatter)
        self.logger.addHandler(self.default_log_handler)

        # Connect everything together
        self.servers_model = Servers(self)
        self.projects_model = Projects(self)
        self.settings_model = Settings(self)

        self.ctrl = Controller(
            self, self.servers_model, self.projects_model, self.settings_model
        )
        self.view = MainWindow(self.ctrl)
        
        self.view.show()
    
    def parse_command_line_args(self, args):
        parser = argparse.ArgumentParser(
            description='Libreflow Launcher Arguments'
        )

        parser.add_argument(
            '-S', '--site', dest='site', help='Site Name to use'
        )

        values, _ = parser.parse_known_args(args)

        if values.site:
            os.environ['LF_LAUNCHER_SITE_NAME'] = values.site

    def log(self, context, *words):
        self._log(logging.INFO, ' '.join([str(i) for i in words]), extra={'context': context})

    def log_info(self, message, *args, **kwargs):
        self._log(logging.INFO, message, *args, **kwargs)

    def log_debug(self, message, *args, **kwargs):
        self._log(logging.DEBUG, message, *args, **kwargs)

    def log_error(self, message, *args, **kwargs):
        self._log(logging.ERROR, message, *args, **kwargs)

    def log_warning(self, message, *args, **kwargs):
        self._log(logging.WARNING, message, *args, **kwargs)

    def log_critical(self, message, *args, **kwargs):
        self._log(logging.CRITICAL, message, *args, **kwargs)

    def _log(self, level, message, *args, **kwargs):
        self.logger.log(level, message, *args, **kwargs)


if __name__ == '__main__':
    if platform.system() == "Windows":
        myappid = 'lfscoop.libreflow_launcher'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    app = SessionApp(sys.argv)
    sys.exit(app.exec_())