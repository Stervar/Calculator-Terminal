# Импорт необходимых библиотек для работы калькулятора
# curses - для создания текстового интерфейса
# math - для математических вычислений
# re - для работы с регулярными выражениями
import curses
import math
import re

def draw_calculator_frame(framework, current_input, result):
    # Получаем размеры текущего окна терминала
    height, width = framework.getmaxyx()
    
    # Расчет позиции для центрирования калькулятора на экране
    calc_width = 60
    start_x = (width - calc_width) // 2  # Центрирование по горизонтали
    start_y = (height - 24) // 2  # Центрирование по вертикали

    # Очистка экрана перед новой отрисовкой
    framework.clear()

    # Создание массива строк для визуального интерфейса калькулятора
    # Используются специальные символы для создания графической рамки
    frame = [
        "╔═══════════════════════════════════════════════════╗",
        "║                  КАЛЬКУЛЯТОР                      ║",
        "╠═══════════════════════════════════════════════════╣",
        "║                                                   ║",
        "╠═══════════════════════════════════════════════════╣",
        "║   7    │    8    │    9    │    /    │    CE      ║",
        "║--------+---------+---------+---------+------------║",
        "║   4    │    5    │    6    │    *    │    √       ║",
        "║--------+---------+---------+---------+------------║",
        "║   1    │    2    │    3    │    -    │    %       ║",
        "║--------+---------+---------+---------+------------║",
        "║   0    │    .    │    +    │ x²  │ 1/x │ ±        ║",
        "║--------+---------+---------+---------+------------║",
        "║   log  │    e    │    ^    │    (   │    )        ║"
    ]

    # Добавление информационной части в низ рамки
    frame.append("╠═══════════════════════════════════════════════════╣")
    frame.append("║ Backspace - удаляет символ | CE - удаляет число   ║")
    frame.append("║ C - полная очистка | Расширенные функции          ║")
    frame.append("╚═══════════════════════════════════════════════════╝")

    # Отрисовка каждой строки рамки калькулятора
    for idx, line in enumerate(frame):
        framework.addstr(start_y + idx, start_x, line)

    # Вывод текущего введенного выражения
    framework.addstr(start_y + 3, start_x + 2, f"Ввод: {current_input}")
    
    # Вывод результата вычисления (если есть)
    if result:
        framework.addstr(start_y + 3, start_x + 35, f"Результат: {result}")

    # Обновление экрана для отображения изменений
    framework.refresh()

def calculator(special_keys):
    # Инициализация цветового режима для curses
    curses.start_color()
    # Скрытие курсора
    curses.curs_set(0)  
    
    # Инициализация переменных для хранения текущего ввода и результата
    current_input = ""
    result = ""
    
    # Основной цикл обработки пользовательского ввода
    while True:
        # Отрисовка интерфейса калькулятора
        draw_calculator_frame(special_keys, current_input, result)
        
        # Получение нажатой клавиши
        key = special_keys.getch()
        
        # Обработка нажатия клавиши выхода
        if key == ord('q'):
            break
        
        # Обработка ввода цифр и точки
        elif key in [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), 
                    ord('5'), ord('6'), ord('7'), ord('8'), ord('9'), ord('.')]:
            # Если есть предыдущий результат, начинаем новый ввод
            if result:
                current_input = chr(key)
                result = ""
            else:
                current_input += chr(key)
        
        # Обработка математических операторов
        elif key in [ord('+'), ord('-'), ord('*'), ord('/')]:
            # Использование предыдущего результата как начало нового выражения
            if result:
                current_input = result + chr(key)
                result = ""
            else:
                current_input += chr(key)
        
        # Полная очистка введенного выражения
        elif key == ord('c') or key == ord('C'):
            current_input = ""
            result = ""
        
        # Удаление последнего элемента
        elif key == ord('e') or key == ord('E'):
            current_input = remove_last_number_or_operator(current_input)
        
        # Удаление последнего символа (Backspace)
        elif key == 263 or key == 127:
            current_input = current_input[:-1]
        
        # Вычисление результата
        elif key == ord('=') or key == 10:
            try:
                result = str(eval(current_input))
                current_input = ""  # Очистка ввода после вычисления
            except Exception:
                result = "Ошибка"
        
        # Вычисление процента
        elif key == ord('%'):
            try:
                result = str(eval(f"{current_input}/100"))
                current_input = ""
            except Exception:
                result = "Ошибка"
        
        # Вычисление квадратного корня
        elif key == ord('r') or key == ord('R'):
            try:
                result = str(math.sqrt(float(current_input)))
                current_input = ""
            except:
                result = "Ошибка"
        
        # Возведение в степень
        elif key == ord('^'):
            current_input += '**'
        
        # Смена знака числа
        elif key == ord('s'):
            try:
                current_input = str(-float(current_input))
            except:
                result = "Ошибка"
        
        # Вычисление обратного числа
        elif key == ord('i'):
            try:
                result = str(1 / float(current_input))
                current_input = ""
            except:
                result = "Ошибка"
        
        # Вычисление логарифма
        elif key == ord('l'):
            try:
                result = str(math.log(float(current_input)))
                current_input = ""
            except:
                result = "Ошибка"
        
        # Добавление открывающей скобки
        elif key == ord('('):
            current_input += '('
        
        # Добавление закрывающей скобки
        elif key == ord(')'):
            current_input += ')'
        
        # Добавление константы e
        elif key == ord('e'):
            current_input += str(math.e)

def remove_last_number_or_operator(expression):
    """Функция удаления последнего числа или оператора из выражения"""
    # Использует регулярные выражения для разбора выражения на части
    parts = re.findall(r'[\d.]+|[+\-*/]', expression)
    
    # Если есть элементы, удаляем последний
    if parts:
        return expression[:-len(parts[-1])]
    
    return expression

def main():
    # Главная функция запу��ка калькулятора
    # Использует curses.wrapper для корректной инициализации и завершения работы curses
    curses.wrapper(calculator)

# Проверка, что скрипт запущен напрямую, а не импортирован
if __name__ == "__main__":
    main()