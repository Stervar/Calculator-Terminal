import sys  # Импортируем модуль sys для работы с параметрами командной строки
import math  # Импортируем библиотеку math для математических операций
import re  # Импортируем библиотеку re для работы с регулярными выражениями
import ast  # Импортируем библиотеку для работы с абстрактным синтаксическим деревом (AST)
import operator  # Импортируем библиотеку operator для работы с операциями
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QGridLayout, QLineEdit, QLabel, QProgressBar, QTextEdit, QMessageBox  # Импортируем необходимые классы из PyQt5
from PyQt5.QtGui import QFont, QPixmap  # Импортируем класс QFont и QPixmap для настройки шрифтов и изображений
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation  # Импортируем классы для таймеров и анимации
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent  # Импортируем классы для работы со звуком
from PyQt5.QtCore import QUrl




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
        """
        Безопасная оценка математического выражения.
        """
        try:
            expression = cls.preprocess_expression(expression)  # Предобработка выражения
            if not re.match(r'^[0-9+\-*/().,a-zA-Z\s]+$', expression):  # Проверка на допустимые символы
                return "Недопустимые символы в выражении"  # Сообщение об ошибке
            parsed = ast.parse(expression, mode='eval')  # Парсинг выражения в AST
            result = cls.eval_node(parsed.body)  # Оценка корневого узла AST
            return cls.format_result(result)  # Форматирование результата
        except Exception as e:
            return f"Ошибка: {str(e)}"  # Возв ```python
            return f"Ошибка: {str(e)}"  # Возврат сообщения об ошибке

    @classmethod
    def preprocess_expression(cls, expression):
        """
        Предобработка выражения для замены специальных символов.
        """
        expression = expression.replace('^', '**')  # Замена ^ на **
        expression = expression.replace('√', 'sqrt(')  # Замена √ на sqrt(
        return expression

    @classmethod
    def eval_node(cls, node):
        """
        Оценка узла AST.
        """
        if isinstance(node, ast.Num):
            return node.n  # Возврат числа
        elif isinstance(node, ast.BinOp):
            left = cls.eval_node(node.left)  # Оценка левого подузла
            right = cls.eval_node(node.right)  # Оценка правого подузла
            op = cls.SAFE_OPERATORS.get(type(node.op))  # Получение оператора
            return op(left, right)  # Применение оператора
        elif isinstance(node, ast.Call):
            func_name = node.func.id  # Получение имени функции
            func = cls.SAFE_FUNCTIONS.get(func_name)  # Получение функции
            if func:
                args = [cls.eval_node(arg) for arg in node.args]  # Оценка аргументов
                return func(*args)  # Вызов функции с аргументами
            raise ValueError(f"Неподдерживаемая функция: {func_name}")  # Ошибка для неподдерживаемой функции
        raise ValueError("Неподдерживаемый тип узла")  # Ошибка для неподдерживаемого типа узла

    @classmethod
    def format_result(cls, result):
        """
        Форматирование результата для вывода.
        """
        if isinstance(result, float):
            return f"{result:.10f}".rstrip('0').rstrip('.')  # Форматирование числа с плавающей точкой
        return str(result)  # Возврат результата как строки


