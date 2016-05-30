from PyQt5 import QtCore
from PyQt5.QtCore import QJsonDocument, QJsonValue

from TreeItem import TreeItem, RootItem


class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)

        self.rootItem = RootItem(2)
        self.get_type(data, self.rootItem)

        # # self.rootItem = RootItem(1)
        # item_1 = TreeItem('l1_1', self.rootItem)
        # item_1.appendChild(TreeItem('l2_1', item_1))
        # item_1.appendChild(TreeItem('l2_2', item_1))
        # item_1.appendChild(TreeItem('l2_3', item_1))
        #
        # self.rootItem.appendChild(item_1)
        #
        #
        # item_2 = TreeItem('l1_2', self.rootItem)
        # self.rootItem.appendChild(item_2)
        #
        # item_3 = TreeItem('l1_3', self.rootItem)
        # self.rootItem.appendChild(item_3)
        # # self.setupModelData(data.split('\n'), self.rootItem)

    @staticmethod
    def get_type(json_document, root_item):

        if isinstance(json_document, QJsonValue):
            if json_document.isBool():
                name = 'True' if json_document.isBool() else 'False'
                root_item.setValue(name)
                return

            if json_document.isDouble():
                name = str(json_document.toDouble())
                root_item.setValue(name)
                return

            if json_document.isNull():
                name = 'None'
                root_item.setValue(name)
                return

            if json_document.isString():
                name = json_document.toString()
                root_item.setValue(name)
                return

        if json_document.isArray():
            array_item = TreeItem('array', root_item)
            array = None
            if isinstance(json_document, QJsonDocument):
                array = json_document.array()
            elif isinstance(json_document, QJsonValue):
                array = json_document.toArray()

            for el in array:
                TreeModel.get_type(el, array_item)

            root_item.appendChild(array_item)
            return

        if json_document.isNull():
            name = 'None'
            root_item.appendChild(TreeItem(name, root_item))
            return

        if json_document.isObject():
            json_document_object = None
            if isinstance(json_document, QJsonDocument):
                json_document_object = json_document.object()
            elif isinstance(json_document, QJsonValue):
                json_document_object = json_document.toObject()

            for obj in json_document_object:
                obj_item = TreeItem(obj, root_item)
                TreeModel.get_type(json_document_object[obj], obj_item)
                root_item.appendChild(obj_item)

            return

        return

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != QtCore.Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            # return self.rootItem.data(section)
            return ''

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def setupModelData(self, lines, parent):
        parents = [parent]
        indentations = [0]

        number = 0

        while number < len(lines):
            position = 0
            while position < len(lines[number]):
                if lines[number][position] != ' ':
                    break
                position += 1

            lineData = lines[number][position:].trimmed()

            if lineData:
                # Read the column data from the rest of the line.
                columnData = [s for s in lineData.split('\t') if s]

                if position > indentations[-1]:
                    # The last child of the current parent is now the new
                    # parent unless the current parent has no children.

                    if parents[-1].childCount() > 0:
                        parents.append(parents[-1].child(parents[-1].childCount() - 1))
                        indentations.append(position)

                else:
                    while position < indentations[-1] and len(parents) > 0:
                        parents.pop()
                        indentations.pop()

                # Append a new item to the current parent's list of children.
                parents[-1].appendChild(TreeItem(columnData, parents[-1]))

            number += 1