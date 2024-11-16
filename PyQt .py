import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout, QLineEdit

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор")
        self.setGeometry(100, 100, 300, 400)

        self.result = QLineEdit()
        self.result.setReadOnly(True)

        layout = QGridLayout()
        layout.addWidget(self.result, 0, 0, 1, 4)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('C', 4, 1), ('=', 4, 2), ('+', 4, 3)
        ]

        for (text, row, col) in buttons:
            button = QPushButton(text)
            button.clicked.connect(lambda checked, b=text: self.on_button_click(b))
            layout.addWidget(button, row, col)

        self.setLayout(layout)

    def on_button_click(self, char):
        if char == 'C':
            self.result.clear()
        elif char == '=':
            try:
                self.result.setText(str(eval(self.result.text())))
            except Exception:
                self.result.setText("Ошибка")
        else:
            self.result.setText(self.result.text() + char)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())