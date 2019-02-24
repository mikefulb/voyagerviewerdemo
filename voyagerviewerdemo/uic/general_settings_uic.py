# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'general_settings.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GeneralSettingsDialog(object):
    def setupUi(self, GeneralSettingsDialog):
        GeneralSettingsDialog.setObjectName("GeneralSettingsDialog")
        GeneralSettingsDialog.resize(252, 132)
        self.verticalLayout = QtWidgets.QVBoxLayout(GeneralSettingsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_3 = QtWidgets.QGroupBox(GeneralSettingsDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QtCore.QSize(0, 75))
        self.groupBox_3.setObjectName("groupBox_3")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox_3)
        self.formLayout.setObjectName("formLayout")
        self.autoconnect_on_start = QtWidgets.QCheckBox(self.groupBox_3)
        self.autoconnect_on_start.setObjectName("autoconnect_on_start")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.autoconnect_on_start)
        self.nosplash = QtWidgets.QCheckBox(self.groupBox_3)
        self.nosplash.setObjectName("nosplash")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.nosplash)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(GeneralSettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_5.addWidget(self.buttonBox)
        self.horizontalLayout_5.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.retranslateUi(GeneralSettingsDialog)
        self.buttonBox.accepted.connect(GeneralSettingsDialog.accept)
        self.buttonBox.rejected.connect(GeneralSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GeneralSettingsDialog)

    def retranslateUi(self, GeneralSettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        GeneralSettingsDialog.setWindowTitle(_translate("GeneralSettingsDialog", "Dialog"))
        self.groupBox_3.setTitle(_translate("GeneralSettingsDialog", "Settings"))
        self.autoconnect_on_start.setText(_translate("GeneralSettingsDialog", "Autoconnect on start"))
        self.nosplash.setText(_translate("GeneralSettingsDialog", "Do not show splash on start"))

