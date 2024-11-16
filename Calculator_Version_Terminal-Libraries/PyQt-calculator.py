import sys
import math
import re
import ast
import operator
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QGridLayout, QLineEdit, QLabel, QProgressBar
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar, QFrame
from PyQt5.QtCore import QPropertyAnimation, QTimer, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar, QPushButton
from PyQt5.QtCore import QPropertyAnimation, QTimer, Qt
from PyQt5.QtGui import QPixmap
import sys
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit, QMessageBox, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QSound
import sys
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit, QMessageBox, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QSound
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QTextEdit, QGridLayout, QMessageBox, QVBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QFont



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
            expression = cls.preprocess_expression(expression)
            if not re.match(r'^[0-9+\-*/().,a-zA-Z\s]+$', expression):
                return "Недопустимые символы в выражении"
            parsed = ast.parse(expression, mode='eval')
            result = cls.eval_node(parsed.body)
            return cls.format_result(result)
        except Exception as e:
            return f"Ошибка: {str(e)}"

    @classmethod
    def preprocess_expression(cls, expression):
        expression = expression.replace('^', '**')
        expression = expression.replace('√', 'sqrt(')  # Заменяем √ на sqrt(
        return expression

    @classmethod
    def eval_node(cls, node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            left = cls.eval_node(node.left)
            right = cls.eval_node(node.right)
            op = cls.SAFE_OPERATORS.get(type(node.op))
            return op(left, right)
        elif isinstance(node, ast.Call):
            func_name = node.func.id
            func = cls.SAFE_FUNCTIONS.get(func_name)
            if func:
                args = [cls.eval_node(arg) for arg in node.args]
                return func(*args)
            raise ValueError(f"Неподдерживаемая функция: {func_name}")
        raise ValueError("Неподдерживаемый тип узла")

    @classmethod
    def format_result(cls, result):
                if isinstance(result, float):
                    return f"{result:.10f}".rstrip('0').rstrip('.')
                return str(result)


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()  # Создаем экземпляр QMediaPlayer
        self.is_dark_theme = True  # Переменная для хранения текущей темы
        self.setWindowTitle("Научный Калькулятор")
        self.setGeometry(100, 100, 600, 600)

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

        layout = QGridLayout()
        layout.addWidget(self.theme_button, 0, 0)
        layout.addWidget(self.help_button, 0, 1)
        layout.addWidget(self.export_button, 0, 2)

        # Поле для вывода результатов
        self.result = QLineEdit()
        self.result.setReadOnly(True)
        self.result.setFont(font)
        self.result.setStyleSheet("background-color: #1E1E1E; color: white; padding: 10px; border-radius: 5px;")
        layout.addWidget(self.result, 1, 0, 1, 5)

        # Область для истории вычислений
        self.history_area = QTextEdit()
        self.history_area.setReadOnly(True)
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
            button = QPushButton(text)
            button.setFont(font)
            button.setStyleSheet("background-color: #4C4C4C; color: white; padding: 20px; border-radius: 5px;")
            button.pressed.connect(lambda b=button: self.on_button_pressed(b))
            button.released.connect(lambda b=button: self.on_button_released(b))
            button.clicked.connect(lambda checked, b=text: self.on_button_click(b))
            layout.addWidget(button, row, col)

        # Центрируем кнопки скобок
        self.bracket_layout = QGridLayout()
        self.left_bracket_button = QPushButton("(")
        self.right_bracket_button = QPushButton(")")
        self.left_bracket_button.setFont(font)
        self.right_bracket_button.setFont(font)
        self.left_bracket_button.clicked.connect(lambda: self.on_button_click('('))
        self.right_bracket_button.clicked.connect(lambda: self.on_button_click(')'))
        
        self.bracket_layout.addWidget(self.left_bracket_button, 0, 0)
        self.bracket_layout.addWidget(self.right_bracket_button, 0, 1)
        
        layout.addLayout(self.bracket_layout, 10, 0, 1, 5)  # Добавляем в основной layout

        self.setLayout(layout)
        self.apply_theme()  # Применяем начальную тему

        # Устанавливаем растяжение колонок
        for i in range(5):
            layout.setColumnStretch(i, 1)

    def apply_theme(self):
        if self.is_dark_theme:
            self.setStyleSheet("background-color: #2E2E2E; color: white;")
            self.theme_button.setText("Светлая тема")
            self.theme_button.setStyleSheet("background-color: #4C4C4C; color: white;")
            self.help_button.setStyleSheet("background-color: #4C4C4C; color: white;")
            self.export_button.setStyleSheet("background-color: #4C4C4C; color: white;")
        else:
            self.setStyleSheet("background-color: #FFFFFF; color: black;")
            self.theme_button.setText("Тёмная тема")
            self.theme_button.setStyleSheet("background-color: #CCCCCC; color: black;")
            self.help_button.setStyleSheet("background-color: #CCCCCC; color: black;")
            self.export_button.setStyleSheet("background-color: #CCCCCC; color: black;")

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme  # Переключаем тему
        self.apply_theme()  # Применяем новую тему

    def show_help(self):
        QMessageBox.information(self, "Подсказки", "Используйте кнопки для выполнения операций. "
                                                    "Кнопка 'C' очищает ввод, '=' вычисляет результат. "
                                                    "Кнопка 'Экспорт' сохраняет историю вычислений.")

    def export_history(self):
        with open("history.txt", "w") as file:
            for entry in self.history:
                file.write(entry + "\n")
        QMessageBox.information(self, "Экспорт", "История вычислений экспортирована в history.txt")

    def on_button_pressed(self, button):
        button.setStyleSheet("background-color: #3C3C3C; color: white; padding: 20px; border-radius: 5px;")
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile("adding-calculator-button-press-multiple-01.mp3")))  # Укажите полный путь, если необходимо
        self.player.play()  # Воспроизводим звук
        
    def on_button_released(self, button):
        button.setStyleSheet("background-color: #4C4C4C; color: white; padding: 20px; border-radius: 5px;")
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile("adding-calculator-button-press-multiple-01.mp3")))  # Укажите полный путь, если необходимо
        self.player.play()  # Воспроизводим звук
        

    def on_button_click(self, char):
        if char == 'C':
            self.result.clear()
        elif char == '=':
            try:
                expression = self.result.text()
                if expression.count('(') > expression.count(')'):
                    expression += ')'  # Добавляем закрывающую скобку только если есть открывающая
                result = UltraAdvancedSafeCalculator.safe_eval(expression)
                self.result.setText(result)
                self.history.append(f"{expression} = {result}")  # Сохраняем в историю
                self.history_area.append(f"{expression} = {result}")  # Отображаем в области истории
            except Exception:
                self.result.setText("Ошибка")
        else:
            if char == '√':
                self.result.setText(self.result.text() + 'sqrt(')  # Добавляем открывающую скобку
            else:
                self.result.setText(self.result.text() + char)


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Загрузка")
        self.setGeometry(100, 100, 600, 600)
        self.setStyleSheet("background-color: #2E2E2E;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Центрируем элементы по вертикали

        # Логотип
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("logo.png").scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
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
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        # Кнопка с текстом
        # Кнопка с текстом
        self.footer_button = QPushButton('Создано Габеркорн Вадимом')
        self.footer_button.setStyleSheet("""
    QPushButton {
        background-color: #FFD700;  /* Золотистый цвет фона */
        color: black; 
        font-size: 18px;  /* Увеличил размер шрифта */
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

        self.setLayout(layout)

        # Анимация для логотипа
        self.logo_animation = QPropertyAnimation(self.logo, b"opacity")
        self.logo_animation.setDuration(2000)  # Длительность анимации 2 секунды
        self.logo_animation.setStartValue(0)  # Начальная прозрачность
        self.logo_animation.setEndValue(1)  # Конечная прозрачность

        # Таймер для обновления индикатора загрузки
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)  # Обновление каждые 100 мс

        self.show()
        self.logo_animation.start()  # Запускаем анимацию логотипа

        # Инициализация анимации заголовка
        self.title_text = "CALCULATOR"
        self.title_index = 0
        self.title_timer = QTimer()
        self.title_timer.timeout.connect(self.update_title)
        self.title_timer.start(200)  # Появление каждой буквы каждые 200 мс

    def update_title(self):
        if self.title_index < len(self.title_text):
            self.title.setText(self.title.text() + self.title_text[self.title_index])
            self.title_index += 1
        else:
            self.title_timer.stop()  # Останавливаем таймер после завершения

        # Анимация заголовка
        if self.title_index == len(self.title_text):
            self.title_animation = QPropertyAnimation(self.title, b"opacity")
            self.title_animation.setDuration(8000)  # Длительность анимации 2 секунды
            self.title_animation.setStartValue(0)  # Начальная прозрачность
            self.title_animation.setEndValue(1)  # Конечная прозрачность
            self.title_animation.start()  # Запускаем анимацию заголовка

    def update_progress(self):
        value = self.progress.value() + 4  # Увеличиваем значение на 4
        if value > 100:
            self.timer.stop()
            self.close() # Закрываем заставку
            self.open_calculator()
        self.progress.setValue(value)

    def open_calculator(self):
        self.calculator = Calculator()
        self.calculator.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    sys.exit(app.exec_())