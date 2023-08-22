from PyQt5 import QtWidgets, uic, QtGui
import sys
import os

class Ui(QtWidgets.QMainWindow):
	def __init__(self):
		super(Ui, self).__init__()
		uic.loadUi('gui.ui', self)
		
		browseFileName = self.findChild(QtWidgets.QPushButton, "browseFileName")
		browseFileName.clicked.connect(self.browseSaveFile)
		
		mapCodeLink = self.findChild(QtWidgets.QLabel, "mapCodeLink")
		mapCodeLink.setText('Map codes can be found <a href="https://tcrf.net/Notes:Yo-kai_Watch_(Nintendo_3DS)#Map_names">here!</a>')
		
		onlyInt = QtGui.QIntValidator()
		onlyInt.setRange(0, 65535)
		
		global xCoordText
		xCoordText = self.findChild(QtWidgets.QLineEdit, "xCoordText")
		xCoordText.setValidator(onlyInt)
		
		global yCoordText
		yCoordText = self.findChild(QtWidgets.QLineEdit, "yCoordText")
		yCoordText.setValidator(onlyInt)
		
		global zCoordText
		zCoordText = self.findChild(QtWidgets.QLineEdit, "zCoordText")
		zCoordText.setValidator(onlyInt)
		
		global timeText
		timeText = self.findChild(QtWidgets.QLineEdit, "timeText")
		timeText.setValidator(onlyInt)
		
		global mapText
		mapText = self.findChild(QtWidgets.QLineEdit, "mapText")
		mapText.setMaxLength(7)
		
		goButton = self.findChild(QtWidgets.QPushButton, "goButton")
		goButton.clicked.connect(self.goFunction)
		
		global sunTimeComboBox
		sunTimeComboBox = self.findChild(QtWidgets.QComboBox, "sunTimeComboBox")
		
		global saveFileName
		saveFileName = self.findChild(QtWidgets.QLineEdit, "saveFileName")
		
		global keepDecryptedCheckBox
		keepDecryptedCheckBox = self.findChild(QtWidgets.QCheckBox, "keepDecryptedCheckBox")
		
		self.show()
	
	def browseSaveFile(self):
		fname = QtWidgets.QFileDialog.getOpenFileName(self, "Open save file", "C:", "Yo-kai Watch save files (*.yw)")
		self.saveFileName.setText(fname[0])
	
	def successPopup(self):
		self.popup = QtWidgets.QMessageBox()
		self.popup.setWindowTitle("Done!")
		self.popup.setDefaultButton(QtWidgets.QMessageBox.Ok)
		self.popup.setText("Complete! File saved as output.yw.")
		
		self.popup.show()
	
	def goFunction(self):
		os.system('python yw_save/yw_save.py --game yw --decrypt "' + saveFileName.text() + '" decrypted.yw')
		
		with open("decrypted.yw", "r+b") as f:
			if mapText.text() != "":
				f.seek(72)
				f.write(bytes(mapText.text(), 'utf-8'))
			if xCoordText.text() != "":
				xCoord = int(xCoordText.text())
				f.seek(22)
				f.write(xCoord.to_bytes(2, byteorder = "big", signed = True))
			if yCoordText.text() != "":
				yCoord = int(yCoordText.text())
				f.seek(24)
				f.write(yCoord.to_bytes(2, byteorder = "big", signed = True))
			if zCoordText.text() != "":
				zCoord = int(zCoordText.text())
				f.seek(28)
				f.write(zCoord.to_bytes(2, byteorder = "big", signed = True))
			if timeText.text() != "":
				time = int(timeText.text())
				f.seek(1488)
				f.write(time.to_bytes(2, byteorder = "big", signed = False))
			f.seek(1490)
			if sunTimeComboBox.currentText() == "Morning to Midday":
				f.write(int.to_bytes(1, 1, byteorder = "big"))
			if sunTimeComboBox.currentText() == "Midday to Night":
				f.write(int.to_bytes(2, 1, byteorder = "big"))
			if sunTimeComboBox.currentText() == "Night to Midnight":
				f.write(int.to_bytes(3, 1, byteorder = "big"))
			if sunTimeComboBox.currentText() == "Midnight to Morning":
				f.write(int.to_bytes(4, 1, byteorder = "big"))
		
		os.system("python yw_save/yw_save.py --game yw --encrypt decrypted.yw output.yw")
		if keepDecryptedCheckBox.isChecked() == False:
			os.remove("decrypted.yw")
		
		self.successPopup()

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()