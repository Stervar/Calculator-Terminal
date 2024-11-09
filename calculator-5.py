import curses
import math
import re

def draw_calculator_frame(stdscr, current_input, result):
    try:
        # Получаем размеры экрана
        height, width = stdscr.getmaxyx()
        
        # Проверяем минимальный размер окна
        if height < 30 or width < 150:  # Увеличил минимальную ширину
            stdscr.clear()
            stdscr.addstr(height//2, 0, "Увеличьте размер окна терминала!")
            stdscr.refresh()
            return
        
        # Рассчитываем позицию для центрирования
        calc_width = 60
        start_x = max(0, (width - calc_width) // 2)
        start_y = max(0, (height - 24) // 2)

        # Инструкции слева с рамкой
        instructions_left = [
            "╔═══════════════════════════════════╗",
            "║           УПРАВЛЕНИЕ             ║",
            "╠═══════════════════════════════════╣",
            "║ Кнопки    Действие               ║",
            "╠═══════════════════════════════════╣",
            "║ 1-9,0     Ввод цифр              ║",
            "║ +−×÷      Мат. операции          ║",
            "║ =         Результат              ║",
            "║ C         Очистка экрана         ║",
            "║ ←         Удаление символа       ║",
            "║ ±         Смена знака            ║",
            "╚═══════════════════════════════════╝"
        ]

        # Инструкции справа с рамкой
        instructions_right = [
            "╔═══════════════════════════════════╗",
            "║         ДОПОЛНИТЕЛЬНО            ║",
            "╠═══════════════════════════════════╣",
            "║ Кнопки    Действие               ║",
            "╠═══════════════════════════════════╣",
            "║ ( )       Скобки                 ║",
            "║ .         Десятичная дробь       ║",
            "║ 1/x       Обратное число         ║",
            "║ x²        Возведение в квадрат   ║",
            "║ √         Квадратный корень      ║",
            "║ log       Логарифм               ║",
            "║ e         Число Эйлера           ║",
            "╚═══════════════════════════════════╝"
        ]

        # Отрисовка левых инструкций
        for i, line in enumerate(instructions_left):
            stdscr.addstr(start_y + i, start_x - 40, line)

        # Отрисовка правых инструкций
        for i, line in enumerate(instructions_right):
            stdscr.addstr(start_y + i, start_x + calc_width + 5, line)

        # Основная рамка калькулятора 
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

        # Отрисовка рамки
        for idx, line in enumerate(frame):
            stdscr.addstr(start_y + idx, start_x, line)

        # Отображение ввода
        stdscr.addstr(start_y + 3, start_x + 2, f"Ввод: {current_input}")
        
        # Отображение результата
        if result:
            stdscr.addstr(start_y + 3, start_x + 35, f"Результат: {result}")

        stdscr.refresh()
    
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Произошла ошибка: {str(e)}")
        stdscr.refresh()

def calculator(stdscr):
    # Настройка цветов
    curses.start_color()
    curses.curs_set(0)  # Скрываем курсор
    
    # Инициализация переменных
    current_input = ""
    result = ""
    
    while True:
        # Отрисовка калькулятора
        draw_calculator_frame(stdscr, current_input, result)
        
        # Получение нажатия клавиши
        key = stdscr.getch()
        
        # Обработка нажатий
        if key == ord('q'):
            break
        
        elif key in [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), 
                    ord('5'), ord('6'), ord('7'), ord('8'), ord('9'), ord('.')]:
            # Если есть результат, начинаем новый ввод
            if result:
                current_input = chr(key)
                result = ""
            else:
                current_input += chr(key)
        
        elif key in [ord('+'), ord('-'), ord('*'), ord('/')]:
            # Если есть результат, используем его как начало нового выражения
            if result:
                current_input = result + chr(key)
                result = ""
            else:
                current_input += chr(key)
        
        # Полная очистка (C)
        elif key == ord('c') or key == ord('C'):
            current_input = ""
            result = ""
        
        # Очистка последнего элемента (CE)
        elif key == ord('e') or key == ord('E'):
            current_input = remove_last_number_or_operator(current_input)
        
        # Backspace - удаление последнего символа
        elif key == 263 or key == 127:  # Коды Backspace
            current_input = current_input[:-1]
        
        # Вычисление результата
        elif key == ord('=') or key == 10:
            try:
                result = str(eval(current_input))
                current_input = ""  # Очищаем ввод после получения результата
            except Exception:
                result = "Ошибка"
        
        # Процент
        elif key == ord('%'):
            try:
                result = str(eval(f"{current_input}/100"))
                current_input = ""
            except Exception:
                result = "Ошибка"
        
        
        # Квадратный корень
        elif key == ord('r') or key == ord('R'):
            try:
                result = str(math.sqrt(float(current_input)))
                current_input = ""
            except:
                result = "Ошибка"
        
        # Возведение в степень
        elif key == ord('^'):
            current_input += '**'
        
        # Смена знака
        elif key == ord('s'):  # sign
            try:
                current_input = str(-float(current_input))
            except:
                result = "Ошибка"
        
        # Обратное число
        elif key == ord('i'):  # inverse
            try:
                result = str(1 / float(current_input))
                current_input = ""
            except:
                result = "Ошибка"
        
        # Логарифм
        elif key == ord('l'):  # log
            try:
                result = str(math.log(float(current_input)))
                current_input = ""
            except:
                result = "Ошибка"
        
        # Открывающая скобка
        elif key == ord('('):
            current_input += '('
        
        # Закрывающая скобка
        elif key == ord(')'):
            current_input += ')'
        
        # Константа e
        elif key == ord('e'):
            current_input += str(math.e)

def remove_last_number_or_operator(expression):
    """Удаляет последнее число или оператор"""
    # Разбиваем выражение на части
    parts = re.findall(r'[\d.]+|[+\-*/]', expression)
    
    # Если есть элементы, удаляем последний
    if parts:
        return expression[:-len(parts[-1])]
    
    return expression

def main():
    curses.wrapper(calculator)

if __name__ == "__main__":
    main()