import ast  # Импортируем библиотеку для работы с абстрактным синтаксическим деревом (AST)
import operator  # Импортируем библиотеку для работы с операциями
import math  # Импортируем библиотеку math для математических операций
import cmath  # Импортируем библиотеку cmath для работы с комплексными числами

class UniversalCalculator:
    """
    Класс для универсального калькулятора, который поддерживает математические операции и функции.
    """

    # Безопасные функции, доступные для вычислений
    SAFE_FUNCTIONS = {
        'abs': abs,  # Модуль числа
        'round': round,  # Округление
        'max': max,  # Максимальное значение
        'min': min,  # Минимальное значение
        'sum': sum,  # Сумма
        'sin': math.sin,  # Синус
        'cos': math.cos,  # Косинус
        'tan': math.tan,  # Тангенс
        'asin': math.asin,  # Арксинус
        'acos': math.acos,  # Арккосинус
        'atan': math.atan,  # Арктангенс
        'sinh': math.sinh,  # Гиперболический синус
        'cosh': math.cosh,  # Гиперболический косинус
        'tanh': math.tanh,  # Гиперболический тангенс
        'exp': math.exp,  # Экспонента
        'log': math.log,  # Натуральный логарифм
        'log10': math.log10,  # Десятичный логарифм
        'log2': math.log2,  # Двоичный логарифм
        'sqrt': math.sqrt,  # Квадратный корень
        'pow': pow,  # Возведение в степень
        'pi': math.pi,  # Число π
        'e': math.e,  # Число Эйлера
        'inf': float('inf'),  # Бесконечность
        'i': complex(0, 1),  # Мнимая единица
    }

    # Безопасные операторы для работы с арифметическими операциями
    SAFE_OPERATORS = {
        ast.Add: operator.add,  # Сложение
        ast.Sub: operator.sub,  # Вычитание
        ast.Mult: operator.mul,  # Умножение
        ast.Div: operator.truediv,  # Деление
        ast.FloorDiv: operator.floordiv,  # Целочисленное деление
        ast.Mod: operator.mod,  # Остаток от деления
        ast.Pow: operator.pow,  # Возведение в степень
        ast.BitAnd: operator.and_,  # Битовое И
        ast.BitOr: operator.or_,  # Битовое ИЛИ
        ast.BitXor: operator.xor,  # Битовый XOR
        ast.LShift: operator.lshift,  # Сдвиг влево
        ast.RShift: operator.rshift,  # Сдвиг вправо
    }

    def __init__(self):
        """
        Инициализация калькулятора.
        """
        self.variables = {}  # Словарь для хранения переменных

    def set_variable(self, name, value):
        """
        Установка значения переменной.

        :param name: Имя переменной
        :param value: Значение переменной
        """
        self.variables[name] = value

    def get_variable(self, name):
        """
        Получение значения переменной.

        :param name: Имя переменной
        :return: Значение переменной или None, если переменная не определена
        """
        return self.variables.get(name, None)

    def safe_eval(self, expression):
        """
        Безопасная оценка математического выражения.

        :param expression: Строка, представляющая математическое выражение
        :return: Результат вычисления или сообщение об ошибке
        """
        try:
            expression = self.preprocess_expression(expression)  # Предобработка выражения
            parsed = ast.parse(expression, mode='eval')  # Парсинг выражения в AST
            result = self.eval_node(parsed.body)  # Оценка корневого узла AST
            return self.format_result(result)  # Форматирование результата
        except Exception as e:
            return f"Ошибка: {str(e)}"  
    def preprocess_expression(self, expression):
        """
        Предобработка выражения перед его оценкой.

        :param expression: Строка, представляющая математическое выражение
        :return: Предобработанное выражение
        """
        expression = expression.replace('^', '**')  # Замена '^' на '**' для возведения в степень
        
        # Заменяем все случаи, когда число предшествует открывающей скобке, на умножение
        new_expression = ""
        for i, char in enumerate(expression):
            if char == '(' and i > 0 and expression[i - 1].isdigit():
                new_expression += '*'  # Добавляем оператор умножения
            new_expression += char
        return new_expression

    def eval_node(self, node):
        """
        Оценка узлов абстрактного синтаксического дерева.

        :param node: Узел AST
        :return: Результат оценки узла
        """
        if isinstance(node, ast.Constant):
            return node.value  # Возвращаем значение константы
        elif isinstance(node, ast.Num):
            return node.n  # Возвращаем число
        elif isinstance(node, ast.BinOp):
            left = self.eval_node(node.left)  # Оценка левого операнда
            right = self.eval_node(node.right)  # Оценка правого операнда
            return self.SAFE_OPERATORS[type(node.op)](left, right)  # Применение оператора
        elif isinstance(node, ast.UnaryOp):
            operand = self.eval_node(node.operand)  # Оценка операнда
            return operator.neg(operand) if isinstance(node.op, ast.USub) else operator.pos(operand)  # Унарные операции
        elif isinstance(node, ast.Name):
            value = self.get_variable(node.id)  # Получение значения переменной
            if value is None:
                raise ValueError(f"Переменная '{node.id}' не определена")  # Ошибка, если переменная не найдена
            return value
        elif isinstance(node, ast.Call):
            func = self.SAFE_FUNCTIONS.get(node.func.id)  # Получение функции
            if not func:
                raise ValueError(f"Функция {node.func.id} не поддерживается")  # Ошибка, если функция не поддерживается
            args = [self.eval_node(arg) for arg in node.args]  # Оценка аргументов функции
            return func(*args)  # Вызов функции с аргументами
        else:
            raise TypeError(f"Неподдерживаемый узел: {type(node)}")  # Ошибка для неподдерживаемых узлов

    def format_result(self, result):
        """
        Форматирование результата для удобства отображения.

        :param result: Результат вычисления
        :return: Строка с отформатированным результатом
        """
        return f"Результат: {result}"  # Возвращаем результат в виде строки
