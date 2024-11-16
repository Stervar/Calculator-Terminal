import sys
import math
import re
import ast
import operator
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QGridLayout, QLineEdit
from PyQt5.QtGui import QFont

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

        font = QFont("Arial", 20)

        self.result = QLineEdit()
        self.result.setReadOnly(True)
        self.result.setFont(font)
        self.result.setStyleSheet("background-color: #1E1E1E; color: white; padding: 10px; border-radius: 5px;")
        
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
            button.setFont(font)
            button.setStyleSheet("background-color: #4C4C4C; color: white; padding: 20px; border-radius: 5px;")
            button.clicked.connect(lambda checked, b=text: self .on_button_click(b))
            layout.addWidget(button, row, col)

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