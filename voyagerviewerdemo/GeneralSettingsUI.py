import logging

from PyQt5 import QtWidgets

from voyagerviewerdemo.uic.general_settings_uic import Ui_GeneralSettingsDialog

class GeneralSettingsDialog(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        self.ui = Ui_GeneralSettingsDialog()
        self.ui.setupUi(self)

    def run(self, settings):

        self.ui.autoconnect_on_start.setChecked(settings.autoconnect)
        self.ui.nosplash.setChecked(settings.nosplash)

        result = self.exec_()

        if result:
            settings.nosplash = self.ui.nosplash.isChecked()
            settings.autoconnect = self.ui.autoconnect_on_start.isChecked()

            logging.info(f'{settings._config}')

            settings.write()

        logging.info('General settings wrote out')
