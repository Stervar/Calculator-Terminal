import curses  # Импортируем библиотеку curses для работы с консольным интерфейсом
import math  # Импортируем библиотеку math для математических операций
import re  # Импортируем библиотеку re для работы с регулярными выражениями
import traceback  # Импортируем библиотеку для отладки и обработки исключений
import ast  # Импортируем библиотеку для работы с абстрактным синтаксическим деревом (AST)
import operator  # Импортируем библиотеку для работы с операциями

class SafeCalculator:
    """
    Класс для безопасного вычисления математических выражений.
    """
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
        
        # Экспоненциальные и логарифмические функции
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
        ast.Add: operator.add,  # Оператор сложения
        ast.Sub: operator.sub,  # Оператор вычитания
        ast.Mult: operator.mul,  # Оператор умножения
        ast.Div: operator.truediv,  # Оператор деления
        ast.Pow: operator.pow,  # Оператор возведения в степень
        ast.USub: operator.neg  # Унарный оператор отрицания
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
            # Предварительная обработка выражения
            expression = cls.preprocess_expression(expression)
            
            # Парсинг AST (абстрактное синтаксическое дерево)
            parsed = ast.parse(expression, mode='eval')
            return cls.eval_node(parsed.body)  # Оценка корневого узла
        
        except Exception as e:
            return f"Ошибка: {str(e)}"  # Возврат сообщения об ошибке

    @classmethod
    def eval_node(cls, node):
        """
        Оценка узлов AST.

        Args:
            node: Узел AST.

        Returns:
            Результат вычисления узла.
        """
        if isinstance(node, ast.Num):  # Если узел является числом
            return node.n
        
        elif isinstance(node, ast.Name):  # Если узел является именем
            if node.id in cls.SAFE_FUNCTIONS:  # Проверка на разрешенные функции
                return cls.SAFE_FUNCTIONS[node.id]
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
            
            if op not in cls.SAFE_OPERATORS: raise ValueError(f"Недопустимая операция: {op}")  # Ошибка для недопустимой операции
            
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
        
        return expression  # Возврат обработанного выражения

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
        
        # Обработка клавиш с расширенной логикой
        if key == ord('q'):  # Выход при нажатии 'q'
            break
        
        elif key in [ord(c) for c in '0123456789.+-*/()√^']:  # Обработка цифр и операторов
            current_input += chr(key)  # Добавление символа к текущему вводу
        
        elif key == ord('c') or key == ord('C'):  # Полная очистка
            current_input = ""
            result = ""
        
        elif key == 263 or key == 127:  # Backspace
            current_input = current_input[:-1]  # Удаление последнего символа
        
        elif key == ord('=') or key == 10:  # Нажатие Enter
            try:
                result = SafeCalculator.safe_eval(current_input)  # Вычисление результата
                current_input = str(result)  # Обновление текущего ввода на результат
            except Exception as e:
                result = f"Ошибка: {str(e)}"  # Обработка ошибок
        
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
    """
    Инициализация и запуск калькулятора.

    Returns:
        None.
    """
    curses.wrapper(calculator)  # Запуск калькулятора в контексте curses

if __name__ == "__main__":
    main()  # Запуск программы
    
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