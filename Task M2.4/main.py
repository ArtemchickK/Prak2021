from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtGui import QPixmap
import os
from PyQt5.Qt import Qt
from matplotlib.figure import Figure


def get_picture(picture_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, picture_path)
    return os.path.join(os.path.abspath("."), picture_path)

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("Брюсселятор - Коновалов Артем 304")
        self.setGeometry(300, 250, 1300, 450)

        self.restrictions = QtWidgets.QLabel(self)
        self.restrictions.setText("A > 0, B > 0")
        self.restrictions.move(50, 180)

        self.A = QtWidgets.QLabel("A =", self)
        self.A.move(50, 200)
        self.A_data = QtWidgets.QLineEdit(self)
        self.A_data.setGeometry(70, 208, 25, 15)
        self.A_data.setText("1")
        self.a = 0

        self.B = QtWidgets.QLabel("B =", self)
        self.B.move(50, 220)
        self.B_data = QtWidgets.QLineEdit(self)
        self.B_data.setGeometry(70, 228, 25, 15)
        self.B_data.setText("2")
        self.b = 0

        self.main_text = QtWidgets.QLabel(self)
        self.main_text.setText("Биохимический осциллятор")
        self.main_text.move(50, 25)
        self.main_text.adjustSize()

        self.equation = QtWidgets.QLabel(self)
        pic = QPixmap(get_picture("eq.png")).scaledToHeight(80, Qt.SmoothTransformation)
        self.equation.setGeometry(20, 50, 450, 100)
        self.equation.setPixmap(pic)

        self.unique_point = QtWidgets.QLabel(self)
        self.unique_point.setText("Особая точка- \n(A;B/A)")
        self.unique_point.move(50, 250)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax1 = self.figure.add_subplot(131)
        self.ax2 = self.figure.add_subplot(132)
        self.ax3 = self.figure.add_subplot(133)
        self.plot_widget = QtWidgets.QWidget(self)
        self.plot_widget.setGeometry(300, 10, 1100, 400)
        plot_box = QtWidgets.QVBoxLayout()
        plot_box.addWidget(self.canvas)
        self.plot_widget.setLayout(plot_box)

        self.btn = QtWidgets.QPushButton(self)
        self.btn.move(50, 300)
        self.btn.setText("Рассчитать")
        self.btn.setFixedWidth(200)
        self.btn.clicked.connect(self.draw_plots)

    def draw_plots(self):
        if len(self.A_data.text()) == 0:
            self.a = 1
        else:
            self.a = float(self.A_data.text())

        if len(self.B_data.text()) == 0:
            self.b = 2
        else:
            self.b = float(self.B_data.text())

        if (self.a <= 0) or (self.b <= 0):
            raise SystemExit(1)

        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()

        def system_of_ode(s, t, A, B):
            y1, y2 = s
            return A - B * y1 - y1 + y1 ** 2 * y2, B * y1 - y1 ** 2 * y2

        eps = 0.05
        dt = 0.01
        t_stop = 250
        iters = int(t_stop / dt)
        t = np.linspace(0, t_stop, iters)
        start_state = [self.a + eps, self.b / self.a + eps]
        solution = odeint(system_of_ode, start_state, t, args=(self.a, self.b))

        self.ax1.plot(t, solution[:, 0], 'b', lw=0.7)
        self.ax1.set(xlabel='t', ylabel='y1(t)', title='Функция y1(t)')

        self.ax2.plot(t, solution[:, 1], 'g', lw=0.7)
        self.ax2.set(xlabel='t', ylabel='y2(t)', title='Функция y2(t)')

        if (self.b >= 2) & (self.b <= 2.5):
            self.ax3.plot(solution[:, 0], solution[:, 1], lw=0.5)
            self.ax3.set(xlabel='y1(t)', ylabel='y2(t)', title='Фазовая плоскость')
        else:
            self.ax3.plot(solution[:, 0], solution[:, 1], lw=1.0)
            self.ax3.set(xlabel='y1(t)', ylabel='y2(t)', title='Фазовая плоскость')
        self.canvas.draw()


def application():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
