import ast
import operator
import math
import tkinter as tk
from tkinter import messagebox

class UniversalCalculator:
    SAFE_FUNCTIONS = {
        'abs': abs,
        'round': round,
        'max': max,
        'min': min,
        'sum': sum,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'asin': math.asin,
        'acos': math.acos,
        'atan': math.atan,
        'sinh': math.sinh,
        'cosh': math.cosh,
        'tanh': math.tanh,
        'exp': math.exp,
        'log': math.log,
        'log10': math.log10,
        'log2': math.log2,
        'sqrt': math.sqrt,
        'pow': pow,
        'pi': math.pi,
        'e': math.e,
        'inf': float('inf'),
        'i': complex(0, 1),
    }

    SAFE_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.BitAnd: operator.and_,
        ast.BitOr: operator.or_,
        ast.BitXor: operator.xor,
        ast.LShift: operator.lshift,
        ast.RShift: operator.rshift,
    }

    def __init__(self):
        self.variables = {}

    def set_variable(self, name, value):
        self.variables[name] = value

    def get_variable(self, name):
        return self.variables.get(name, None)

    def safe_eval(self, expression):
        try:
            expression = self.preprocess_expression(expression)
            parsed = ast.parse(expression, mode='eval')
            result = self.eval_node(parsed.body)
            return self.format_result(result)
        except Exception as e:
            return f"Ошибка: {str(e)}"

    def preprocess_expression(self, expression):
        expression = expression.replace('^', '**')
        
        # Заменяем все случаи, когда число предшествует открывающей скобке, на умножение
        new_expression = ""
        for i, char in enumerate(expression):
            if char == '(' and i > 0 and expression[i - 1].isdigit():
                new_expression += '*'  # Добавляем оператор умножения
            new_expression += char
        return new_expression

    def eval_node(self, node):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            left = self.eval_node(node.left)
            right = self.eval_node(node.right)
            return self.SAFE_OPERATORS[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = self.eval_node(node.operand)
            return operator.neg(operand) if isinstance(node.op, ast.USub) else operator.pos(operand)
        elif isinstance(node, ast.Name):
            value = self.get_variable(node.id)
            if value is None:
                raise ValueError(f"Переменная '{node.id}' не определена")
            return value
        elif isinstance(node, ast.Call):
            func = self.SAFE_FUNCTIONS.get(node.func.id)
            if not func:
                raise ValueError(f"Функция {node.func.id} не поддерживается")
            args = [self.eval_node(arg) for arg in node.args]
            return func(*args)
        else:
            raise TypeError(f"Неподдерживаемый узел: {type(node)}")

    def format_result(self, result):
        return f"Результат: {result}"

class CalculatorApp:
    def __init__(self, root):
        self.calculator = UniversalCalculator()
        self.root = root
        self.root.title("Универсальный Калькулятор")

        self.expression_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        entry = tk.Entry(self.root, textvariable=self.expression_var, width=40)
        entry.grid(row=0, column=0, padx=10, pady=10)

        calculate_button = tk.Button(self.root, text="Вычислить", command=self.calculate)
        calculate_button.grid(row=0, column=1, padx=10, pady=10)

        self.result_label = tk.Label(self.root, text="", width=40)
        self.result_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def calculate(self):
        expression = self.expression_var.get()
        result = self.calculator.safe_eval(expression)
        self.result_label.config(text=result)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()