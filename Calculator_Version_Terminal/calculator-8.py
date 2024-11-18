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
            
            # Парсинг и вычисление
            parsed = ast.parse(expression, mode='eval')  # Парсинг выражения в AST
            result = cls.eval_node(parsed.body)  # Оценка корневого узла AST
            
            # Обработка результата
            return cls.format_result(result)  # Форматирование результата перед возвратом
            
        except Exception as e:
            return f"Ошибка: {cls.handle_error(e)}"  # Возврат сообщения об ошибке

    @classmethod
    def eval_node(cls, node):
        """
        Оцен ```python
        узлов AST.

        Args:
            node: Узел AST.

        Returns:
            Результат вычисления узла.
        """
        if isinstance(node, ast.Num):  # Если узел является числом
            return node.n  # Возврат значения числа
        
        elif isinstance(node, ast.Name):  # Если узел является именем
            if node.id in cls.SAFE_FUNCTIONS:  # Проверка на разрешенные функции
                return cls.SAFE_FUNCTIONS[node.id]  # Возврат функции
            raise NameError(f"Неизвестное имя: {node.id}")  # Ошибка для недопустимого имени
        
        elif isinstance(node, ast.Call):  # Если узел является вызовом функции
            func = cls.eval_node(node.func)  # Оценка функции
            args = [cls.eval_node(arg) for arg in node.args]  # Оценка аргументов
            return func(*args)  # Вызов функции с аргументами
        
        elif isinstance(node, ast.BinOp):  # Если узел является бинарной операцией
            left = cls.eval_node(node.left)  # Оценка левого операнда
            right = cls.eval_node(node.right)  # Оценка правого операнда
            
            op = type(node.op)  # Получение типа операции
            if op not in cls.SAFE_OPERATORS:  # Проверка на допустимую операцию
                raise ValueError(f"Недопустимая операция: {op}")
            
            return cls.SAFE_OPERATORS[op](left, right)  # Выполнение операции
        
        elif isinstance(node, ast.UnaryOp):  # Если узел является унарной операцией
            operand = cls.eval_node(node.operand)  # Оценка операнда
            op = type(node.op)  # Получение типа операции
            
            if op not in cls.SAFE_OPERATORS:  # Проверка на допустимую операцию
                raise ValueError(f"Недопустимая операция: {op}")
            
            return cls.SAFE_OPERATORS[op](operand)  # Выполнение унарной операции
        
        raise TypeError(f"Неподдерживаемый тип узла: {type(node)}")  # Ошибка для неподдерживаемого типа узла

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
            error: Иск лючение, которое нужно обработать.

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
    pass  # Здесь будет логика отрисовки интерфейса калькулятора

def calculator(framework):
    """
    Основная функция калькулятора, обрабатывающая ввод и вычисления.

    Args:
        framework: Объект curses, предоставляющий доступ к клавиатурному вводу.

    Returns:
        None.
    """
    curses.start_color()  # Инициализация цветовой схемы
    curses.curs_set(0)  # Скрытие курсора
    
    current_input = ""  # Переменная для хранения текущего ввода
    result = ""  # Переменная для хранения результата
    
    while True:
        draw_calculator_frame(framework, current_input, result)  # Отрисовка интерфейса
        
        key = framework.getch()  # Получение нажатой клавиши
        
        # Расширенная обработка клавиш
        if key == ord('q'):  # Выход при нажатии 'q'
            break
        
        # Добавлены новые возможности ввода
        elif key in [ord(c) for c in '0123456789.+-*/()√^j']:
            current_input += chr(key)  # Добавление символа к текущему вводу
        
        elif key == ord('c') or key == ord('C'):  # Полная очистка
            current_input = ""
            result = ""
        
        elif key == 263 or key == 127:  # Backspace
            current_input = current_input[:-1]  # Удаление последнего символа
        
        elif key == ord('=') or key == 10:  # Нажатие Enter
            result = UltraAdvancedSafeCalculator.safe_eval(current_input)  # Вычисление результата
            current_input = ""  # Сброс текущего ввода
        
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
    """
    Инициализация и запуск калькулятора.

    Returns:
        None.
    """
    curses.wrapper(calculator)  # Запуск калькулятора в контексте curses

if __name__ == "__main__":
    main()  # Запуск программы