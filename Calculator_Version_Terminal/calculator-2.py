# Импорт необходимых библиотек
import curses  # Библиотека для создания текстового интерфейса в терминале
import math    # Библиотека для математических операций

def draw_calculator_frame(framework, current_input, result, show_result_button):
    """
    Функция отрисовки графического интерфейса калькулятора
    
    Параметры:
    - framework: объект окна curses
    - current_input: текущий введенный пользователем текст
    - result: результат вычисления
    - show_result_button: флаг для отображения кнопки результата
    """
    # Получаем полные размеры экрана терминала
    height, width = framework.getmaxyx()
    
    # Расчет позиции для центрирования калькулятора
    calc_width = 60  # Фиксированная ширина калькулятора
    start_x = (width - calc_width) // 2  # Центрирование по горизонтали
    start_y = (height - 20) // 2  # Центрирование по вертикали

    # Очистка экрана перед новой отрисовкой
    framework.clear()

    # Определение графической структуры калькулятора с использованием символов Unicode
    frame = [
        # Верхняя часть рамки с заголовком
        "╔═══════════════════════════════════════════════════╗",
        "║                   КАЛЬКУЛЯТОР                     ║",
        "╠═══════════════════════════════════════════════════╣",
        "║                                                   ║",
        "╠═══════════════════════════════════════════════════╣",
        
        # Кнопки калькулятора
        "║   7    │    8    │    9    │    /    │    CE      ║",
        "║--------+---------+---------+---------+------------║",
        "║   4    │    5    │    6    │    *    │    √       ║",
        "║--------+---------+---------+---------+------------║",
        "║   1    │    2    │    3    │    -    │    %       ║",
        "║--------+---------+---------+---------+------------║",
        "║   0    │    .    │    +    │ Backspace            ║"
    ]

    # Динамическое добавление кнопки "=" при наличии результата
    if show_result_button:
        frame.append("║                   │    =    │                   ║")
    
    # Добавление нижней части рамки с инструкциями
    frame.append("╠═══════════════════════════════════════════════════╣")
    frame.append("║ Инструкция: Символы:+,-,*,/ | C-очистка | q-выход,║")
    frame.append("╚═══════════════════════════════════════════════════╝")

    # Отрисовка каждой линии рамки на экране
    for idx, line in enumerate(frame):
        framework.addstr(start_y + idx, start_x, line)

    # Вывод текущего ввода пользователя
    framework.addstr(start_y + 3, start_x + 2, f"Ввод: {current_input}")
    
    # Вывод результата вычисления
    if result:
        framework.addstr(start_y + 3, start_x + 35, f"Результат: {result}")

    # Обновление экрана для отображения изменений
    framework.refresh()

def calculator(special_keys):
    """
    Основная функция логики калькулятора
    
    Параметры:
    - special_keys: объект окна curses для обработки клавиш
    """
    # Инициализация цветов и настроек curses
    curses.start_color()  # Подготовка к использованию цветов
    curses.curs_set(0)    # Скрытие курсора
    
    # Инициализация переменных состояния калькулятора
    current_input = ""  # Текущий вводимый текст
    result = ""         # Результат вычисления
    show_result_button = False  # Флаг отображения кнопки результата
    
    # Основной цикл обработки событий
    while True:
        # Отрисовка интерфейса калькулятора
        draw_calculator_frame(special_keys, current_input, result, show_result_button)
        
        # Получение нажатой клавиши
        key = special_keys.getch()
        
        # Обработка различных сценариев нажатия клавиш
        
        # Выход из программы
        if key == ord('q'):
            break
        
        # Ввод цифр и точки
        elif key in [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), 
                    ord('5'), ord('6'), ord('7'), ord('8'), ord('9'), ord('.')]:
            current_input += chr(key)
            show_result_button = False
        
        # Ввод математических операторов
        elif key in [ord('+'), ord('-'), ord('*'), ord('/')]:
            current_input += chr(key)
            show_result_button = False
        
        # Полная очистка (клавиша C)
        elif key == ord('c') or key == ord('C'):
            current_input = ""
            result = ""
            show_result_button = False
        
        # Очистка последнего элемента (CE)
        elif key == ord('e') or key == ord('E'):
            if current_input:
                # Удаление последнего числа или оператора
                current_input = ' '.join(current_input.split()[:-1])
            show_result_button = False
        
        # Удаление последнего символа (Backspace)
        elif key == 263 or key == 127:
            current_input = current_input[:-1]
            show_result_button = False
        
        # Вычисление результата
        elif key == ord('=') or key == 10:
            try:
                # Вычисление выражения с помощью eval()
                result = str(eval(current_input))
                show_result_button = True
            except Exception:
                # Обработка ошибок вычисления
                result = "Ошибка"
                show_result_button = False
        
        # Вычисление процента
        elif key == ord('%'):
            try:
                result = str(eval(f"{current_input}/100"))
                show_result_button = True
            except Exception:
                result = "Ошибка"
                show_result_button = False
        
        # Вычисление квадратного корня
        elif key == ord('r') or key == ord('R'):
            try:
                result = str(math.sqrt(float(current_input)))
                show_result_button = True
            except:
                result = "Ошибка"
                show_result_button = False

def main():
    """
    Основная функция запуска калькулятора
    Использует обертку curses для корректной инициализации и закрытия
    """
    curses.wrapper(calculator)

# Проверка, что скрипт запускается напрямую
if __name__ == "__main__":
    main()