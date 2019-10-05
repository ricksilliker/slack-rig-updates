import os
import platform

from PySide2 import QtWidgets, QtCore, QtNetwork

import utils
import service


test_value = [{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "A message *with some bold text* and _some italicized text_."
  }
}]

class MainWidget(QtWidgets.QWidget):
    @staticmethod
    def run():
        """Creates an instance of the MainWidget and shows it in Maya's main view."""
        mayaWindow = utils.mayaMainWindow()
        widget = MainWidget(parent=mayaWindow)
        if platform.system() == 'Darwin':
            # MacOS is special, and the QtCore.Qt.Window flag does not sort the windows properly,
            # so instead QtCore.Qt.Tool is used.
            widget.setWindowFlags(widget.windowFlags() | QtCore.Qt.Tool)
        # Center the widget with Maya's main window.
        widget.move(mayaWindow.frameGeometry().center() - QtCore.QRect(QtCore.QPoint(), widget.sizeHint()).center())
        
        widget.show()

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent=parent)

        # Configure the QWidget properties.
        self.setObjectName('SlackRigUpdater')
        self.setWindowTitle('Send to Slack')

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.tabs = QtWidgets.QTabWidget()
        main_layout.addWidget(self.tabs)

        self.sendUpdateTab = SendUpdateTab(self)
        self.tabs.addTab(self.sendUpdateTab, self.sendUpdateTab.title)

        self.requestFeedbackTab = RequestFeedbackTab(self)
        self.tabs.addTab(self.requestFeedbackTab, self.requestFeedbackTab.title)


class SendUpdateTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SendUpdateTab, self).__init__(parent=parent)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        form_layout = QtWidgets.QFormLayout()
        main_layout.addLayout(form_layout)

        self.channelNameField = QtWidgets.QLineEdit()
        form_layout.addRow('Channel Name:', self.channelNameField)

        self.assetNameField = QtWidgets.QLineEdit()
        form_layout.addRow('Asset Name:', self.assetNameField)

        notesLabel = QtWidgets.QLabel('Notes:')
        main_layout.addWidget(notesLabel)

        self.notesList = QtWidgets.QListWidget()
        main_layout.addWidget(self.notesList)

        self.addNoteField = QtWidgets.QLineEdit()
        main_layout.addWidget(self.addNoteField)

        h_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(h_layout)

        self.attachFileButton = QtWidgets.QPushButton('Attach File')
        h_layout.addWidget(self.attachFileButton)

        self.uploadFilePath = QtWidgets.QLabel()
        h_layout.addWidget(self.uploadFilePath)

        self.button = QtWidgets.QPushButton('Send')
        self.button.clicked.connect(self.sendTest)
        main_layout.addWidget(self.button)

        self.http = QtNetwork.QNetworkAccessManager()
        self.http.finished.connect(self.logResponse)

        self.response = None

    @property
    def title(self):
        return 'Send Update'


    def createBlocks(self):
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "{0} was updated!".format(self.assetNameField.text()),
                }
		    },
            {
			    "type": "divider"
		    },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*CHANGELOG*",
                }
		    }
        ]

        notesFormatted = ''

        for item in self.notesList.items():
            note = item.data(QtCore.Qt.DisplayRole)
            noteFormatted = "• {0} \n".format(note)
            notesFormatted += noteFormatted

        blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": notesFormatted,
                }
		    })

        return blocks

    def sendTest(self):
        url = os.environ['SLACK_WEBHOOK_URL']
        request = service.createRequest(url)
        self.response = service.doPOST(self.http, request, blocks=self.createBlocks())

    def logResponse(self):
        if self.response == None:
            return

        err = self.response.error()

        if err == QtNetwork.QNetworkReply.NoError:
            print str(self.response.readAll())
        else:
            print self.response.errorString()


class RequestFeedbackTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(RequestFeedbackTab, self).__init__(parent=parent)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        form_layout = QtWidgets.QFormLayout()
        main_layout.addLayout(form_layout)

        self.channelNameField = QtWidgets.QLineEdit()
        form_layout.addRow('Channel Name:', self.channelNameField)

        self.askQuestionField = QtWidgets.QLineEdit()
        form_layout.addRow('Ask:', self.askQuestionField)

        optionsLabel = QtWidgets.QLabel('Options:')
        main_layout.addWidget(optionsLabel)

        self.optionsList = QtWidgets.QListWidget()
        main_layout.addWidget(self.optionsList)

        self.addOptionField = QtWidgets.QLineEdit()
        main_layout.addWidget(self.addOptionField)

        h_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(h_layout)

        self.attachFileButton = QtWidgets.QPushButton('Attach File')
        h_layout.addWidget(self.attachFileButton)

        self.uploadFilePath = QtWidgets.QLabel()
        h_layout.addWidget(self.uploadFilePath)

        self.button = QtWidgets.QPushButton('Send')
        self.button.clicked.connect(self.sendTest)
        main_layout.addWidget(self.button)

        self.http = QtNetwork.QNetworkAccessManager()
        self.http.finished.connect(self.logResponse)

        self.response = None

    @property
    def title(self):
        return 'Request Feedback'

    def createBlocks(self):
        blocks = []
        return blocks

    def sendTest(self):
        url = os.environ['SLACK_WEBHOOK_URL']
        request = service.createRequest(url)
        self.response = service.doPOST(self.http, request, blocks=test_value)

    def logResponse(self):
        if self.response == None:
            return

        err = self.response.error()

        if err == QtNetwork.QNetworkReply.NoError:
            print str(self.response.readAll())
        else:
            print self.response.errorString()