#!/usr/bin/env python3
#
# voyager_view_main
#
# Copyright 2019 Michael Fulbright <mike.fulbright@pobox.com>
#
import os
import sys
import logging

# needed when we run out of a directory and haven't installed as a pacakge
# under anaconda
sys.path.append('..')

import numpy as np

from PyQt5 import QtCore, QtWidgets, QtGui

from voyagerviewerdemo.ImageWindowSTF import ImageWindowSTF
from voyagerviewerdemo.ImageAreaInfo import ImageAreaInfo
from voyagerviewerdemo.ProgramSettings import ProgramSettings
from voyagerviewerdemo.VoyagerClient import VoyagerClient

import voyagerviewerdemo.uic.icons

# FIXME Need better VERSION system
# this has to match yaml
import importlib

# see if we injected a version at conda build time
if importlib.util.find_spec('voyagerviewerdemo.build_version'):
    from ..voyagerviewer.build_version import VERSION
else:
    VERSION='0.1'

class MainWindow(QtGui.QMainWindow):
    class ImageDocument:
        """Represents a loaded image and any analysis/metadata
        """

        def __init__(self):
            """
            filename : str
                Filename for image file
            image_data : numpy 2D array
                Image data
            image_width : ImageWindowSTF
                Widget containing the image display
            """
            self.filename = None
            self.median = None
            self.image_data = None
            self.image_widget = None
            self.fits = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('voyagerviewerdemo v' + VERSION)

        vlayout = QtGui.QVBoxLayout()
        vlayout.setSpacing(0)
        vlayout.setContentsMargins(0, 0, 0, 0)

        container = QtGui.QWidget()
        container.setLayout(vlayout)
        self.setCentralWidget(container)

        self.create_menu_and_toolbars()

        self.status = QtGui.QStatusBar()
        self.setStatusBar(self.status)

        self.image_area_ui = ImageAreaInfo()
        vlayout.addWidget(self.image_area_ui)
        self.image_area_ui.view_changed.connect(self.current_view_changed)

        # dict of all ImageDocuments for all loaded images
        # indexed by the tab index for the image view
        self.image_documents = {}

        self.resize(800, 600)
        self.show()

        # program settings
        self.settings = ProgramSettings()
        self.settings.read()

        # connect to Voyager
        self.voyager_client = VoyagerClient()
        self.voyager_client.signals.new_fit_ready.connect(self.new_fit_image)
        self.voyager_client.signals.disconnected.connect(self.voyager_disconnected)
        self.voyager_client.signals.connect_close.connect(self.voyager_connection_closed)
        #self.voyager_client.signals.tcperror.connect(self.tcperror)

        QtCore.QTimer.singleShot(1000, self.show_welcome_screen)

    def create_menu_and_toolbars(self):
        main_toolbar = QtGui.QToolBar('File')
        main_toolbar.setIconSize(QtCore.QSize(16, 16))
        self.addToolBar(main_toolbar)

        file_menu = self.menuBar().addMenu("&File")
