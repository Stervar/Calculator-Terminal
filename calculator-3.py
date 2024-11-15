import curses
import math
import re

def draw_calculator_frame(framework, current_input, result):
    # Получаем размеры экрана
    height, width = framework.getmaxyx()
    
    # Рассчитываем позицию для центрирования
    calc_width = 60
    start_x = (width - calc_width) // 2
    start_y = (height - 20) // 2

    # Стираем предыдущее содержимое
    framework.clear()

    # Рамка калькулятора
    frame = [
        "╔═══════════════════════════════════════════════════╗",
        "║                   КАЛЬКУЛЯТОР                     ║",
        "╠═══════════════════════════════════════════════════╣",
        "║                                                   ║",
        "╠═══════════════════════════════════════════════════╣",
        "║   7    │    8    │    9    │    /    │    CE      ║",
        "║--------+---------+---------+---------+------------║",
        "║   4    │    5    │    6    │    *    │    √       ║",
        "║--------+---------+---------+---------+------------║",
        "║   1    │    2    │    3    │    -    │    %       ║",
        "║--------+---------+---------+---------+------------║",
        "║   0    │    .    │    +    │ Backspace            ║"
    ]


    frame.append("╠═══════════════════════════════════════════════════╣")
    frame.append("║ Backspace - удаляет символ | CE - удаляет число   ║")
    frame.append("║ C - полная очистка | = появится при вводе         ║")
    frame.append("╚═══════════════════════════════════════════════════╝")

    # Отрисовка рамки
    for idx, line in enumerate(frame):
        framework.addstr(start_y + idx, start_x, line)

    # Отображение ввода
    framework.addstr(start_y + 3, start_x + 2, f"Ввод: {current_input}")
    
    # Отображение результата
    if result:
        framework.addstr(start_y + 3, start_x + 35, f"Результат: {result}")

    framework.refresh()

def calculator(special_keys):
    # Настройка цветов
    curses.start_color()
    curses.curs_set(0)  # Скрываем курсор
    
    # Инициализация переменных
    current_input = ""
    result = ""
    
    while True:
        # Отрисовка калькулятора
        draw_calculator_frame(special_keys, current_input, result)
        
        # Получение нажатия клавиши
        key = special_keys.getch()
        
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
                current_input = ""  # Очищаем ввод после получения результата
            except Exception:
                result = "Ошибка"
        
        # Квадратный корень
        elif key == ord('r') or key == ord('R'):
            try:
                result = str(math.sqrt(float(current_input)))
                current_input = ""  # Очищаем ввод после получения результата
            except:
                result = "Ошибка"

def remove_last_number_or_operator(expression):
    """Удаляет последнее число или оператор"""
    # Разбиваем выражение на части
    parts = re.findall(r'[\d.]+|[+\-*/]', expression)
    
    # Если есть элементы, удаляем последний
    if parts:
        return expression[:-len(parts[-1])]
    
    return expression

def is_valid_expression(expression):
    """Проверяет, можно ли показать кнопку = """
    # Проверяем наличие полного выражения с двумя операндами
    match = re.match(r'^-?\d+(\.\d+)?[+\-*/]-?\d+(\.\d+)?$', expression)
    return bool(match)

def main():
    curses.wrapper(calculator)

if __name__ == "__main__":
    main()