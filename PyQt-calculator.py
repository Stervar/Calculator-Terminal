import sys
import math
import re
import ast
import operator
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QGridLayout, QLineEdit, QLabel
from PyQt5.QtGui import QFont

loading_text = [
    " ██████╗ █████╗ ██╗      ██████╗██╗   ██╗██╗      █████╗ ████████╗ ██████╗ ",
    "██╔════╝██╔══██╗██║     ██╔════╝██║   ██║██║     ██╔══██╗╚══██╔══╝██╔═══██╗",
    "██║     ███████║██║     ██║     ██║   ██║██║     ███████║   ██║   ██║   ██║",
    "██║     ██╔══██║██║     ██║     ██║   ██║██║     ██╔══██║   ██║   ██║   ██║",
    "╚██████╗██║  ██║███████╗╚██████╗╚██████╔╝███████╗██║  ██║   ██║   ╚██████╔╝",
    " ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ "
]

class UltraAdvancedSafeCalculator:
    SAFE_FUNCTIONS = {
        'abs': abs,
        'round': round,
        'max': max,
        'min': min,
        'sum': sum,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'sqrt': math.sqrt,
        'log': math.log,
        'exp': math.exp,
        'pi': math.pi,
        'e': math.e,
    }

    SAFE_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos
    }

    @classmethod
    def safe_eval(cls, expression):
        try:
            expression = cls.preprocess_expression(expression)
            if not re.match(r'^[0-9+\-*/().,a-zA-Z\s]+$', expression):
                return "Недопустимые символы в выражении"
            parsed = ast.parse(expression, mode='eval')
            result = cls.eval_node(parsed.body)
            return cls.format_result(result)
        except Exception as e:
            return f"Ошибка: {str(e)}"

    @classmethod
    def preprocess_expression(cls, expression):
        expression = expression.replace('^', '**')
        return expression

    @classmethod
    def eval_node(cls, node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            left = cls.eval_node(node.left)
            right = cls.eval_node(node.right)
            op = cls.SAFE_OPERATORS.get(type(node.op))
            return op(left, right)
        elif isinstance(node, ast.Call):
            func_name = node.func.id
            func = cls.SAFE_FUNCTIONS.get(func_name)
            if func:
                args = [cls.eval_node(arg) for arg in node.args]
                return func(*args)
            raise ValueError(f"Неподдерживаемая функция: {func_name}")
        raise ValueError("Неподдерживаемый тип узла")

    @classmethod
    def format_result(cls, result):
        if isinstance(result, float):
            return f"{result:.10f}".rstrip('0').rstrip('.')
        return str(result)

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор")
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet("background-color: #2E2E2E; color: white;")

        font_title = QFont("Courier", 10)  # Шрифт для заголовка
        font = QFont("Arial", 20)  # Шрифт для кнопок и поля ввода

        # Заголовок
        self.title_label = QLabel("\n".join(loading_text))
        self.title_label.set Font(font_title)
        self.title_label.setStyleSheet("color: white;")
        self.title_label.setWordWrap(True)

        self.result = QLineEdit()
        self.result.setReadOnly(True)
        self.result.setFont(font)
        self.result.setStyleSheet("background-color: #1E1E1E; color: white; padding: 10px; border-radius: 5px;")

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.result)

        buttons_layout = QGridLayout()
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('C', 3, 1), ('=', 3, 2), ('+', 3, 3)
        ]

        for (text, row, col) in buttons:
            button = QPushButton(text)
            button.setFont(font)
            button.setStyleSheet("background-color: #4C4C4C; color: white; padding: 20px; border-radius: 5px;")
            button.clicked.connect(lambda checked, b=text: self.on_button_click(b))
            buttons_layout.addWidget(button, row, col)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def on_button_click(self, char):
        if char == 'C':
            self.result.clear()
        elif char == '=':
            try:
                expression = self.result.text()
                result = UltraAdvancedSafeCalculator.safe_eval(expression)
                self.result.setText(result)
            except Exception:
                self.result.setText("Ошибка")
        else:
            self.result.setText(self.result.text() + char)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())