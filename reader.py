from PyQt5.QtCore import QFile, QJsonDocument, QJsonValue, QJsonParseError, QByteArray


def read_js(js_path):
    js = None
    stream = QFile(js_path)
    if stream.open(QFile.ReadOnly):
        js = QByteArray((stream.readAll()))
        stream.close()
    else:
        print(stream.errorString())

    return js


def get_type(json_document):

    if isinstance(json_document, QJsonValue):
        if json_document.isBool():
            return 'True' if json_document.isBool() else 'False'

        if json_document.isDouble():
            return str(json_document.toDouble())

        if json_document.isNull():
            return ''

        if json_document.isString():
            return json_document.toString()

    if json_document.isArray():
        st = ' ['
        array = None
        if isinstance(json_document, QJsonDocument):
            array = json_document.array()
        elif isinstance(json_document, QJsonValue):
            array = json_document.toArray()

        for el in array:
            st += get_type(el) + ' '

        st = st[:-1]
        st += ']'
        return st

    if json_document.isNull():
        return 'null'

    if json_document.isObject():
        st = ' {\n'

        json_document_object = None
        if isinstance(json_document, QJsonDocument):
            json_document_object = json_document.object()
        elif isinstance(json_document, QJsonValue):
            json_document_object = json_document.toObject()

        for obj in json_document_object:
            st += obj + ': ' + get_type(json_document_object[obj]) + '\n'

        st = st[:-1]
        st += '\n}'
        return st

    return ''


if __name__ == '__main__':
    parse_err = QJsonParseError()
    byte_array = read_js('example.json')
    json_document = QJsonDocument.fromJson(byte_array, parse_err)
    if QJsonParseError.NoError == parse_err.error:
        print(parse_err.errorString())

    # if json_document.isObject():
    #     json_object = json_document.object()
    #     for k in json_object:
    #         print(k + ': ' + str(json_object[k].toVariant()))

    print(get_type(json_document))