#
        open_file_action = QtGui.QAction(QtGui.QIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogOpenButton'))), "&Open file...", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        main_toolbar.addAction(open_file_action)

        exit_action = QtGui.QAction(QtGui.QIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogCancelButton'))), "&Exit", self)
        exit_action.triggered.connect(QtGui.QApplication.quit)
        file_menu.addAction(exit_action)

        tool_menu = self.menuBar().addMenu('&Tools')

        settings_action = QtGui.QAction(QtGui.QIcon(':/gear.png'), 'Settings', self)
        settings_action.triggered.connect(self.edit_settings)
        tool_menu.addAction(settings_action)
        main_toolbar.addAction(settings_action)

        self.connect_action = QtGui.QAction('Connect', self)
        self.connect_action.setCheckable(True)
        tool_menu.addAction(self.connect_action)
        main_toolbar.addAction(self.connect_action)
        self.connect_action.toggled.connect(self.toggle_connect)

        # Not currently used
        #help_menu = self.menuBar().addMenu('&Help')

    def show_welcome_screen(self):
        QtWidgets.QMessageBox.information(None,
                                      'Welcome',
                                      'This is a preview version of VoyagerViewerDemo. '
                                      'You may use or distribute this software for free '
                                      'at your own discretion '
                                      'and risk with no warranty and with no stated '
                                      'or implied suitablility '
                                      'for any application.\n\n',
                                      QtWidgets.QMessageBox.Ok)
        return

    def toggle_connect(self, state):
        logging.info(f'toggle_connect: state = {state}')
        if state:
            if self.voyager_client.is_connected():
                logging.info('Already connected but received connect event - ignoring!')
                return

            logging.info('Attempting to connect')
            rc = self.voyager_client.connect()
            if rc:
                self.status.showMessage('Voyager connected!')
            else:
                self.status.showMessage('Unable to connect to Voyager!')
        else:
            if not self.voyager_client.is_connected():
                logging.info('Already disconnected but received disconnect event - ignoring!')
                return

            logging.info('Attempting to disconnect')
            rc = self.voyager_client.disconnect()
            if rc:
                self.status.showMessage('Voyager disconnected!')
            else:
                self.status.showMessage('Unable to disconnect to Voyager!')

        self.set_connectdisconnect_state(self.voyager_client.is_connected())

    def set_connectdisconnect_state(self, state):
        self.connect_action.setChecked(state)

        if state:
            self.connect_action.setText('Disconnect')
        else:
            self.connect_action.setText('Connect')

    def voyager_disconnected(self):
        logging.info('Received Voyager disconnected signal')
        self.status.showMessage('Voyager disconnected!')
        self.set_connectdisconnect_state(self.voyager_client.is_connected())

    def voyager_connection_closed(self):
        logging.info('Received Voyager connect_closed signal')
        self.status.showMessage('Voyager connection closed!')
        self.set_connectdisconnect_state(self.voyager_client.is_connected())

    def image_mouse_move(self, x, y, val):
        #self.status.showMessage(f'({int(x)}, {int(y)}) : {val}')
        self.image_area_ui.update_xy_value_info(x, y, val)

    def image_mouse_click(self, ev):
        logging.info(f'image_mouse_click: {ev.pos()}, {ev.button()}')

    def current_view_changed(self, index):
        self.image_area_ui.clear_info()
        current_widget = self.image_area_ui.get_current_view_widget()
        if self.image_documents:
            self.image_area_ui.update_info(self.image_documents[current_widget])

    def edit_settings(self):
        return
#        dlg = GeneralSettingsDialog()
#        dlg.run(self.settings)

    def new_fit_image(self, result):
        logging.info(f'new_fit_image: {result}')

        filename, filetype = result

        # HACK strip off type of image from front of filename
        #
        # 3 possibilities
        #
        # 'TestShot'    - this is an image from the 'OnTheFly' capture frame button
        # 'SyncVoyager' - frame taken when Voyager is doing a plate solve operation
        # Other         - frames from a sequence will start with the 'Target' name
        #
        # We will display the latest of each possibility in a tab of its own
        s = os.path.basename(filename).split('_')
        image_type = s[0]
        if image_type != 'TestShot' and image_type != 'SyncVoyager':
            image_type = 'Other'

        # Try to reuse existing tab if possible
        image_widget = self.image_area_ui.find_view_widget(image_type)

        if image_widget is None:
            # create new image widget and put it in a tab
            image_widget = ImageWindowSTF()
            image_widget.image_mouse_move.connect(self.image_mouse_move)
            image_widget.image_mouse_click.connect(self.image_mouse_click)
            tab_index = self.image_area_ui.add_view(image_widget, image_type)
        else:
            # found an existing tab
            tab_index = self.image_area_ui.find_index_widget(image_widget)

        # display the image data
        if not image_widget.show_image(filename):
            QtWidgets.QMessageBox.critical(None,
                                           'Error', 'Unable to load FITS File.'
                                           ' Note color FITS not supported.',
                                           QtWidgets.QMessageBox.Ok)
            return

        # create a document descriptor for new data
        newdoc = self.ImageDocument()
        newdoc.filename = image_type
        newdoc.image_widget = image_widget
        newdoc.image_data = image_widget.image_data
        newdoc.median = np.median(newdoc.image_data)

        # store new image descriptor in image index
        self.image_documents[image_widget] = newdoc
        self.image_area_ui.set_current_view_index(tab_index)

        # make unclosable
        self.image_area_ui.set_view_unclosable(tab_index)
        self.image_area_ui.clear_info()

        self.image_area_ui.update_info(newdoc)

        # set tooltip on 'Other' tab to show long filename
        if image_type == 'Other':
            self.image_area_ui.set_view_tooltip_by_index(tab_index, filename)
            self.status.showMessage(f'{filename} loaded!')

    def file_open(self):
        logging.info('file_open')
        #self.image_filename = '../tmp/test3.fits'

        filename, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Open Image', '', 'FITS (*.fit *.fits, *.fts)')

        logging.info(f'file_open: {filename}')

        if len(filename) < 1:
            return

        # FIXME duplicated in new_camera_image!!

        # create new image widget and put it in a tab
        image_widget = ImageWindowSTF()
        image_widget.image_mouse_move.connect(self.image_mouse_move)
        image_widget.image_mouse_click.connect(self.image_mouse_click)

        if not image_widget.show_image(filename):
            QtWidgets.QMessageBox.critical(None,
                                           'Error', 'Unable to load FITS File.'
                                           ' Note color FITS not supported.',
                                           QtWidgets.QMessageBox.Ok)
            return

        tab_index = self.image_area_ui.add_view(image_widget, os.path.basename(filename))

        newdoc = self.ImageDocument()
        newdoc.filename = filename
        newdoc.image_widget = image_widget
        newdoc.image_data = image_widget.image_data
        newdoc.median = np.median(newdoc.image_data)

        self.image_documents[image_widget] = newdoc
        self.image_area_ui.set_current_view_index(tab_index)
        self.image_area_ui.clear_info()
        self.image_area_ui.update_info(newdoc)

    # this is truncated version of handle_new_image() that DOES NOT
    # add all the FITS headers - it just finds the proper tab
    # and loads the image there
    def find_tab_for_new_image(self, tab_name, fits_doc):
        logging.info('find_tab_for_new_image: START')


        tab_widget = self.image_area_ui.find_view_widget(tab_name)

        if tab_widget is None:
            # create new image widget and put it in a tab
            image_widget = ImageWindowSTF()
            image_widget.image_mouse_move.connect(self.image_mouse_move)
            image_widget.image_mouse_click.connect(self.image_mouse_click)

            tab_index = self.image_area_ui.add_view(image_widget, tab_name)

            imgdoc = self.ImageDocument()
            #imgdoc.filename = 'Camera'
            imgdoc.image_widget = image_widget

            self.image_documents[image_widget] = imgdoc
        else:
            # reuse old
            imgdoc = self.image_documents[tab_widget]

            tab_index = self.image_area_ui.find_index_widget(tab_widget)

            logging.info(f'reuse tab_index = {tab_index}')

            # FIXME REALLY need a way to refresh/reset attributes!!
            # this attr is added in ImageAreaInfo class in update_info()
            # need a better way to associate statistics with an image
            if hasattr(imgdoc, 'perc01'):
                delattr(imgdoc, 'perc01')
            if hasattr(imgdoc, 'perc99'):
                delattr(imgdoc, 'perc99')

        # FIXME repurposing fits image data this way doesn't seem like a good idea
        # but the hope is we don't store it twice
        # might be better to just make fits_image the expected image format
        # and have method to expose raw image data than using an attribute
        imgdoc.fits = fits_doc
        imgdoc.image_data = fits_doc.image_data()
        imgdoc.median = np.median(imgdoc.image_data)

#        logging.info(f'{imgdoc.image_data.shape}  {fits_doc.image_data().shape}')

        imgdoc.image_widget.show_data(imgdoc.image_data)

        logging.info('find_tab_for_new_image: DONE')

        return (imgdoc, tab_index)


# FOR DEBUGGING - enable setstyle in main below it will draw red boxes around elements
class DiagnosticStyle(QtWidgets.QProxyStyle):
    def drawControl(*args): #element, option, painter, widget):
        logging.info(f'{len(args)} f{args}')
#        if len(args) != 4:
#            return
        element, tmpint, option, painter, widget = args
        if widget and painter:
            # draw a border around the widget
            painter.setPen(QtGui.QColor("red"))
            painter.drawRect(widget.rect())

            # show the classname of the widget
            translucentBrush = QtGui.QBrush(QtGui.QColor(255, 246, 240, 100))
            painter.fillRect(widget.rect(), translucentBrush)
            painter.setPen(QtGui.QColor("darkblue"))
            painter.drawText(widget.rect(), QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, widget.metaObject().className())

def create_log_directory():
    # find location
    log_dir = os.path.expandvars('%LOCALAPPDATA%\VoyagerViewerDemo')
    if os.path.isdir(log_dir):
        return log_dir

    # try to create if missing
    print(f'Creating log directory {log_dir}')
    try:
        os.makedirs(log_dir)
    except Exception as e:
        print(f'Exception creating log directory {log_dir}!', exc_info=True)
        return None

    return log_dir

def main_app():
    global app

    app = QtGui.QApplication(sys.argv)

    mainwin = MainWindow()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        #QtGui.QApplication.instance().exec_()
       app.exec()


if __name__ == '__main__':
    log_dir = create_log_directory()
    print(log_dir)
    if log_dir is not None:
        logging.basicConfig(filename=os.path.join(log_dir, 'voyagerviewerdemo.log'),
                            filemode='w',
                            level=logging.INFO,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

    # add to screen as well
    log = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    logging.info(f'voyagerviewerdemo {VERSION} starting')

    main_app()

    logging.error("DONE")
