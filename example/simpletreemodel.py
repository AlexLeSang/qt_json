#!/usr/bin/env python

from PyQt5 import QtCore, QtWidgets

from PyQt5.QtCore import QJsonDocument, QJsonParseError

from TreeModel import TreeModel
from reader import read_js

if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)

    # f = QtCore.QFile('default.txt')
    # f.open(QtCore.QIODevice.ReadOnly)
    # model = TreeModel(f.readAll())
    # f.close()


    parse_err = QJsonParseError()
    byte_array = read_js('../example.json')
    json_document = QJsonDocument.fromJson(byte_array, parse_err)
    if QJsonParseError.NoError == parse_err.error:
        print(parse_err.errorString())

    # json_document = QJsonDocument()
    model = TreeModel(json_document)

    view = QtWidgets.QTreeView()
    view.setModel(model)
    view.setWindowTitle("Json Tree Model")
    view.show()
    sys.exit(app.exec_())
