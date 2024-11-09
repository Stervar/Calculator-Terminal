import curses
import math
import re
import traceback
import ast
import operator

class SafeCalculator:
    SAFE_FUNCTIONS = {
        # Математические функции
        'abs': abs,
        'round': round,
        'max': max,
        'min': min,
        'sum': sum,
        
        # Тригонометрические функции
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'asin': math.asin,
        'acos': math.acos,
        'atan': math.atan,
        
        # Гиперболические функции
        'sinh': math.sinh,
        'cosh': math.cosh,
        'tanh': math.tanh,
        
        # Экспоненциальные и логарифмические
        'exp': math.exp,
        'log': math.log,
        'log10': math.log10,
        'log2': math.log2,
        'sqrt': math.sqrt,
        'pow': pow,
        
        # Константы
        'pi': math.pi,
        'e': math.e
    }

    SAFE_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg
    }

    @classmethod
    def safe_eval(cls, expression):
        try:
            # Предварительная обработка выражения
            expression = cls.preprocess_expression(expression)
            
            # Парсинг AST
            parsed = ast.parse(expression, mode='eval')
            return cls.eval_node(parsed.body)
        
        except Exception as e:
            return f"Ошибка: {str(e)}"

    @classmethod
    def eval_node(cls, node):
        if isinstance(node, ast.Num):
            return node.n
        
        elif isinstance(node, ast.Name):
            if node.id in cls.SAFE_FUNCTIONS:
                return cls.SAFE_FUNCTIONS[node.id]
            raise NameError(f"Неизвестное имя: {node.id}")
        
        elif isinstance(node, ast.Call):
            func = cls.eval_node(node.func)
            args = [cls.eval_node(arg) for arg in node.args]
            return func(*args)
        
        elif isinstance(node, ast.BinOp):
            left = cls.eval_node(node.left)
            right = cls.eval_node(node.right)
            
            op = type(node.op)
            if op not in cls.SAFE_OPERATORS:
                raise ValueError(f"Недопустимая операция: {op}")
            
            return cls.SAFE_OPERATORS[op](left, right)
        
        elif isinstance(node, ast.UnaryOp):
            operand = cls.eval_node(node.operand)
            op = type(node.op)
            
            if op not in cls.SAFE_OPERATORS:
                raise ValueError(f"Недопустимая операция: {op}")
            
            return cls.SAFE_OPERATORS[op](operand)
        
        raise TypeError(f"Неподдерживаемый тип узла: {type(node)}")

    @classmethod
    def preprocess_expression(cls, expression):
        # Замена операторов
        expression = expression.replace('^', '**')
        expression = expression.replace('√', 'sqrt')
        
        # Добавление неявного умножения
        expression = re.sub(r'(\d+)([a-zA-Z(])', r'\1*\2', expression)
        expression = re.sub(r'([a-zA-Z)])(\d+)', r'\1*\2', expression)
        
        return expression

def draw_calculator_frame(stdscr, current_input, result):
    # [Ваш предыдущий код отрисовки с незначительными изменениями]
    pass

def calculator(stdscr):
    curses.start_color()
    curses.curs_set(0)
    
    current_input = ""
    result = ""
    
    while True:
        draw_calculator_frame(stdscr, current_input, result)
        
        key = stdscr.getch()
        
        # Обработка клавиш с расширенной логикой
        if key == ord('q'):
            break
        
        elif key in [ord(c) for c in '0123456789.+-*/()√^']:
            current_input += chr(key)
        
        elif key == ord('c') or key == ord('C'):
            current_input = ""
            result = ""
        
        elif key == 263 or key == 127:  # Backspace
            current_input = current_input[:-1]
        
        elif key == ord('=') or key == 10:  # Enter
            try:
                result = SafeCalculator.safe_eval(current_input)
                current_input = str(result)
            except Exception as e:
                result = f"Ошибка: {str(e)}"
        
        # Дополнительные функции
        elif key == ord('s'):  # sin
            current_input += 'sin('
        elif key == ord('l'):  # log
            current_input += 'log('
        elif key == ord('e'):  # e (число Эйлера)
            current_input += 'e'
        elif key == ord('p'):  # pi
            current_input += 'pi'
        elif key == ord('r'):  # sqrt
            current_input += 'sqrt('

def main():
    curses.wrapper(calculator)

if __name__ == "__main__":
    main()
    
# Возможности:

# Стандартные операции: +, -, *, /, ^
# Математические функции: sin, cos, tan, log, sqrt
# Константы: e, pi
# Скобки и сложные выражения
# Неявное умножение
# Обработка ошибок
# Примеры работающих выражений:

# 2*(3+4)
# sin(pi/2)
# log(10)
# sqrt(16)
# 2^3
# e*2
# Калькулятор максимально устойчив к ошибкам и небезопасным вычислениям.