# -*- coding: utf-8 -*-

#
# voyagerviewerdemo - monitor Voyager application server and display images
#
# Copyright 2019 Michael Fulbright
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Form implementation generated from reading ui file 'imagearea_info.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(955, 753)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.image_tabs = QtWidgets.QTabWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.image_tabs.sizePolicy().hasHeightForWidth())
        self.image_tabs.setSizePolicy(sizePolicy)
        self.image_tabs.setMinimumSize(QtCore.QSize(0, 0))
        self.image_tabs.setObjectName("image_tabs")
        self.horizontalLayout.addWidget(self.image_tabs)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setVerticalSpacing(0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.formLayout.setSpacing(0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.image_size_label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_size_label.sizePolicy().hasHeightForWidth())
        self.image_size_label.setSizePolicy(sizePolicy)
        self.image_size_label.setMinimumSize(QtCore.QSize(0, 0))
        self.image_size_label.setText("")
        self.image_size_label.setObjectName("image_size_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.image_size_label)
        self.image_bin_label_label = QtWidgets.QLabel(Form)
        self.image_bin_label_label.setEnabled(True)
        self.image_bin_label_label.setObjectName("image_bin_label_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.image_bin_label_label)
        self.image_bin_label = QtWidgets.QLabel(Form)
        self.image_bin_label.setEnabled(True)
        self.image_bin_label.setText("")
        self.image_bin_label.setObjectName("image_bin_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.image_bin_label)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.image_median_label = QtWidgets.QLabel(Form)
        self.image_median_label.setText("")
        self.image_median_label.setObjectName("image_median_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.image_median_label)
        self.image_xy = QtWidgets.QLabel(Form)
        self.image_xy.setObjectName("image_xy")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.image_xy)
        self.image_xy_label = QtWidgets.QLabel(Form)
        self.image_xy_label.setText("")
        self.image_xy_label.setObjectName("image_xy_label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.image_xy_label)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.image_value_label = QtWidgets.QLabel(Form)
        self.image_value_label.setText("")
        self.image_value_label.setObjectName("image_value_label")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.image_value_label)
        self.formLayout_2.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.formLayout)
        self.pixel_histogram_spot = QtWidgets.QHBoxLayout()
        self.pixel_histogram_spot.setSpacing(0)
        self.pixel_histogram_spot.setObjectName("pixel_histogram_spot")
        self.formLayout_2.setLayout(1, QtWidgets.QFormLayout.LabelRole, self.pixel_histogram_spot)
        self.horizontalLayout.addLayout(self.formLayout_2)

        self.retranslateUi(Form)
        self.image_tabs.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Image Size:"))
        self.image_bin_label_label.setText(_translate("Form", "Image Binning:"))
        self.label_2.setText(_translate("Form", "Median:"))
        self.image_xy.setText(_translate("Form", "X,Y:"))
        self.label_3.setText(_translate("Form", "Value:"))

