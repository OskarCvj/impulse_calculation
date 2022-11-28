import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox


######     PAGE1     #####
##  CONFIRM PATH BUTTON  ##
def velue_error_func():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Value Error")
    msg.setInformativeText('Expected \'xlsx\' file format.')
    msg.setWindowTitle("Error")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()

def file_not_found_error_func():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("File Not Found Error")
    msg.setInformativeText('Please select file.')
    msg.setWindowTitle("Error")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()

def key_error_func():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Key Error")
    msg.setInformativeText('Selected file not configured correctly.')
    msg.setWindowTitle("Error")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()

##  PLOT BUTTON  ##
def name_error_func():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Name Error")
    msg.setInformativeText('Please select file in first step.')
    msg.setWindowTitle("Error")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()


#####     PAGE2     #####
def value_error_pag2():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Value Error")
    msg.setInformativeText('Expected integer value.')
    msg.setWindowTitle("Error")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()

def value_error_pag2_peaks():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Value Error")
    msg.setInformativeText('Both fields need integer values.')
    msg.setWindowTitle("Error")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()

def name_error_pag2():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Name Error")
    msg.setInformativeText('Enter values in all fields.')
    msg.setWindowTitle("Error")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()


#####     OTHER ERRORS     #####
def other_error():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Unknown Error")
    msg.setInformativeText('Contact administrator')
    msg.setWindowTitle("Error")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()
