from taurus.external.qt.Qt import (QDialog, QLabel, QLineEdit,
                                   QPushButton, QVBoxLayout,
                                   QHBoxLayout)


class DecimationConfigDialog(QDialog):
    """
    Custom Input Dialog to retrieve decimation period desired from the user and
    apply the decimation using archiving.
    """
    def __init__(self, parent=None, message="", default_period=0):
        super().__init__(parent)
        self.setWindowTitle("Select Decimation Factor")

        # Create configurable options
        self.selectedOption = "Apply"

        # Create UI elements
        self.label = QLabel(message)
        self.lineEdit = QLineEdit(str(default_period))
        self.applyButton = QPushButton("Apply")
        self.cancelButton = QPushButton("Cancel")
        self.defaultButton = QPushButton("Default")
        self.dontAskAgainButton = QPushButton("Don't Ask Again")

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.cancelButton)
        buttons_layout.addWidget(self.defaultButton)
        buttons_layout.addWidget(self.dontAskAgainButton)
        buttons_layout.addWidget(self.applyButton)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)
        # Connect signals to slots
        self.applyButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
        self.defaultButton.clicked.connect(self.setDefaultDecimation)
        self.dontAskAgainButton.clicked.connect(self.setDontAskAgain)

    def setDefaultDecimation(self):
        self.selectedOption = "Default"
        self.accept()

    def setDontAskAgain(self):
        self.selectedOption = "No asking"
        self.accept()

    def getInputText(self):
        return self.lineEdit.text()
