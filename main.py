import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

import errors

from scipy.signal import find_peaks
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


qtcreator_file  = "tax_calc.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

def closest_value_index(data, point):
    difference_array = np.absolute(data-point)
    return difference_array.argmin()

def lower_limit(data, index):
    while data[index] > 1:
        index -= 1
    else:
        return index

def upper_limit(data, index):
    while data[index] > 1:
        index += 1
    else:
        return index

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Impulse Calculation")
        self.setGeometry(600, 300, 900, 600)
        self.setWindowIcon(QIcon('title_icon.png'))

        self.confirm_path_button.clicked.connect(self.ConfirmPath)
        self.plot1_button.clicked.connect(self.ConfirmPage1)
        self.border_button_lower.clicked.connect(self.getLowerBorder)
        self.border_button_upper.clicked.connect(self.getUpperBorder)
        self.peakSettingButton.clicked.connect(self.getPeaks)
        self.confirm_borders.clicked.connect(self.calculateImpulse)
        self.chooseButton.clicked.connect(self.chooseFile)
        self.startOverButton.clicked.connect(self.goToFirstPage)
        self.finishButton.clicked.connect(self.close)

        ###setting up the first plot
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.plot_frame)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.horizontalLayout_4.addWidget(self.canvas)

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.plot2_frame)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.figure2 = plt.figure()
        self.canvas2 = FigureCanvas(self.figure2)
        self.horizontalLayout_5.addWidget(self.canvas2)

    

    def chooseFile(self):
        global fname
        fname = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", 'D:')
        self.path_box.setText(fname[0])


    def ConfirmPath(self):
        try:
            path = str(self.path_box.toPlainText())
            df = pd.read_excel(path)

            time_ = np.array(df["Time(Seconds)"])
            torque_ = np.array(df["Torque(Newton-Meters)"])

            global time
            global torque

            time = time_
            torque = torque_

            path_string = "Selected path to file is: \n" + str(path)
            self.results_window.setText(path_string)

        except ValueError:
            errors.velue_error_func()
        
        except FileNotFoundError:
            errors.file_not_found_error_func()
        
        except KeyError:
            errors.key_error_func()

        except:
            errors.other_error()

                

    
    def ConfirmPage1(self):
        try:
            self.stackedWidget.setCurrentIndex(1)
            self.figure.clear()

            ax1 = self.figure.add_subplot(111)

            ax1.plot(time, torque, label="Torque")

            ax1.set_xlabel('Time [s]')
            ax1.set_ylabel('Torque [Nm]')

            ax1.grid(True)
            ax1.legend()

            self.canvas.draw()

        except NameError:
            self.stackedWidget.setCurrentIndex(0)
            errors.name_error_func()
        
        except:
            errors.other_error()


    def goToFirstPage(self):
        self.stackedWidget.setCurrentIndex(0)
        self.results_window.clear()
        self.path_box.clear()

    def getLowerBorder(self):
        try:
            global lower_border
            lower_border_ = float(self.text_border_lower.toPlainText())

            if lower_border_ > time[0]:
                lower_border = lower_border_
            else:
                lower_border = time[0]

            self.figure.clear()

            ax1 = self.figure.add_subplot(111)


            ax1.plot(time, torque, label="Torque")
            ax1.axvline(lower_border, color ="red", label = "Lower border")

            ax1.set_xlabel('Time [s]')
            ax1.set_ylabel('Torque [Nm]')

            ax1.grid(True)
            ax1.legend()

            self.canvas.draw()

        except ValueError:
            errors.value_error_pag2()

        except:
            errors.other_error()

    def getUpperBorder(self):
        try:
            global upper_border
            upper_border_ = float(self.text_border_upper.toPlainText())

            if upper_border_ < time[-1]:
                upper_border = upper_border_
            else:
                upper_border = time[-1]

            self.figure.clear()

            ax1 = self.figure.add_subplot(111)

            ax1.plot(time, torque, label="Torque")
            ax1.axvline(lower_border, color ="red", label = "Lower border")
            ax1.axvline(upper_border, color ="orange", label = "Upper border")

            ax1.set_xlabel('Time [s]')
            ax1.set_ylabel('Torque [Nm]')

            ax1.grid(True)
            ax1.legend()

            self.canvas.draw()

        except ValueError:
            errors.value_error_pag2()

        except:
            errors.other_error()

    def getPeaks(self):
        try:
            height_peaks = float(self.minPeak.toPlainText())
            distance_peaks = float(self.distancePeak.toPlainText())

            ### cuting signals
            lower_index = closest_value_index(time, lower_border)
            upper_index = closest_value_index(time, upper_border)
            
            global time_cut
            global torque_cut
            time_cut = time[lower_index:upper_index+1]
            torque_cut = torque[lower_index:upper_index+1]

            ### finding peaks
            global peaks
            peaks, _ = find_peaks(torque_cut, height = height_peaks, distance = distance_peaks)

            global peaks_lower
            global peaks_upper

            peaks_lower = np.zeros(len(peaks),dtype=int)
            peaks_upper = np.zeros(len(peaks),dtype=int)

            for i in range(0, len(peaks),1):
                peaks_lower[i] = lower_limit(torque_cut, peaks[i])

            for i in range(0, len(peaks),1):
                peaks_upper[i] = upper_limit(torque_cut, peaks[i])

            self.figure.clear()

            ax1 = self.figure.add_subplot(111)

            ax1.plot(time_cut, torque_cut, label="Torque")

            ax1.set_xlabel('Time [s]')
            ax1.set_ylabel('Torque [Nm]')
            ax1.plot(time_cut[peaks], torque_cut[peaks], "o", color = "red", label = "Max values")
            ax1.plot(time_cut[peaks_lower], torque_cut[peaks_lower], "o", color = "orange", label = "Lower limits")
            ax1.plot(time_cut[peaks_upper], torque_cut[peaks_upper], "o", color = "green",  label = "Upper limits")

            ax1.grid(True)
            ax1.legend()

            self.canvas.draw()

        except ValueError:
            errors.value_error_pag2_peaks()

        except:
            errors.other_error()

    
    def calculateImpulse(self):
        try:
            dy = []
            dx = []

            for i in range(0,len(peaks),1):
                integ = torque_cut[peaks_lower[i]:peaks_upper[i]+1]
                integ2 = time_cut[peaks_lower[i]:peaks_upper[i]+1]
                dy.append(integ)
                dx.append(integ2)

            integrals = []

            for i in range(0, len(peaks),1):
                integrals.append(np.trapz(dy[i], dx[i]))

            self.stackedWidget.setCurrentIndex(2)
            self.figure2.clear()

            ax2 = self.figure2.add_subplot(111)

            ax2.plot(time_cut, torque_cut, label="Torque")
            ax2.plot(time_cut[peaks], torque_cut[peaks], "o", color = "red", label = "Max values")
            ax2.plot(time_cut[peaks_lower], torque_cut[peaks_lower], "o", color = "orange", label = "Lower limits")
            ax2.plot(time_cut[peaks_upper], torque_cut[peaks_upper], "o", color = "green",  label = "Upper limits")

            ax2.fill(time_cut,torque_cut, alpha = 0.2, label = "Impulse")


            ax2.set_xlabel('Time [s]')
            ax2.set_ylabel('Torque [Nm]')

            ax2.grid(True)
            ax2.legend()

            self.canvas2.draw()
            
            results_strings = []

            for i in range(0, len(integrals),1):
                results_strings.append(str(f'{i+1}. impulse: {integrals[i]:.3f} Nm s'))

            results_strings.append(str(f'Total impulse {sum(integrals):.3f} Nm s'))

            join = '\n'.join(results_strings)

            self.resultsText.setText(join)

            tut = []

            for i in range(0, len(peaks_lower), 1):
                tut_ = time_cut[peaks_upper[i]] - time_cut[peaks_lower[i]]
                tut.append(tut_)

            tut_str = []

            for i in range(0, len(peaks_lower), 1):
                tut_str.append(str(f'{i+1}. impulse: {tut[i]:.2f} s'))

            

            tut_str.append(str(f'Total time under tension: {sum(tut):.2f} s'))

            tut_strings =  '\n'.join(tut_str)

            self.resultsTut.setText(tut_strings)
        
        except NameError:
            errors.name_error_pag2()
        
        except:
            errors.other_error()

        



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())