from definitions import *
from PyQt6 import QtWidgets, uic #pip install PyQt6
from PyQt6.QtGui import QValidator
import sys

class intValidator(QValidator):
    def __init__(self, maximum, minimum=0, parent=None):
        super().__init__(parent)
        self.maximum = int(maximum)
        self.minimum = int(minimum)
    
    def validate(self, input_str, pos):
        if input_str == "" or input_str.isdigit() and self.minimum <= int(input_str) <= self.maximum:
            return (QValidator.State.Acceptable, input_str, pos)
        return (QValidator.State.Invalid, input_str, pos)

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('gui.ui', self)
        
        browseFileName = self.findChild(QtWidgets.QPushButton, "browseFileName")
        browseFileName.clicked.connect(self.browseSaveFile)
        
        woganogText = self.findChild(QtWidgets.QLabel, "woganogText")
        woganogText.setText('Program by <a href="https://youtube.com/@Woganog">Woganog</a>.')

        woganogText = self.findChild(QtWidgets.QLabel, "emiliaText")
        woganogText.setText('and <a href="https://github.com/nobodyF34R">Emilia</a>.')
        
        int16 = intValidator(65535)
        
        int32 = intValidator(4294967295)
        
        global xCoordText
        xCoordText = self.findChild(QtWidgets.QLineEdit, "xCoordText")
        xCoordText.setValidator(int32)
        
        global yCoordText
        yCoordText = self.findChild(QtWidgets.QLineEdit, "yCoordText")
        yCoordText.setValidator(int32)
        
        global zCoordText
        zCoordText = self.findChild(QtWidgets.QLineEdit, "zCoordText")
        zCoordText.setValidator(int32)
        
        global timeText
        timeText = self.findChild(QtWidgets.QLineEdit, "timeText")
        timeText.setValidator(int16)
        
        global mapText
        mapText = self.findChild(QtWidgets.QComboBox, "mapText")
        # mapText.setMaxLength(7)
        
        goButton = self.findChild(QtWidgets.QPushButton, "goButton")
        goButton.clicked.connect(self.goFunction)
        
        global sunTimeComboBox
        sunTimeComboBox = self.findChild(QtWidgets.QComboBox, "sunTimeComboBox")
        
        global saveFileName
        saveFileName = self.findChild(QtWidgets.QLineEdit, "saveFileName")
        
        self.show()
    
    def browseSaveFile(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, "Open save file", "C:", "Yo-kai Watch save files (*.yw);;Decrypted Yo-kai Watch save files (*.ywd)")
        self.saveFileName.setText(fname[0])
    
    def successPopup(self, path):
        self.popup = QtWidgets.QMessageBox()
        self.popup.setWindowTitle("Done!")
        self.popup.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        self.popup.setText(f"Success! File saved as {path}")
        self.popup.show()

    def failurePopup(self, e):
        self.popup = QtWidgets.QMessageBox()
        self.popup.setWindowTitle("Error!")
        self.popup.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        self.popup.setText(f"An error has occurred: {e}")
        self.popup.show()

    def goFunction(self):
        try:
            if saveFileName.text()[-3:] == "ywd":
                inject(open(saveFileName.text(), "r+b"), locations[mapText.currentText()], xCoordText.text(), yCoordText.text(), zCoordText.text(), timeText.text(), sunTimes[sunTimeComboBox.currentText()])
            else:
                import yw_save
                import io
                with open(saveFileName.text(), "r+b") as f:
                    out = inject(io.BytesIO(yw_save.yw_proc(f.read(), False)), locations[mapText.currentText()], xCoordText.text(), yCoordText.text(), zCoordText.text(), timeText.text(), sunTimes[sunTimeComboBox.currentText()])
                    f.seek(0)
                    f.write(yw_save.yw_proc(out, True))
            self.successPopup(saveFileName.text())
        except FileNotFoundError:
            self.failurePopup("Invalid path.")
        except Exception as e:
            self.failurePopup(e)
            print(e)


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec()
