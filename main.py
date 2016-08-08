import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from gui import Ui_MainWindow

class GuiProgram(Ui_MainWindow):
    def __init__(self, dialog):
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)

        self.scriptOpen.clicked.connect(self.getFileName)
        self.targetOpen.clicked.connect(self.getTargetName)
        self.convertPy.clicked.connect(self.pyConvert)

        self.process = QtCore.QProcess()
        self.process.readyRead.connect(self.dataReady)

        self.process.started.connect(lambda: self.convertPy.setEnabled(False))
        self.process.finished.connect(lambda: self.convertPy.setEnabled(True))

    def getFileName(self):
        self.fileName = str(QtWidgets.QFileDialog.getOpenFileName(None, 'Open Script', os.getenv('HOME'))[0])
        self.scriptFileLocation.setText(self.fileName)

    def getTargetName(self):
        self.outputName = str(QtWidgets.QFileDialog.getExistingDirectory(None, 'Output Directory', os.getenv('HOME')))
        self.outputFolderLocation.setText(self.outputName)

    def dataReady(self):
        cursor = self.commandOutput.textCursor()
        cursor.movePosition(cursor.End)
        self.commandOutput.insertPlainText(str(self.process.ready()))
        self.commandOutput.ensureCursorVisible()

    def pyConvert(self):
        command = ""
        if self.windowedOption.isChecked():
            command += " -w"
        if self.oneFile.isChecked():
            command += " -F"
        #command += " --distpath "
        #command += self.outputName
        command += " \""
        command += os.path.normpath(self.fileName)
        command += "\""

        self.commandOutput.insertPlainText("pyinstaller" + command)

        self.process.start("pyinstaller", command.split())

    def readOutput(self):
        self.commandOutput.append(QString(self.process.readStdout()))
        if self.process.isRunning()==False:
            self.commandOutput.append("\n Compiled")

    def readErrors(self):
        self.commandOutput.append("\n An error occured. \n" + QString(self.process.readLineStderr()))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()

    main = GuiProgram(dialog)
    dialog.setFixedSize(800, 600)

    dialog.show()
    sys.exit(app.exec_())
