import curses  # Импортируем библиотеку curses для работы с консольным интерфейсом
import math  # Импортируем библиотеку math для математических операций
import re  # Импортируем библиотеку re для работы с регулярными выражениями
import ast  # Импортируем библиотеку для работы с абстрактным синтаксическим деревом (AST)
import operator  # Импортируем библиотеку для работы с операциями
import cmath  # Импортируем библиотеку для работы с комплексными числами

class UltraAdvancedSafeCalculator:
    """
    Класс для безопасного вычисления математических выражений.
    """
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
        'sec': lambda x: 1 / math.cos(x),  # Секанс
        'csc': lambda x: 1 / math.sin(x),  # Котангенс
        'cot': lambda x: 1 / math.tan(x),  # Косеканс
        
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
        'cbrt': lambda x: math.copysign(math.pow(abs(x), 1/3), x),  # Кубический корень
        
        # Округление
        'ceil': math.ceil,
        'floor': math.floor,
        'trunc': math.trunc,
        
        # Специальные функции
        'factorial': math.factorial,

        # Комплексные числа
        'complex': complex,
        'real': lambda x: complex(x).real,  # Извлечение действительной части
        'imag': lambda x: complex(x).imag,  # Извлечение мнимой части
        
        # Константы
        'pi': math.pi,
        'e': math.e,
        'tau': math.tau,
        'inf': float('inf'),  # Бесконечность
        
        # Статистические функции
        'degrees': math.degrees,
        'radians': math.radians
    }

    SAFE_OPERATORS = {
        ast.Add: operator.add,  # Оператор сложения
        ast.Sub: operator.sub,  # Оператор вычитания
        ast.Mult: operator.mul,  # Оператор умножения
        ast.Div: operator.truediv,  # Оператор деления
        ast.Pow: operator.pow,  # Оператор возведения в степень
        ast.USub: operator.neg,  # Унарный оператор отрицания
        ast.UAdd: operator.pos  # Унарный оператор положительного значения
    }

    @classmethod
    def safe_eval(cls, expression):
        """
        Безопасная оценка математического выражения.

        Args:
            expression: Строка, представляющая математическое выражение.

        Returns:
            Результат вычисления или сообщение об ошибке.
        """
        try:
            # Расширенная предобработка
            expression = cls.preprocess_expression(expression)  # Обработка выражения перед парсингом
            
            # Проверка на допустимые символы
            if not re.match(r'^[0-9+\-*/().,a-zA-Z\s]+$', expression):
                return "Недопустимые символы в выражении"  # Сообщение об ошибке для недопустимых символов
            
            # Парсинг и вычисление
            parsed = ast.parse(expression, mode='eval')  # Парсинг выражения в AST
            result = cls.eval_node(parsed.body)  # Оценка корневого узла AST
            
            # Обработка результата ```python
            return cls.format_result(result)  # Форматирование результата перед возвратом
            
        except SyntaxError:
            return "Синтаксическая ошибка"  # Сообщение об ошибке для синтаксических ошибок
        except Exception as e:
            return f"Ошибка: {cls.handle_error(e)}"  # Возврат сообщения об ошибке

    @classmethod
    def preprocess_expression(cls, expression):
        """
        Предварительная обработка математического выражения.

        Args:
            expression: Строка, представляющая математическое выражение.

        Returns:
            Обработанное выражение.
        """
        # Замена операторов
        expression = expression.replace('^', '**')  # Замена ^ на **
        expression = expression.replace('√', 'sqrt')  # Замена √ на sqrt
        expression = expression.replace('×', '*')  # Замена × на *
        expression = expression.replace('÷', '/')  # Замена ÷ на /
    
        # Добавление неявного умножения
        expression = re.sub(r'(\d+)([a-zA-Z(])', r'\1*\2', expression)  # Добавление * между числом и скобкой
        expression = re.sub(r'([a-zA-Z)])(\d+)', r'\1*\2', expression)  # Добавление * между скобкой и числом
    
        # Замена математических функций
        replacements = {
            'lg': 'log10',  # Замена lg на log10
            'ln': 'log',  # Замена ln на log
            '∛': 'cbrt'  # Замена ∛ на cbrt
        }
    
        for old, new in replacements.items():
            expression = expression.replace(old, new)  # Замена функций в выражении
    
        return expression  # Возврат обработанного выражения

    @classmethod
    def format_result(cls, result):
        """
        Форматирование результата вычислений.

        Args:
            result: Результат вычислений.

        Returns:
            Строка, представляющая отформатированный результат.
        """
        # Интеллектуальное форматирование результата
        if isinstance(result, float):  # Если результат является числом с плавающей запятой
            # Округление больших чисел
            if abs(result) > 1e10 or abs(result) < 1e-10:
                return f"{result:.5e}"  # Научный формат
            # Округление малых чисел
            return f"{result:.10f}".rstrip('0').rstrip('.')  # Удаление лишних нулей
        
        return str(result)  # Возврат результата как строки

    @classmethod
    def handle_error(cls, error):
        """
        Обработка ошибок.

        Args:
            error: Исключение, которое нужно обработать.

        Returns:
            Строка с сообщением об ошибке.
        """
        # Расширенная обработка ошибок
        error_map = {
            ZeroDivisionError: "Деление на ноль",  # Сообщение для деления на ноль
            OverflowError: "Слишком большое число",  # Сообщение для переполнения
            ValueError: "Недопустимое математическое действие",  # Сообщение для недопустимого действия
            TypeError: "Неверный тип данных"  # Сообщение для неверного типа данных
        }
        
        for err_type, message in error_map.items():
            if isinstance(error, err_type):  # Проверка типа ошибки
                return message  # Возврат соответствующего сообщения
        
        return str(error)  # Возврат общего сообщения об ошибке

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
        
        # Проверяем минимальный размер окна
        if height < 30 or width < 150:  # Увеличил минимальную ширину
            framework.clear()
            framework.addstr(height//2, 0, "Увеличьте размер окна терминала!")
            framework.refresh()
            return
        
        # Рассчитываем позицию для центрирования
        calc_width = 60
        start_x = max(0, (width - calc_width) // 2)
        start_y = max(0, (height - 24) // 2)

        # Инструкции слева с рамкой
        instructions_left = [
            "╔═══════════════════════════════════╗",
            "║           УПРАВЛЕНИЕ              ║",
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
            "║         ДОПОЛНИТЕЛЬНО             ║",
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
            "║                  КАЛЬКУЛЯТОР                      ║",
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

        # Отрисовка рамки
        for idx, line in enumerate(frame):
            framework.addstr(start_y + idx, start_x, line)

        # Отображение ввода
        framework.addstr(start_y + 3, start_x + 7, current_input)
        
        # Отображение результата
        if result:
            framework.addstr(start_y + 3, start_x + 35, f"Результат: {result}")

        framework.refresh()
    
    except Exception as e:
        framework.clear()
        framework.addstr(0, 0, f"Произошла ошибка: {str(e)}")
        framework.refresh()

def calculator(special_keys):
    # Настройка цветов
    curses.start_color()
    curses.curs_set(0)  # Скрываем курсора
    
    # Включаем возможность чтения специальных клавиш
    special_keys.keypad(True)
    
    # Инициализация переменных
    current_input = ""
    result = ""
    
    while True:
        # Отрисовка калькулятора
        draw_calculator_frame(special_keys, current_input, result)
        
        # Получение нажатия клавиши
        key = special_keys.getch()
        
        # Обработка нажатий
        if key == ord('q'):
            break
        
        elif key == curses.KEY_BACKSPACE or key == 127 or key == 8:
            # Удаление последнего символа
            current_input = current_input[:-1]
        
        elif key in [ord(c) for c in '0123456789.+-*/()√^']:
            current_input += chr(key)
        
        elif key == ord('c') or key == ord('C'):
            current_input = ""
            result = ""
        
        elif key == ord('=') or key == 10:  # Enter
            # Если текущий ввод пустой, ничего не делаем
            if not current_input:
                continue
            
            # Вычисление результата
            try:
                result = UltraAdvancedSafeCalculator.safe_eval(current_input)
            except Exception as e:
                result = str(e)
        
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

def remove_last_number_or_operator(expression):
    """Удаляет последнее число или оператор"""
    # Разбиваем выражение на части
    parts = re.findall(r'[\d.]+|[+\-*/]', expression)
    
    # Если есть элементы, удаляем последний
    if parts:
        return expression[:-len(parts[-1])]
    
    return expression

def main():
    curses.wrapper(calculator)

if __name__ == "__main__":
    main()