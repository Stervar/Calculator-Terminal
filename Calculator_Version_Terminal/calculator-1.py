# Импорт необходимых библиотек:
# curses - библиотека для создания текстового пользовательского интерфейса в терминале
# math - библиотека для математических операций
import curses
import math

def draw_calculator_frame(framework, current_input, result, show_result_button):
    # Функция отрисовки графического интерфейса калькулятора
    
    # Получаем максимальные размеры окна терминала (высота и ширина)
    height, width = framework.getmaxyx()
    
    # Расчет позиции для центрирования калькулятора на экране
    calc_width = 40  # Фиксированная ширина калькулятора
    start_x = (width - calc_width) // 2  # Координата X для центрирования
    start_y = (height - 15) // 2  # Координата Y для центрирования

    # Очистка экрана перед новой отрисовкой
    framework.clear()

    # Определение графической структуры калькулятора с использованием символов Unicode
    frame = [
        # Верхняя и нижняя границы, заголовок
        "╔══════════════════════════════════════╗",
        "║            КАЛЬКУЛЯТОР               ║",
        "╠══════════════════════════════════════╣",
        "║                                      ║",
        "╠══════════════════════════════════════╣",
        # Кнопки калькулятора
        "║  7   │   8   │   9   │   /   │  CE   ║",
        "║------+--------+--------+--------+----║",
        "║  4   │   5   │   6   │   *   │   √   ║",
        "║------+--------+--------+--------+----║",
        "║  1   │   2   │   3   │   -   │   %   ║",
        "║------+--------+--------+--------+----║",
        "║  0   │   .   │   +   │ Backspace     ║"
    ]

    # Динамическое добавление кнопки "=" при наличии результата
    if show_result_button:
        frame.append("║                │   =   │             ║")
    
    # Закрытие рамки калькулятора
    frame.append("╚══════════════════════════════════════╝")

    # Отрисовка каждой линии рамки на экране
    for idx, line in enumerate(frame):
        framework.addstr(start_y + idx, start_x, line)

    # Вывод текущего ввода пользователя
    framework.addstr(start_y + 3, start_x + 2, f"Ввод: {current_input}")
    
    # Вывод результата вычисления, если он есть
    if result:
        framework.addstr(start_y + 3, start_x + 25, f"Результат: {result}")

    # Обновление экрана для отображения изменений
    framework.refresh()

def calculator(special_keys):
    # Основная функция логики калькулятора
    
    # Инициализация цветов и скрытие курсора
    curses.start_color()
    curses.curs_set(0)  # Делает курсор невидимым
    
    # Инициализация переменных состояния калькулятора
    current_input = ""  # Текущий вводимый пользователем текст
    result = ""  # Результат вычисления
    show_result_button = False  # Флаг для отображения кнопки результата
    
    # Основной цикл обработки событий
    while True:
        # Отрисовка интерфейса калькулятора
        draw_calculator_frame(special_keys, current_input, result, show_result_button)
        
        # Получение нажатой клавиши
        key = special_keys.getch()
        
        # Обработка различных сценариев нажатия клавиш
        if key == ord('q'):  # Выход из программы
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
        
        # Очистка всего ввода (клавиша C)
        elif key == ord('c') or key == ord('C'):
            current_input = ""
            result = ""
            show_result_button = False
        
        # Удаление последнего слова (клавиша E)
        elif key == ord('e') or key == ord('E'):
            current_input = current_input[:-len(current_input.split()[-1]) if current_input.split() else 0]
            show_result_button = False
        
        # Удаление последнего символа (Backspace)
        elif key == 263 or key == 127:
            current_input = current_input[:-1]
            show_result_button = False
        
        # Вычисление результата (=, Enter, %)
        elif key == ord('=') or key == 10 or key == ord('%'):
            try:
                # Обработка процентов
                if key == ord('%'):
                    result = str(eval(f"{current_input}/100"))
                else:
                    # Вычисление обычного выражения
                    result = str(eval(current_input))
                show_result_button = True
            except Exception:
                # Обработка ошибок вычисления
                result = "Ошибка"
                show_result_button = False
        
        # Вычисление квадратного корня (клавиша R)
        elif key == ord('r') or key == ord('R'):
            try:
                result = str(math.sqrt(float(current_input)))
                show_result_button = True
            except:
                result = "Ошибка"
                show_result_button = False

def main():
    # Основная функция запуска, использующая обертку curses
    curses.wrapper(calculator)

# Проверка, что скрипт запускается напрямую, а не импортируется
if __name__ == "__main__":
    main()
    
#     Основные особенности кода:

# Использует библиотеку curses для создания текстового интерфейса
# Реализует базовые математические операции
# Поддерживает ввод цифр, операторов и специальных функций
# Обработка ошибок при вычислениях
# Интерактивный интерфейс с возможностью навигации через клавиши
# Код представляет собой консольный калькулятор с графическим интерфейсом, который работает в терминале и поддерживает базовые математические операции.