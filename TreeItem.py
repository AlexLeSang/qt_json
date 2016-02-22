from sympy.physics.secondquant import NO


class TreeItem(object):
    def __init__(self, data=None, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return 2

    def data(self, column):
        if column == 0:
            return self.itemData
        # try:
        #     return self.itemData[column]
        # except IndexError:
        #     return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0


class RootItem(object):
    def __init__(self, colum_count):
        self.childItems = []
        self.colum_count = colum_count

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def row(self):
        return 0

    def parent(self):
        return None

    def columnCount(self):
        return self.colum_count