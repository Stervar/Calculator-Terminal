import curses
import math
import re

def safe_eval(expression):
    """
    Безопасное вычисление математических выражений с расширенной обработкой
    """
    try:
        # Заменяем математические функции на безопасные
        expression = expression.replace('^', '**')
        expression = expression.replace('√', 'sqrt')
        
        # Словарь разрешенных функций
        safe_dict = {
            'abs': abs,
            'round': round,
            'max': max,
            'min': min,
            'sum': sum,
            'pow': pow,
            'sqrt': math.sqrt,
            'log': math.log,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'pi': math.pi,
            'e': math.e
        }
        
        # Проверка корректности скобок
        if not is_balanced_parentheses(expression):
            return "Ошибка скобок"
        
        # Проверка на недопустимые символы
        if not re.match(r'^[0-9+\-*/().,\s\^√logstanpie]+$', expression):
            return "Недопустимые символы"
        
        # Предобработка выражения для неявного умножения
        expression = handle_implicit_multiplication(expression)
        
        # Безопасное вычисление
        result = eval(expression, {"__builtins__": None}, safe_dict)
        
        return str(round(result, 10))  # Округление до 10 знаков
    
    except SyntaxError:
        return "Синтаксическая ошибка"
    except ZeroDivisionError:
        return "Деление на ноль"
    except Exception as e:
        return f"Ошибка: {str(e)}"

def is_balanced_parentheses(expression):
    """
    Проверка сбалансированности скобок
    """
    stack = []
    for char in expression:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0

def handle_implicit_multiplication(expression):
    """
    Обработка неявного умножения
    """
    # Добавление * между числом и скобкой
    expression = re.sub(r'(\d+)(\()', r'\1*\2', expression)
    # Добавление * между скобкой и числом
    expression = re.sub(r'(\))(\d+)', r'\1*\2', expression)
    return expression

def calculator(special_keys):
    # Отключаем курсор
    curses.curs_set(0)
    
    # Очистка экрана
    special_keys.clear()
    
    # Начальные переменные
    current_input = ""
    result = ""
    
    while True:
        # Отрисовка основного интерфейса
        draw_calculator_frame(stdscr, current_input, result)
        
        # Получение нажатия клавиши
        key = stdscr.getch()
        
        # Обработка клавиш
        if key == ord('q') or key == 27:  # q или Esc
            break
        
        elif key == ord('c') or key == ord('C'):  # Полная очистка
            current_input = ""
            result = ""
        
        elif key == 127 or key == curses.KEY_BACKSPACE:  # Backspace
            current_input = current_input[:-1]
        
        elif key == ord('=') or key == 10:  # Enter или =
            result = safe_eval(current_input)
            current_input = ""
        
        # Обработка цифр и операций
        elif chr(key) in '0123456789+-*/().,^√':
            current_input += chr(key)
        
        # Обновление экрана
        stdscr.refresh()

def draw_calculator_frame(framework, current_input, result):
    # Получаем размеры экрана
    height, width = framework
    # Определяем начальные координаты
    start_y = 2
    start_x = 2
    
    # Основная рамка калькулятора 
    frame = [
        "╔═══════════════════════════════════════════════════╗",
        "║                  КАЛЬКУЛЯТОР                      ║",
        "╠═══════════════════════════════════════════════════╣",
        "║ Ввод:                                    Результат║",
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
        "║ Backspace - удаляет символ | CE - удаляет число   ║",
        "║ C - полная очистка | Расширенные функции          ║",
        "╚═══════════════════════════════════════════════════╝"
    ]

    # Отрисовка рамки
    for idx, line in enumerate(frame):
        framework.addstr(start_y + idx, start_x, line)

    # Отображение ввода
    framework.addstr(start_y + 3, start_x + 7, current_input)
    
    # Отображение результата
    if result:
        framework.addstr(start_y + 3, start_x + 40, result)

def main():
    # Инициализация curses
    something = curses.initscr()
    
    try:
        # Настройки curses
        curses.noecho()
        curses.cbreak()
        something.keypad(True)
        
        # Запуск калькулятора
        calculator(something)
    
    finally:
        # Восстановление настроек терминала
        curses.nocbreak()
        something.keypad(False)
        curses.echo()
        curses.endwin()

if __name__ == "__main__":
    main()