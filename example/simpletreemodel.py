#!/usr/bin/env python

from PyQt5 import QtCore, QtWidgets

from PyQt5.QtCore import QJsonDocument

from TreeModel import TreeModel

if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)

    # f = QtCore.QFile('default.txt')
    # f.open(QtCore.QIODevice.ReadOnly)
    # model = TreeModel(f.readAll())
    # f.close()


    jsonDocument = QJsonDocument()
    model = TreeModel(jsonDocument)

    view = QtWidgets.QTreeView()
    view.setModel(model)
    view.setWindowTitle("Json Tree Model")
    view.show()
    sys.exit(app.exec_())
