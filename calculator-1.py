import curses
import math

def draw_calculator_frame(framework, current_input, result, show_result_button):
    # Получаем размеры экрана
    height, width = framework.getmaxyx()
    
    # Рассчитываем позицию для центрирования
    calc_width = 40
    start_x = (width - calc_width) // 2
    start_y = (height - 15) // 2

    # Стираем предыдущее содержимое
    framework.clear()

    # Рамка калькулятора
    frame = [
        "╔══════════════════════════════════════╗",
        "║            КАЛЬКУЛЯТОР               ║",
        "╠══════════════════════════════════════╣",
        "║                                      ║",
        "╠══════════════════════════════════════╣",
        "║  7   │   8   │   9   │   /   │  CE   ║",
        "║------+--------+--------+--------+----║",
        "║  4   │   5   │   6   │   *   │   √   ║",
        "║------+--------+--------+--------+----║",
        "║  1   │   2   │   3   │   -   │   %   ║",
        "║------+--------+--------+--------+----║",
        "║  0   │   .   │   +   │ Backspace     ║"
    ]

    # Если есть результат, добавляем кнопку =
    if show_result_button:
        frame.append("║                │   =   │             ║")
    
    frame.append("╚══════════════════════════════════════╝")

    # Отрисовка рамки
    for idx, line in enumerate(frame):
        framework.addstr(start_y + idx, start_x, line)

    # Отображение ввода
    framework.addstr(start_y + 3, start_x + 2, f"Ввод: {current_input}")
    
    # Отображение результата
    if result:
        framework.addstr(start_y + 3, start_x + 25, f"Результат: {result}")

    framework.refresh()

def calculator(special_keys):
    # Настройка цветов
    curses.start_color()
    curses.curs_set(0)  # Скрываем курсор
    
    # Инициализация переменных
    current_input = ""
    result = ""
    show_result_button = False
    
    while True:
        # Отрисовка калькулятора
        draw_calculator_frame(special_keys, current_input, result, show_result_button)
        
        # Получение нажатия клавиши
        key = special_keys.getch()
        
        # Обработка нажатий
        if key == ord('q'):
            break
        
        elif key in [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), 
                    ord('5'), ord('6'), ord('7'), ord('8'), ord('9'), ord('.')]:
            current_input += chr(key)
            show_result_button = False
        
        elif key in [ord('+'), ord('-'), ord('*'), ord('/')]:
            current_input += chr(key)
            show_result_button = False
        
        elif key == ord('c') or key == ord('C'):
            current_input = ""
            result = ""
            show_result_button = False
        
        elif key == ord('e') or key == ord('E'):
            current_input = current_input[:-len(current_input.split()[-1]) if current_input.split() else 0]
            show_result_button = False
        
        elif key == 263 or key == 127:  # Backspace
            current_input = current_input[:-1]
            show_result_button = False
        
        elif key == ord('=') or key == 10 or key == ord('%'):
            try:
                if key == ord('%'):
                    result = str(eval(f"{current_input}/100"))
                else:
                    result = str(eval(current_input))
                show_result_button = True
            except Exception:
                result = "Ошибка"
                show_result_button = False
        
        elif key == ord('r') or key == ord('R'):
            try:
                result = str(math.sqrt(float(current_input)))
                show_result_button = True
            except:
                result = "Ошибка"
                show_result_button = False

def main():
    curses.wrapper(calculator)

if __name__ == "__main__":
    main()