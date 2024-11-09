import curses
import math
import re
import ast
import operator
import cmath  # Для комплексных чисел

class UltraAdvancedSafeCalculator:
    SAFE_FUNCTIONS = {
        # Основные математические функции
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
        'sinh': math.sinh,
        'cosh': math.cosh,
        'tanh': math.tanh,
        
        # Расширенные тригонометрические функции
        'sec': lambda x: 1 / math.cos(x),
        'csc': lambda x: 1 / math.sin(x),
        'cot': lambda x: 1 / math.tan(x),
        
        # Гиперболические обратные функции
        'asinh': math.asinh,
        'acosh': math.acosh,
        'atanh': math.atanh,
        
        # Экспоненциальные и логарифмические функции
        'exp': math.exp,
        'log': math.log,
        'log10': math.log10,
        'log2': math.log2,
        'ln': math.log,  # Натуральный логарифм
        
        # Корни и степени
        'sqrt': math.sqrt,
        'pow': pow,
        'cbrt': lambda x: math.copysign(math.pow(abs(x), 1/3), x),
        
        # Округление
        'ceil': math.ceil,
        'floor': math.floor,
        'trunc': math.trunc,
        
        # Специальные функции
        'factorial': math.factorial,
        🇷🇺 🇬🇧 
        # Комплексные числа
        'complex': complex,
        'real': lambda x: complex(x).real,
        'imag': lambda x: complex(x).imag,
        
        # Константы
        'pi': math.pi,
        'e': math.e,
        'tau': math.tau,
        'inf': float('inf'),
        
        # Статистические функции
        'degrees': math.degrees,
        'radians': math.radians
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
            # Расширенная предобработка
            expression = cls.preprocess_expression(expression)
            
            # Парсинг и вычисление
            parsed = ast.parse(expression, mode='eval')
            result = cls.eval_node(parsed.body)
            
            # Обработка результата
            return cls.format_result(result)
        
        except Exception as e:
            return f"Ошибка: {cls.handle_error(e)}"

    @classmethod
    def eval_node(cls, node):
        # [Предыдущая реализация с небольшими улучшениями]
        # Добавить обработку комплексных чисел
        # Добавить более строгую проверку типов
        pass

    @classmethod
    def preprocess_expression(cls, expression):
        # Расширенная предобработка
        expression = expression.replace('^', '**')
        expression = expression.replace('√', 'sqrt')
        
        # Улучшенное неявное умножение
        expression = re.sub(r'(\d+)([a-zA-Z(])', r'\1*\2', expression)
        expression = re.sub(r'([a-zA-Z)])(\d+)', r'\1*\2', expression)
        
        # Замена математических функций
        replacements = {
            'lg': 'log10',
            'ln': 'log',
            '∛': 'cbrt'
        }
        
        for old, new in replacements.items():
            expression = expression.replace(old, new)
        
        return expression

    @classmethod
    def format_result(cls, result):
        # Интеллектуальное форматирование результата
        if isinstance(result, float):
            # Округление больших чисел
            if abs(result) > 1e10 or abs(result) < 1e-10:
                return f"{result:.5e}"
            # Округление малых чисел
            return f"{result:.10f}".rstrip('0').rstrip('.')
        
        return str(result)

    @classmethod
    def handle_error(cls, error):
        # Расширенная обработка ошибок
        error_map = {
            ZeroDivisionError: "Деление на ноль",
            OverflowError: "Слишком большое число",
            ValueError: "Недопустимое математическое действие",
            TypeError: "Неверный тип данных"
        }
        
        for err_type, message in error_map.items():
            if isinstance(error, err_type):
                return message
        
        return str(error)

def draw_calculator_frame(stdscr, current_input, result):
    # [Ваш предыдущий код отрисовки]
    pass

def calculator(stdscr):
    curses.start_color()
    curses.curs_set(0)
    
    current_input = ""
    result = ""
    
    while True:
        draw_calculator_frame(stdscr, current_input, result)
        
        key = stdscr.getch()
        
        # Расширенная обработка клавиш
        if key == ord('q'):
            break
        
        # Добавлены новые возможности ввода
        elif key in [ord(c) for c in '0123456789.+-*/()√^j']:
            current_input += chr(key)
        
        elif key == ord('c') or key == ord('C'):
            current_input = ""
            result = ""
        
        elif key == 263 or key == 127:  # Backspace
            current_input = current_input[:-1]
        
        elif key == ord('=') or key == 10:  # Enter
            result = UltraAdvancedSafeCalculator.safe_eval(current_input)
            current_input = ""
        
        # Расширенные математические функции
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
        
        # Новые функции
        elif key == ord('t'):  # tan
            current_input += 'tan('
        elif key == ord('g'):  # log10
            current_input += 'log10('

def main():
    curses.wrapper(calculator)

if __name__ == "__main__":
    main()