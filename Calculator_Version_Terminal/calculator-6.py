import curses  # Импортируем библиотеку curses для работы с консольным интерфейсом
import math  # Импортируем библиотеку math для математических операций
import re  # Импортируем библиотеку re для работы с регулярными выражениями

def safe_eval(expression):
    """
    Безопасное вычисление математических выражений с расширенной обработкой.

    Args:
        expression: Строка, представляющая математическое выражение.

    Returns:
        Результат вычисления в виде строки или сообщение об ошибке.
    """
    try:
        # Заменяем математические функции на безопасные
        expression = expression.replace('^', '**')  # Заменяем ^ на **
        expression = expression.replace('√', 'sqrt')  # Заменяем √ на sqrt
        
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
            return "Ошибка скобок"  # Возвращаем сообщение об ошибке, если скобки не сбалансированы
        
        # Проверка на недопустимые символы
        if not re.match(r'^[0-9+\-*/().,\s\^√logstanpie]+$', expression):
            return "Недопустимые символы"  # Возвращаем сообщение об ошибке, если есть недопустимые символы
        
        # Предобработка выражения для неявного умножения
        expression = handle_implicit_multiplication(expression)
        
        # Безопасное вычисление
        result = eval(expression, {"__builtins__": None}, safe_dict)  # Используем eval с ограниченным контекстом
        
        return str(round(result, 10))  # Округление до 10 знаков
    
    except SyntaxError:
        return "Синтаксическая ошибка"  # Возвращаем сообщение об ошибке при синтаксической ошибке
    except ZeroDivisionError:
        return "Деление на ноль"  # Возвращаем сообщение об ошибке при делении на ноль
    except Exception as e:
        return f"Ошибка: {str(e)}"  # Возвращаем сообщение об ошибке для других исключений

def is_balanced_parentheses(expression):
    """
    Проверка сбалансированности скобок.

    Args:
        expression: Строка, представляющая математическое выражение.

    Returns:
        True, если скобки сбалансированы, иначе False.
    """
    stack = []  # Стек для отслеживания открывающих скобок
    for char in expression:
        if char == '(':
            stack.append(char)  # Добавляем открывающую скобку в стек
        elif char == ')':
            if not stack:
                return False  # Если закрывающая скобка без соответствующей открывающей, возвращаем False
            stack.pop()  # Удаляем последнюю открывающую скобку из стека
    return len(stack) == 0  # Возвращаем True, если стек пуст (все скобки сбалансированы)

def handle_implicit_multiplication(expression):
    """
    Обработка неявного умножения в выражении.

    Args:
        expression: Строка, представляющая математическое выражение.

    Returns:
        Строка с добавленным явным умножением.
    """
    # Добавление * между числом и скобкой
    expression = re.sub(r'(\d+)(\()', r'\1*\2', expression)
    # Добавление * между скобкой и числом
    expression = re.sub(r'(\))(\d+)', r'\1*\2', expression)
    return expression  # Возвращаем обработанное выражение

def draw_calculator_frame(framework, current_input, result):
    """
    Отрисовка рамки калькулятора.

    Args:
        framework: Объект curses, предоставляющий доступ к консольному интерфейсу.
        current_input: Текущее введенное пользователем выражение.
        result: Результат вычислений.

    Returns:
        None.
    """
    try:
        # Получаем размеры экрана
        height, width = framework.getmaxyx()
        
        # Определяем начальные координаты
        start_y = 2
        start_x =  2
        
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
            framework.addstr(start_y + idx, start_x, line)  # Выводим каждую строку рамки на заданную позицию

        # Отображение ввода
        framework.addstr(start_y + 3, start_x + 7, current_input)  # Выводим текущее введенное выражение
        
        # Отображение результата
        if result:
            framework.addstr(start_y + 3, start_x + 40, result)  # Выводим результат вычислений

    except Exception as e:
        framework.clear()  # Очищаем экран в случае ошибки
        framework.addstr(0, 0, f"Ошибка отрисовки: {str(e)}")  # Выводим сообщение об ошибке

def calculator(special_keys):
    """
    Основная функция калькулятора, обрабатывающая ввод и вычисления.

    Args:
        special_keys: Объект curses, предоставляющий доступ к клавиатурному вводу.

    Returns:
        None.
    """
    # Отключаем курсор
    curses.curs_set(0)  # Скрываем курсор
    
    # Очистка экрана
    special_keys.clear()  # Очищаем экран
    
    # Начальные переменные
    current_input = ""  # Переменная для хранения текущего ввода
    result = ""  # Переменная для хранения результата вычислений
    
    while True:
        # Отрисовка основного интерфейса
        draw_calculator_frame(special_keys, current_input, result)  # Отрисовываем интерфейс калькулятора
        special_keys.refresh()  # Обновляем экран
        
        # Получение нажатия клавиши
        key = special_keys.getch()  # Чтение нажатой клавиши
        
        # Обработка клавиш
        if key == ord('q') or key == 27:  # Выход при нажатии 'q' или Esc
            break
        
        elif key == ord('c') or key == ord('C'):  # Полная очистка
            current_input = ""  # Очищаем текущий ввод
            result = ""  # Очищаем результат
        
        elif key == 127 or key == curses.KEY_BACKSPACE:  # Backspace
            current_input = current_input[:-1]  # Удаляем последний символ из текущего ввода
        
        elif key == ord('=') or key == 10:  # Нажатие Enter или '='
            result = safe_eval(current_input)  # Вычисляем результат
            current_input = ""  # Очищаем ввод после получения результата
        
        # Обработка цифр и операций
        elif chr(key) in '0123456789.+-*/()√^':  # Если нажата цифра или оператор
            current_input += chr(key)  # Добавляем символ к текущему вводу

def main():
    """
    Инициализация и запуск калькулятора.

    Returns:
        None.
    """
    # Инициализация curses
    special_keys = curses.initscr()  # Инициализируем экран для работы с curses
    
    try:
        # Настройки curses
        curses.noecho()  # Отключаем отображение вводимых символов
        curses.cbreak()  # Включаем режим немедленного ввода
        special_keys.keypad(True)  # Включаем поддержку специальных клавиш
        
        # Запуск калькулятора
        calculator(special_keys)  # Запускаем основную функцию калькулятора
    
    except KeyboardInterrupt:
        print("Работа калькулятора прервана пользователем.")  # Обработка прерывания работы калькулятора
    
    except Exception as e:
        print(f"Произошла ошибка: {e}")  # Обработка других исключений
    
    finally:
        # Восстановление настроек терминала
        curses.nocbreak()  # Отключаем режим немедленного ввода
        special_keys.keypad(False)  # Отключаем поддержку специальных клавиш
        curses.echo()  # Включаем отображение вводимых символов
        curses.endwin()  # Завершаем работу с curses

if __name__ == "__main__":
    main()  # Запускаем программу