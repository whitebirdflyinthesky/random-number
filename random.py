from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QTextEdit, QCheckBox, QHBoxLayout
from PyQt5.QtCore import pyqtSlot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
import random
import numpy as np
from scipy.stats import norm

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Random Number Generator'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.layout = QHBoxLayout()

        self.vbox = QVBoxLayout()
        self.layout.addLayout(self.vbox)

        self.label_min = QLabel("Minimum Value:")
        self.vbox.addWidget(self.label_min)
        self.input_min = QLineEdit(self)
        self.vbox.addWidget(self.input_min)

        self.label_max = QLabel("Maximum Value:")
        self.vbox.addWidget(self.label_max)
        self.input_max = QLineEdit(self)
        self.vbox.addWidget(self.input_max)

        self.label_count = QLabel("Number of Random Numbers:")
        self.vbox.addWidget(self.label_count)
        self.input_count = QLineEdit(self)
        self.input_count.setText("10")
        self.vbox.addWidget(self.input_count)

        self.label_decimals = QLabel("Number of Decimals:")
        self.vbox.addWidget(self.label_decimals)
        self.input_decimals = QLineEdit(self)
        self.input_decimals.setText("2")
        self.vbox.addWidget(self.input_decimals)

        self.check_repeat = QCheckBox("Allow Repeat")
        self.check_repeat.setChecked(True)
        self.vbox.addWidget(self.check_repeat)

        self.check_normal = QCheckBox("Normal Distribution")
        self.vbox.addWidget(self.check_normal)

        self.button = QPushButton('Generate Random Numbers', self)
        self.button.clicked.connect(self.on_click)
        self.vbox.addWidget(self.button)

        self.text_area = QTextEdit(self)
        self.vbox.addWidget(self.text_area)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)
        self.show()

    @pyqtSlot()
    def on_click(self):
        min_value = float(self.input_min.text())
        max_value = float(self.input_max.text())
        count = int(self.input_count.text())
        decimals = int(self.input_decimals.text())
        allow_repeat = self.check_repeat.isChecked()
        normal_distribution = self.check_normal.isChecked()

        if normal_distribution:
            mean = (max_value + min_value) / 2
            std_dev = (max_value - min_value) / 4
            random_numbers = np.random.normal(mean, std_dev, count)
        else:
            if allow_repeat:
                random_numbers = [round(random.uniform(min_value, max_value), decimals) for _ in range(count)]
            else:
                if count > max_value - min_value:
                    self.text_area.setText("Error: Cannot generate non-repeating numbers more than the range.")
                    return
                random_numbers = random.sample(range(int(min_value), int(max_value) + 1), count)
                random_numbers = [round(num + random.uniform(0, 1), decimals) for num in random_numbers]

        self.text_area.setText("Generated Random Numbers:\n" + ', '.join(str(num) for num in random_numbers))

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # 绘制直方图
        ax.hist(random_numbers, bins='auto', density=True, alpha=0.6, color='g')

        # 绘制正态分布曲线
        xmin, xmax = min(random_numbers), max(random_numbers)
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, np.mean(random_numbers), np.std(random_numbers))
        ax.plot(x, p, 'k', linewidth=2)

        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