class Calculator(QWidget):
    """
    Класс для создания графического интерфейса калькулятора.
    """
    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()  # Создаем экземпляр QMediaPlayer
        self.is_dark_theme = True  # Переменная для хранения текущей темы
        self.setWindowTitle("Научный Калькулятор")  # Заголовок окна
        self.setGeometry(100, 100, 600, 600)  # Размеры окна

        self.history = []  # Список для хранения истории вычислений
        font = QFont("Arial", 20)  # Шрифт для кнопок и текстового поля

        # Кнопка переключения темы
        self.theme_button = QPushButton("Светлая тема")
        self.theme_button.clicked.connect(self.toggle_theme)

        # Кнопка подсказок
        self.help_button = QPushButton("?")
        self.help_button.clicked.connect(self.show_help)

        # Кнопка экспорта
        self.export_button = QPushButton("Экспорт")
        self.export_button.clicked.connect(self.export_history)

        layout = QGridLayout()  # Создание сеточного макета
        layout.addWidget(self.theme_button, 0, 0)
        layout.addWidget(self.help_button, 0, 1)
        layout.addWidget(self.export_button, 0, 2)

        # Поле для вывода результатов
        self.result = QLineEdit()
        self.result.setReadOnly(True)  # Поле только для чтения
        self.result.setFont(font)  # Установка шрифта
        self.result.setStyleSheet("background-color: #1E1E1E; color: white; padding: 10px; border-radius: 5px;")
        layout.addWidget(self.result, 1, 0, 1, 5)

        # Область для истории вычислений
        self.history_area = QTextEdit()
        self.history_area.setReadOnly(True)  # Поле только для чтения
        layout.addWidget(self.history_area, 2, 0, 1, 5)

        # Определение кнопок калькулятора
        buttons = [
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('/', 3, 3), ('C', 3, 4),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('*', 4, 3), ('√', 4, 4),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('-', 5, 3), ('^', 5, 4),
            ('0', 6, 0), ('.', 6, 1), ('+', 6, 2), ('=', 6, 3), ('sin', 6, 4),
            ('cos', 7, 0), ('tan', 7, 1), ('log', 7, 2), ('e', 7, 3), ('1/x', 7, 4),
            ('asin', 8, 0), ('acos', 8, 1), ('atan', 8, 2), ('exp', 8, 3), ('sqrt', 8, 4),
            ('ceil', 9, 0), ('floor', 9, 1), ('factorial', 9, 2), ('cbrt', 9, 3), ('ln', 9, 4),
        ]

        for (text, row, col) in buttons:
            button = QPushButton(text)  # Создание кнопки
            button.setFont(font)  # Установка шрифта
            button.setStyleSheet("background-color: #4C4C4C; color: white; padding: 20px; border-radius: 5px;")
            button.pressed.connect(lambda b=button: self.on_button_pressed(b))  # Обработка нажатия кнопки
            button.released.connect(lambda b=button: self.on_button_released(b))  # Обработка отпускания кнопки
            button.clicked.connect(lambda checked, b=text: self.on_button_click(b))  # Обработка клика по кнопке
            layout.addWidget(button, row, col)  # Добавление кнопки в макет

        # Центрируем кнопки скобок
        self.bracket_layout = QGridLayout()
        self.left_bracket_button = QPushButton("(")
        self.right_bracket_button = QPushButton(")")
        self.left_bracket_button.setFont(font)
        self.right_bracket_button.setFont(font)
        self.left_bracket_button.clicked.connect(lambda: self.on_button_click('('))  # Обработка нажатия на (
        self.right_bracket_button.clicked.connect(lambda: self.on_button_click(')'))  # Обработка нажатия на )

        self.bracket_layout.addWidget(self.left_bracket_button, 0, 0)
        self.bracket_layout.addWidget(self.right_bracket_button, 0, 1)

        layout.addLayout(self.bracket_layout, 10, 0, 1, 5)  # Добавляем в основной layout

        self.setLayout(layout)  # Установка макета для виджета
        self.apply_theme()  # Применяем начальную тему

        # Устанавливаем растяжение колонок
        for i in range(5):
            layout.setColumnStretch(i, 1)

    def apply_theme(self):
        """
        Применение темы (темная или светлая).
        """
        if self.is_dark_theme:
            self.setStyleSheet("background-color: #2E2E2E; color: white;")  # Темная тема
            self.theme_button.setText("Светлая тема")
            self.theme_button.setStyleSheet("background-color: #4C4C4C; color: white;")
            self.help_button.setStyleSheet("background-color: #4C4C4C; color: white;")
            self.export_button.setStyleSheet("background-color: #4C4C4C; color: white;")
        else:
            self.setStyleSheet("background-color: #FFFFFF; color: black;")  # Светлая тема
            self.theme_button.setText("Тёмная тема")
            self.theme_button.setStyleSheet("background-color: #CCCCCC; color: black;")
            self.help_button.setStyleSheet("background-color: #CCCCCC; color: black;")
            self.export_button.setStyleSheet("background-color: #CCCCCC; color: black;")

    def toggle_theme(self):
        """
        Переключение темы между темной и светлой.
        """
        self.is_dark_theme = not self.is_dark_theme  # Переключаем тему
        self.apply_theme()  # Применяем новую тему

    def show_help(self):
        """
        Показать подсказки пользователю.
        """
        QMessageBox.information(self, "Подсказки", "Используйте кнопки для выполнения операций. "
                                                    "Кнопка 'C' очищает ввод, "
                                                    " '=' вычисляет результат. "
                                                    "Кнопка 'Экспорт' сохраняет историю вычислений.")

    def export_history(self):
        """
        Экспортировать историю вычислений в текстовый файл.
        """
        with open("history.txt", "w") as file:
            for entry in self.history:
                file.write(entry + "\n")  # Запись каждой записи в файл
        QMessageBox.information(self, "Экспорт", "История вычислений экспортирована в history.txt")

    def on_button_pressed(self, button):
        """
        Обработка нажатия кнопки.
        """
        button.setStyleSheet("background-color: #3C3C3C; color: white; padding: 20px; border-radius: 5px;")
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile("adding-calculator-button-press-multiple-01.mp3")))  # Укажите полный путь, если необходимо
        self.player.play()  # Воспроизводим звук
        
    def on_button_released(self, button):
        """
        Обработка отпускания кнопки.
        """
        button.setStyleSheet("background-color: #4C4C4C; color: white; padding: 20px; border-radius: 5px;")
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile("adding-calculator-button-press-multiple-01.mp3")))  # Укажите полный путь, если необходимо
        self.player.play()  # Воспроизводим звук

    def on_button_click(self, char):
        """
        Обработка клика по кнопке.
        """
        if char == 'C':
            self.result.clear()  # Очистка поля ввода
        elif char == '=':
            try:
                expression = self.result.text()  # Получение выражения из поля ввода
                if expression.count('(') > expression.count(')'):
                    expression += ')'  # Добавляем закрывающую скобку только если есть открывающая
                result = UltraAdvancedSafeCalculator.safe_eval(expression)  # Оценка выражения
                self.result.setText(result)  # Установка результата в поле ввода
                self.history.append(f"{expression} = {result}")  # Сохраняем в историю
                self.history_area.append(f"{expression} = {result}")  # Отображаем в области истории
            except Exception:
                self.result.setText("Ошибка")  # Сообщение об ошибке
        else:
            if char == '√':
                self.result.setText(self.result.text() + 'sqrt(')  # Добавляем открывающую скобку
            else:
                self.result.setText(self.result.text() + char)  # Добавляем символ к выражению


