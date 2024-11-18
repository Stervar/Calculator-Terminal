import sys  # Импортируем модуль sys для работы с параметрами командной строки
import math  # Импортируем библиотеку math для математических операций
import re  # Импортируем библиотеку re для работы с регулярными выражениями
import ast  # Импортируем библиотеку для работы с абстрактным синтаксическим деревом (AST)
import operator  # Импортируем библиотеку operator для работы с операциями
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QGridLayout, QLineEdit  # Импортируем необходимые классы из PyQt5
from PyQt5.QtGui import QFont  # Импортируем класс QFont для настройки шрифтов

class UltraAdvancedSafeCalculator:
    """
    Класс для безопасного вычисления математических выражений.
    """
    SAFE_FUNCTIONS = {
        'abs': abs,  # Модуль числа
        'round': round,  # Округление
        'max': max,  # Максимальное значение
        'min': min,  # Минимальное значение
        'sum': sum,  # Сумма
        'sin': math.sin,  # Синус
        'cos': math.cos,  # Косинус
        'tan': math.tan,  # Тангенс
        'sqrt': math.sqrt,  # Квадратный корень
        'log': math.log,  # Натуральный логарифм
        'exp': math.exp,  # Экспонента
        'pi': math.pi,  # Число π
        'e': math.e,  # Число Эйлера
    }

    SAFE_OPERATORS = {
        ast.Add: operator.add,  # Сложение
        ast.Sub: operator.sub,  # Вычитание
        ast.Mult: operator.mul,  # Умножение
        ast.Div: operator.truediv,  # Деление
        ast.Pow: operator.pow,  # Возведение в степень
        ast.USub: operator.neg,  # Унарное отрицание
        ast.UAdd: operator.pos  # Унарное положительное
    }

    @classmethod
    def safe_eval(cls, expression):
        """
        Безопасная оценка математического выражения.
        """
        try:
            expression = cls.preprocess_expression(expression)  # Предобработка выражения
            # Проверка на допустимые символы
            if not re.match(r'^[0-9+\-*/().,a-zA-Z\s]+$', expression):
                return "Недопустимые символы в выражении"
            parsed = ast.parse(expression, mode='eval')  # Парсинг выражения в AST
            result = cls.eval_node(parsed.body)  # Оценка корневого узла AST
            return cls.format_result(result)  # Форматирование результата
        except Exception as e:
            return f"Ошибка: {str(e)}"  # Возврат сообщения об ошибке

    @classmethod
    def preprocess_expression(cls, expression):
        """
        Предобработка выражения перед его оценкой.
        """
        expression = expression.replace('^', '**')  # Замена '^' на '**' для возведения в степень
        return expression

    @classmethod
    def eval_node(cls, node):
        """
        Оценка узлов абстрактного синтаксического дерева.
        """
        if isinstance(node, ast.Num):  # Если узел - число
            return node.n  # Возвращаем число
        elif isinstance(node, ast.BinOp):  # Если узел - бинарная операция
            left = cls.eval_node(node.left)  # Оценка левого операнда
            right = cls.eval_node(node.right)  # Оценка правого операнда
            op = cls.SAFE_OPERATORS.get(type(node.op))  # Получение оператора
            return op(left, right)  # Применение оператора
        elif isinstance(node, ast.Call):  # Если узел - вызов функции
            func_name = node.func.id  # Имя функции
            func = cls.SAFE_FUNCTIONS.get(func_name)  # Получение функции
            if func:
                args = [cls.eval_node(arg) for arg in node.args]  # Оценка аргументов
                return func(*args)  # Вызов функции с аргументами
            raise ValueError(f"Неподдерживаемая функция: {func_name}")  # Ошибка для неподдерживаемой функции
        raise ValueError("Неподдерживаемый тип узла")  # ```python
        raise ValueError("Неподдерживаемый тип узла")  # Ошибка для неподдерживаемого типа узла

    @classmethod
    def format_result(cls, result):
        """
        Форматирование результата для удобства отображения.
        """
        if isinstance(result, float):  # Если результат - число с плавающей точкой
            return f"{result:.10f}".rstrip('0').rstrip('.')  # Форматируем до 10 знаков после запятой
        return str(result)  # Возвращаем результат как строку

class Calculator(QWidget):
    """
    Класс для создания графического интерфейса калькулятора.
    """
    def __init__(self):
        super().__init__()  # Инициализация родительского класса
        self.setWindowTitle("Калькулятор")  # Установка заголовка окна
        self.setGeometry(100, 100, 400, 600)  # Установка размеров окна
        self.setStyleSheet("background-color: #2E2E2E; color: white;")  # Установка стиля окна

        font = QFont("Arial", 20)  # Установка шрифта

        self.result = QLineEdit()  # Поле для отображения результата
        self.result.setReadOnly(True)  # Поле только для чтения
        self.result.setFont(font)  # Установка шрифта для поля
        self.result.setStyleSheet("background-color: #1E1E1E; color: white; padding: 10px; border-radius: 5px;")  # Установка стиля для поля
        
        layout = QGridLayout()  # Создание сеточного макета
        layout.addWidget(self.result, 0, 0, 1, 4)  # Добавление поля результата в макет

        buttons = [  # Определение кнопок калькулятора
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('C', 4, 1), ('=', 4, 2), ('+', 4, 3)
        ]

        for (text, row, col) in buttons:  # Создание кнопок и добавление их в макет
            button = QPushButton(text)  # Создание кнопки
            button.setFont(font)  # Установка шрифта для кнопки
            button.setStyleSheet("background-color: #4C4C4C; color: white; padding: 20px; border-radius: 5px;")  # Установка стиля для кнопки
            button.clicked.connect(lambda checked, b=text: self.on_button_click(b))  # Привязка события нажатия кнопки
            layout.addWidget(button, row, col)  # Добавление кнопки в макет

        self.setLayout(layout)  # Установка макета для виджета

    def on_button_click(self, char):
        """
        Обработка нажатия кнопки.
        """
        if char == 'C':  # Если нажата кнопка "C"
            self.result.clear()  # Очистка поля результата
        elif char == '=':  # Если нажата кнопка "="
            try:
                expression = self.result.text()  # Получение выражения из поля
                result = UltraAdvancedSafeCalculator.safe_eval(expression)  # Оценка выражения
                self.result.setText(result)  # Установка результата в поле
            except Exception:
                self.result.setText("Ошибка")  # Установка сообщения об ошибке
        else:  # Если нажата другая кнопка
            self.result.setText(self.result.text() + char)  # Добавление символа к выражению

if __name__ == "__main__":  # Проверка, является ли скрипт основным
    app = QApplication(sys.argv)  # Создание экземпляра приложения
    window = Calculator()  # Создание экземпляра калькулятора
    window.show()  # Отображение окна
    sys.exit(app.exec_())  # Запуск приложения