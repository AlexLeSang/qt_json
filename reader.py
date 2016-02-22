from PyQt5.QtCore import QFile, QJsonDocument, QJsonParseError, QByteArray


def read_js(js_path):
    js = None
    stream = QFile(js_path)
    if stream.open(QFile.ReadOnly):
        js = QByteArray(unicode(stream.readAll()))
        stream.close()
    else:
        print(stream.errorString())

    return js


if __name__ == '__main__':
    parse_err = QJsonParseError()
    byte_array = read_js('example.json')
    json_document = QJsonDocument.fromJson(byte_array, parse_err)
    if QJsonParseError.NoError == parse_err.error:
        print(parse_err.errorString())

    if json_document.isObject():
        json_object = json_document.object()
        for k in json_object:
            print(k + ': ' + str(json_object[k].toVariant()))