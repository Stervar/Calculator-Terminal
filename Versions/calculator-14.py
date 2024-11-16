from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import ast
import operator
import math

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

    def safe_eval(self, expression):
        try:
            expression = self.preprocess_expression(expression)
            parsed = ast.parse(expression, mode='eval')
            result = self.eval_node(parsed.body)
            return result
        except Exception as e:
            return f"Ошибка: {str(e)}"

    def preprocess_expression(self, expression):
        expression = expression.replace('^', '**')
        new_expression = ""
        for i, char in enumerate(expression):
            if char == '(' and i > 0 and expression[i - 1].isdigit():
                new_expression += '*'
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
        else:
            raise TypeError(f"Неподдерживаемый узел: {type(node)}")

class CalculatorApp(App):
    def build(self):
        self.calculator = UniversalCalculator()
        self.layout = GridLayout(cols=1)

        self.input_box = TextInput(multiline=False, font_size=55, size_hint_y=None, height=100)
        self.layout.add_widget(self.input_box)

        self.result_label = Label(text="", font_size=55, size_hint_y=None, height=100)
        self.layout.add_widget(self.result_label)

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C'
        ]

        grid = GridLayout(cols=4)
        for button in buttons:
            grid.add_widget(Button(text=button, on_press=self.on_button_press))

        self.layout.add_widget(grid)
        return self.layout

    def on_button_press(self, instance):
        current = self.input_box.text
        button_text = instance.text

        if button_text == "C":
            self.input_box.text = ""
            self.result_label.text = ""
        elif button_text == "=":
            try:
                result = self.calculator.safe_eval(current)
                self.result_label.text = str(result)
            except Exception as e:
                self.result_label.text = f"Ошибка: {str(e)}"
        else:
            self.input_box.text += button_text

if __name__ == "__main__":
    CalculatorApp().run()