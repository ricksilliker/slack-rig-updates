import json

from PySide2 import QtNetwork, QtCore


def createRequest(url):
    url = QtCore.QUrl(url)
    request = QtNetwork.QNetworkRequest(url)
    request.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, 'application/json')

    return request

def doPOST(manager, request, **data):
    return manager.post(request, json.dumps(data))