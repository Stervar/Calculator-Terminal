import curses
import math
import re
import ast
import operator
import cmath
import time

# ASCII-арт надписи
loading_text = [
    " ██████╗ █████╗ ██╗      ██████╗██╗   ██╗██╗      █████╗ ████████╗ ██████╗ ",
    "██╔════╝██╔══██╗██║     ██╔════╝██║   ██║██║     ██╔══██╗╚══██╔══╝██╔═══██╗",
    "██║     ███████║██║     ██║     ██║   ██║██║     ███████║   ██║   ██║   ██║",
    "██║     ██╔══██║██║     ██║     ██║   ██║██║     ██╔══██║   ██║   ██║   ██║",
    "╚██████╗██║  ██║███████╗╚██████╗╚██████╔╝███████╗██║  ██║   ██║   ╚██████╔╝",
    " ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ "
]

creator_text = [
    "Калькулятор создан Sterva",
    "С любовью к программированию"
]

# Весь класс UltraAdvancedSafeCalculator остается прежним (как в предыдущей версии)
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

            # Проверка на допустимые символы
            if not re.match(r'^[0-9+\-*/().,a-zA-Z\s]+$', expression):
                return "Недопустимые символы в выражении"

            # Парсинг и вычисление
            parsed = ast.parse(expression, mode='eval')
            result = cls.eval_node(parsed.body)

            # Обработка результата
            formatted_result = cls.format_result(result)
            return formatted_result

        except SyntaxError:
            return "Синтаксическая ошибка в выражении"

        except Exception as e:
            return f"Ошибка вычисления: {cls.handle_error(e)}"
    
    @classmethod
    def format_result(cls, result):
    # Интеллектуальное форматирование результата
        if isinstance(result, (int, float)):
            # Округление больших чисел
            if abs(result) > 1e10 or abs(result) < 1e-10:
                return f"{result:.5e}"
        
            # Округление для чисел с плавающей точкой
            if isinstance(result, float):
                return f"{result:.10f}".rstrip('0').rstrip('.')
        
            return str(result)
    
        return str(result)

    @classmethod
    def preprocess_expression(cls, expression):
        # Расширенная предобработка
        expression = expression.replace('^', '**')  # Степень
        expression = expression.replace('√', 'sqrt')  # Квадратный корень
        expression = expression.replace('×', '*')  # Умножение
        expression = expression.replace('÷', '/')  # Деление
    
        # Замена математических функций
        replacements = {
            'lg': 'log10',   # Десятичный логарифм
            'ln': 'log',     # Натуральный логарифм
            '∛': 'cbrt'      # Кубический корень
    }
    
        for old, new in replacements.items():
            expression = expression.replace(old, new)
    
    # Неявное умножение
        expression = re.sub(r'(\d+)([a-zA-Z(])', r'\1*\2', expression)
        expression = re.sub(r'([a-zA-Z)])(\d+)', r'\1*\2', expression)
    
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
    
    @classmethod
    def eval_node(cls, node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            left = cls.eval_node(node.left)
            right = cls.eval_node(node.right)
            op = cls.SAFE_OPERATORS.get(type(node.op))
            if op:
                return op(left, right)
            
            raise ValueError(f"Неподдерживаемая операция: {type(node.op)}")
        elif isinstance(node, ast.UnaryOp):
            operand = cls.eval_node(node.operand)
            op = cls.SAFE_OPERATORS.get(type(node.op))
            if op:
                return op(operand)
            
            raise ValueError(f"Неподдерживаемая унарная операция: {type(node.op)}")
        elif isinstance(node, ast.Call):
            func_name = node.func.id
            func = cls.SAFE_FUNCTIONS.get(func_name)
            if func:
                args = [cls.eval_node(arg) for arg in node.args]
                return func(*args)
            raise ValueError(f"Неподдерживаемая функция: {func_name}")
        elif isinstance(node, ast.Name):
        
        # Обработка констант и переменных
            const = cls.SAFE_FUNCTIONS.get(node.id)
            if const is not None:
                return const
            raise ValueError(f"Неизвестная переменная: {node.id}")
        else:
            raise ValueError(f"Неподдерживаемый тип узла: {type(node)}")

def draw_loading_screen(stdscr):
    """
    Отрисовка загрузочного экрана
    """
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

    curses.curs_set(0)  # Скрываем курсор
    stdscr.clear()
    
    # Получаем размеры экрана
    height, width = stdscr.getmaxyx()
    
    # Центрирование надписи
    def draw_centered_text(text_lines, start_row):
        for i, line in enumerate(text_lines):
            x = (width - len(line)) // 2
            stdscr.addstr(start_row + i, x, line, curses.color_pair(1))

    # Отрисовка больших надписей
    draw_centered_text(loading_text, height // 4)
    draw_centered_text(creator_text, height - 10)

    stdscr.refresh()
    time.sleep(2)

def draw_calculator_frame(framework, current_input, result):
    try:
        # Получаем размеры экрана
        height, width = framework.getmaxyx()

        # Проверяем минимальный размер окна
        if height < 30 or width < 150:
            framework.clear()
            framework.addstr(height // 2, 0, "Увеличьте размер окна терминала!")
            framework.refresh()
            return

        # Рассчитываем позицию для центрирования
        calc_width = 60
        start_x = max(0, (width - calc_width) // 2)
        start_y = max(0, (height - 24) // 2)

        # Добавляем статичную надпись сверху
        for idx, line in enumerate(loading_text):
            x = (width - len(line)) // 2
            framework.addstr(1 + idx, x, line)  # Фиксированное положение сверху

        # Инструкции слева с рамкой
        instructions_left = [
            "╔═══════════════════════════════════╗",
            "║       ✦  ДОПОЛНИТЕЛЬНО  ✦         ║",
            "╠═══════════════════════════════════╣",
            "║ Кнопки    Действие                ║",
            "╠═══════════════════════════════════╣",
            "║ 1-9,0     Ввод цифр               ║",
            "║ +−×÷      Мат. операции           ║",
            "║ =         Результат               ║",
            "║ C         Очистка экрана          ║",
            "║ ←         Удаление символа        ║",
            "║ ±         Смена знака             ║",
            "╚═══════════════════════════════════╝"
        ]

        # Инструкции справа с рамкой
        instructions_right = [
            "╔═══════════════════════════════════╗",
            "║       ✦  ДОПОЛНИТЕЛЬНО   ✦        ║",
            "╠═══════════════════════════════════╣",
            "║ Кнопки    Действие                ║",
            "╠═══════════════════════════════════╣",
            "║ ( )       Скобки                  ║",
            "║ .         Десятичная дробь        ║",
            "║ 1/x       Обратное число          ║",
            "║ x²        Возведение в квадрат    ║",
            "║ √         Квадратный корень       ║",
            "║ log       Логарифм                ║",
            "║ e         Число Эйлера            ║",
            "╚═══════════════════════════════════╝"
        ]

        # Отрисовка левых инструкций
        for i, line in enumerate(instructions_left):
            framework.addstr(start_y + i, start_x - 45, line)

        # Отрисовка правых инструкций
        for i, line in enumerate(instructions_right):
            framework.addstr(start_y + i, start_x + calc_width + 1, line)

        # Основная рамка калькулятора
        frame = [
            "╔═══════════════════════════════════════════════════╗",
            "║              ✦    КАЛЬКУЛЯТОР     ✦               ║",
            "╠═══════════════════════════════════════════════════╣",
            "║ Ввод:                                             ║",
            "╠═══════════════════════════════════════════════════╣",
            "║   7    │    8    │    9    │    /    │    CE      ║",
            "║--------+---------+---------+---------+------------║",
            "║   4    │    5    │    6    │    *    │    √       ║",
            "║--------+---------+---------+---------+------------║",
            "║   1    │    2    │    3    │    -    │    %       ║",
            "║--------+---------+---------+---------+------------║",
            "║   0    │    .    │    +    │ x²  │ 1/x │ ±        ║",
            "║--------+---------+---------+---------+------------║",
            "║   log  │    e    │    ^    │    (   │    )        ║",
            "╠═══════════════════════════════════════════════════╣",
            "║    ←   Удаление символа - удаляет один символ     ║",
            "║               C - Полная очистка                  ║",
            "╚═══════════════════════════════════════════════════╝"
        ]

        for idx, line in enumerate(frame):
            framework.addstr(start_y + idx, start_x, line)

        framework.addstr(start_y + 3, start_x + 7, current_input)

        if result:
            framework.addstr(start_y + 3, start_x + 35, f"Результат: {result}")

        framework.refresh()

    except Exception as e:
        framework.clear()
        framework.addstr(0, 0, f"Произошла ошибка: {str(e)}")
        framework.refresh()

def calculator(special_keys):
    # Инициализация curses
    stdscr = curses.initscr()
    
    # Проверка поддержки цветов
    if not curses.has_colors():
        curses.endwin()
        print("Ваш терминал не поддерживает цвета")
        return

    # Включение цветов
    curses.start_color()
    
    # Безопасная инициализация пары цветов
    try:
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    except:
        pass

    curses.curs_set(0)

    current_input = ""
    result = ""

    while True:
        draw_calculator_frame(stdscr, current_input, result)
        key = stdscr.getch()

        if key in special_keys['exit']:
            break
        elif key == 10 or key == ord('='):  # Enter или "=" для вычисления
            result = UltraAdvancedSafeCalculator.safe_eval(current_input)
        elif key in special_keys['clear']:
            current_input = ""
            result = ""
        elif key in special_keys['delete']:
            current_input = current_input[:-1]
        elif key == ord('c') or key == ord('C'):  # Полная очистка
            current_input = ""
            result = ""
        elif chr(key) in '0123456789+-*/().,^√×÷':
            current_input += chr(key)
        elif key == ord('s'):  # Квадратный корень
            current_input += '√'
        elif key == ord('l'):  # Логарифм
            current_input += 'log'
        elif key == ord('e'):  # Число Эйлера
            current_input += 'e'

    curses.endwin()
    
if __name__ == "__main__":
    special_keys = {
        'exit': [ord('q'), ord('Q')],
        'clear': [curses.KEY_DC],
        'delete': [curses.KEY_BACKSPACE]
    }
    calculator(special_keys)