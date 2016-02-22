from PyQt5.QtCore import QObject, QAbstractItemModel, QJsonDocument


class QJsonTreeModel(QAbstractItemModel):
    def __init__(self, json_document, QObject_parent=None):
        QObject.__init__(self, QObject_parent)
        self.json_document = json_document

    def jsonDocument(self):
        return self.json_document


def test_create():
    model = QJsonTreeModel(None)
    assert model.jsonDocument() is None


def test_set_json_object():
    json_object = QJsonDocument()
    model = QJsonTreeModel(json_object)
    assert model.jsonDocument().isEmpty()