class SplashScreen(QWidget):
    """
    Класс для отображения заставки при запуске приложения.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Загрузка")  # Заголовок окна заставки
        self.setGeometry(100, 100, 600, 600)  # Размеры окна
        self.setStyleSheet("background-color: #2E2E2E;")  # Цвет фона заставки

        layout = QVBoxLayout()  # Создание вертикального макета
        layout.setAlignment(Qt.AlignCenter)  # Центрируем элементы по вертикали

        # Логотип
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("logo.png").scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Установка логотипа
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setStyleSheet("opacity: 0;")  # Начальное состояние невидимое
        layout.addWidget(self.logo)

        # Заголовок
        self.title = QLabel("")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: white; font-size: 50px; opacity: 0;")  # Увеличенный размер шрифта
        layout.addWidget(self.title)

        # Индикатор загрузки
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)  # Установка диапазона индикатора
        self.progress.setValue(0)  # Начальное значение
        layout.addWidget(self.progress)

        # Кнопка с текстом
        self.footer_button = QPushButton('Создано Габеркорн Вадимом')
        self.footer_button.setStyleSheet("""
    QPushButton {
        background-color: #FFD700;  /* Золотистый цвет фона */
        color: black; 
        font-size: 18px; ```python
        font-weight: bold; 
        border: 2px solid #FFA500;  /* Оранжевая граница */
        border-radius: 10px; 
        padding: 10px 20px;  /* Увеличил вертикальный и горизонтальный отступы */
        max-width: 350px;   /* Ограничил максимальную ширину */
    }
    QPushButton:hover {
        background-color: #FFA500;  /* Цвет фона при наведении */
        border: 2px solid #FF8C00;  /* Изменение цвета границы при наведении */
    }
""")
        self.footer_button.setFixedWidth(350)  # Фиксированная ширина
        self.footer_button.setCursor(Qt.PointingHandCursor)

        # Добавляем кнопку в центр
        layout.addStretch()  # Добавляем растяжение перед кнопкой
        layout.addWidget(self.footer_button, alignment=Qt.AlignCenter)  # Центрируем кнопку
        layout.addStretch()  # Добавляем растяжение после кнопки

        self.setLayout(layout)  # Установка макета для виджета

        # Анимация для логотипа
        self.logo_animation = QPropertyAnimation(self.logo, b"opacity")
        self.logo_animation.setDuration(2000)  # Длительность анимации 2 секунды
        self.logo_animation.setStartValue(0)  # Начальная прозрачность
        self.logo_animation.setEndValue(1)  # Конечная прозрачность

        # Таймер для обновления индикатора загрузки
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)  # Обновление каждые 100 мс

        self.show()  # Отображение заставки
        self.logo_animation.start()  # Запускаем анимацию логотипа

        # Инициализация анимации заголовка
        self.title_text = "CALCULATOR"
        self.title_index = 0
        self.title_timer = QTimer()
        self.title_timer.timeout.connect(self.update_title)
        self.title_timer.start(200)  # Появление каждой буквы каждые 200 мс

    def update_title(self):
        """
        Обновление заголовка заставки.
        """
        if self.title_index < len(self.title_text):
            self.title.setText(self.title.text() + self.title_text[self.title_index])  # Добавление буквы к заголовку
            self.title_index += 1
        else:
            self.title_timer.stop()  # Останавливаем таймер после завершения

        # Анимация заголовка
        if self.title_index == len(self.title_text):
            self.title_animation = QPropertyAnimation(self.title, b"opacity")
            self.title_animation.setDuration(8000)  # Длительность анимации 8 секунд
            self.title_animation.setStartValue(0)  # Начальная прозрачность
            self.title_animation.setEndValue(1)  # Конечная прозрачность
            self.title_animation.start()  # Запускаем анимацию заголовка

    def update_progress(self):
        """
        Обновление индикатора загрузки.
        """
        value = self.progress.value() + 4  # Увеличиваем значение на 4
        if value > 100:
            self.timer.stop()  # Останавливаем таймер
            self.close()  # Закрываем заставку
            self.open_calculator()  # Открываем калькулятор
        self.progress.setValue(value)  # Установка нового значения индикатора

    def open_calculator(self):
        """
        Открытие основного окна калькулятора.
        """
        self.calculator = Calculator()  # Создание экземпляра калькулятора
        self.calculator.show()  # Отображение калькулятора

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Создание экземпляра приложения
    splash = SplashScreen()  # Создание и отображение заставки
    sys.exit(app.exec_())  # Запуск основного цикла приложения