# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 10:52:47 2026

@author: mrwol
"""


import tkinter as tk
from math import sqrt
import os
import sys  # тоже пригодится для sys._MEIPASS если используете PyInstaller



class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("MSI Calculator 4.3")
        self.window.resizable(False, False)
        self.window.geometry("412x471")

        self.canvas = tk.Canvas(self.window, width=412, height=469)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", lambda e: self.window.focus_set())

        # Фон
        # Определяем базовую директорию, где находится скрипт
        if getattr(sys, 'frozen', False):
            # Если программа упакована в EXE (PyInstaller)
            base_dir = sys._MEIPASS
        else:
            # Если запущен как скрипт Python
            base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Полный путь к изображению
        image_full_path = os.path.join(base_dir, "msi_calculator471.png")
        
        # Проверяем существование файла
        if not os.path.exists(image_full_path):
            # Если не нашли, пробуем искать в рабочей директории
            image_full_path = os.path.join(os.getcwd(), "msi_calculator471_3.png")
        
        print(f"Загружаем изображение из: {image_full_path}")
        
        # Инициализируем bg_image как None
        self.bg_image = None
        
        try:
            if os.path.exists(image_full_path):
                self.bg_image = tk.PhotoImage(file=image_full_path)
                self.canvas.create_image(0, 0, image=self.bg_image, anchor='nw')
                print("Изображение загружено успешно")
            else:
                print(f"ПРЕДУПРЕЖДЕНИЕ: Файл изображения не найден: {image_full_path}")
                # Создаем серый фон вместо изображения
                self.canvas.create_rectangle(0, 0, 412, 469, fill='#2b2b2b', outline='')
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            # Создаем серый фон на случай ошибки
            self.canvas.create_rectangle(0, 0, 412, 469, fill='#2b2b2b', outline='')
        
       
        self.create_button_regions()

        self.memory = 0.0
        self.current_input = ''      # текущее вводимое число
        self.pending_operator = ''   # последний введённый оператор
        self.full_expression = ''    # полное выражение для вычисления
        self.waiting_for_operand = False  # ← новое поле

        # Основной дисплей — только число
        self.display_id = self.canvas.create_text(
            382, 62, text='0', font=("Digital-7", 50), fill='white', anchor='e'
        )
        # Оператор — в левом нижнем углу дисплея
        self.operator_id = self.canvas.create_text(
            38, 80, text='', font=("Digital-7", 24), fill='white', anchor='w'
        )

        # Привязка клавиш
        self.window.bind('<Control-KeyPress>', self.handle_ctrl_keys)
        self.window.bind('<Delete>', self.clear_entry)
        self.window.bind('<Key>', self.handle_key)
        
        self.window.mainloop()
        

    def is_operator(self, char):
        return char in '+-*/'
    
    def handle_ctrl_keys(self, event):
        # keycode 67 = C, keycode 86 = V на всех раскладках
        if event.keycode == 67:  # Ctrl+C
            return self.copy_to_clipboard(event)
        elif event.keycode == 86:  # Ctrl+V
            return self.paste_from_clipboard(event)

    def handle_key(self, event):


    # Игнорируем служебные клавиши
        if event.keysym in ('Control_L', 'Control_R', 'Alt_L', 'Alt_R', 'Shift_L', 'Shift_R'):
            return
        if not event.char and event.keysym not in ('Return', 'Escape', 'BackSpace', 'Delete', 's', 'plus', 'minus', 'asterisk', 'slash', 'KP_Add', 'KP_Subtract', 'KP_Multiply', 'KP_Divide'):
            return

        key = event.char
        keysym = event.keysym

    # Цифры и точка — по char
        if key in '0123456789.':
            self.append(key)
    # Операторы — по keysym (для всех раскладок и numpad)
        elif keysym in ('plus', 'KP_Add'):
            self.append('+')
        elif keysym in ('minus', 'KP_Subtract'):
            self.append('-')
        elif keysym in ('asterisk', 'KP_Multiply'):
            self.append('*')
        elif keysym in ('slash', 'KP_Divide'):
            self.append('/')
        elif key == '%':
            self.percent()
        elif keysym == 'Return':
            self.calculate()
        elif keysym == 'Escape':
            self.all_clear()
        elif keysym == 'BackSpace':
            self.delete_last()
        elif keysym == 'Delete':
            self.clear_entry()
        elif keysym == 's':
            self.square_root()

    def append(self, char):
        if self.is_operator(char):
        # Специальный случай: начало с минуса
            if char == '-' and not self.full_expression and not self.current_input:
                self.current_input = '-'
                self.pending_operator = ''
                self.waiting_for_operand = False
            elif self.current_input or self.full_expression:
                self.pending_operator = char
                if not self.waiting_for_operand:  # ← Новый if: добавляем только если НЕ ждём операнда (т.е. после числа)
                    if self.current_input:
                        self.full_expression += self.current_input + char
                    self.waiting_for_operand = True
                else:  # ← Новый else: если ждём операнда (после предыдущего оператора), просто заменяем последний оператор
                    if self.full_expression and self.is_operator(self.full_expression[-1]):
                        self.full_expression = self.full_expression[:-1] + char
        else:
            if self.waiting_for_operand:
                self.current_input = ''
                self.waiting_for_operand = False
            if char == '.' and '.' in self.current_input:
                return
        # Если после = вводим число — сбрасываем всё
            if self.full_expression == '' and self.pending_operator == '' and self.current_input and not self.current_input.replace('.','').replace('-','').isdigit():
                self.current_input = ''
            self.current_input += char
            self.pending_operator = ''
        self.update_display()

    def update_display(self):
        display_text = self.current_input[-13:] if self.current_input else '0'  # Ограничение на 13 символов
        text_len = len(display_text)
    
    # Динамический размер шрифта
        if text_len <= 10:
            font_size = 50
        elif text_len <= 13:
            font_size = 40
        else:
            font_size = 40  # На всякий случай, если >13 (хотя обрезка предотвратит)
    
        self.canvas.itemconfig(self.display_id, text=display_text, font=("Digital-7", font_size))
        self.canvas.itemconfig(self.operator_id, text=self.pending_operator)

    def delete_last(self):
        if self.waiting_for_operand:
            return
        if self.current_input:
            self.current_input = self.current_input[:-1]
        self.update_display()

    def clear_entry(self, event=None):
        if not self.waiting_for_operand:
            self.current_input = ''
        self.update_display()

    def all_clear(self, event=None):
        self.current_input = ''
        self.pending_operator = ''
        self.full_expression = ''
        self.waiting_for_operand = False
        self.memory = 0.0
        self.update_display()
        return "break"  # ← Добавлено: предотвращает распространение события

    def sign_change(self):
        if self.current_input:
            if self.current_input == '0':
                return
            if self.current_input[0] == '-':
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.update_display()

    def percent(self):
    # """Обработка операции "%": преобразование текущего ввода в проценты."""
        if self.current_input and self.current_input != 'Error':
            # Получаем текущее число
            current_value = float(self.current_input)
            
            # Извлекаем предыдущее число из full_expression
            prev_value = None
            operators = ['+', '-', '*', '/']
            for op in reversed(operators):
                pos = self.full_expression.rfind(op)
                if pos != -1:
                    prev_value_str = self.full_expression[:pos]
                    try:
                        prev_value = float(prev_value_str.strip())  # Преобразуем строку в число
                    except ValueError:
                        continue
                    break
            
            # Если предыдущие значения найдены, используем их
            if prev_value is not None:
                # Вычисляем процент от предыдущего числа
                percentage_value = prev_value * (current_value / 100)
                # Обновляем текущее число, используя рассчитанный процент
                self.current_input = str(percentage_value)
            else:
                # Если полных значений нет, просто делим текущее число на 100
                self.current_input = str(current_value / 100)
            
            self.update_display()

    def square_root(self):
        if self.current_input and self.current_input != 'Error':
            try:
                value = float(self.current_input)
                if value < 0:
                    self.current_input = 'Error'
                else:
                    self.current_input = self.format_result(sqrt(value))
                self.update_display()
            except:
                self.current_input = 'Error'
                self.update_display()

    def memory_add(self):
        if self.current_input and self.current_input != 'Error':
            try:
                self.memory += float(self.current_input)
            except:
                pass
        self.current_input = ''
        self.update_display()

    def memory_subtract(self):
        if self.current_input and self.current_input != 'Error':
            try:
                self.memory -= float(self.current_input)
            except:
                pass
        self.current_input = ''
        self.update_display()

    def memory_recall(self):
        self.current_input = self.format_result(self.memory)
        self.update_display()

    def calculate(self):
        if not self.full_expression and not self.current_input:
            return
        expr = self.full_expression + self.current_input
        if not expr:
            return
        try:
            result = eval(expr)
            self.current_input = self.format_result(result)
            self.pending_operator = ''
            self.full_expression = ''
            self.waiting_for_operand = False
        except:
            self.current_input = 'Error'
            self.pending_operator = ''
            self.full_expression = ''
            self.waiting_for_operand = False
        self.update_display()

    def copy_to_clipboard(self, event=None):
        text = self.current_input if self.current_input and self.current_input != 'Error' else ''
        if not text and self.full_expression:
            try:
                result = eval(self.full_expression[:-1])  # без последнего оператора
                text = self.format_result(result)
            except:
                text = ''
        if text:
            self.window.clipboard_clear()
            self.window.clipboard_append(text)
        return "break"  # ← Добавлено: предотвращает распространение события    

    def paste_from_clipboard(self, event=None):
        try:
            content = self.window.clipboard_get()
            allowed = "0123456789.-"  # Добавил минус
            cleaned = ''.join(c for c in content if c in allowed)
            if cleaned:
                self.current_input = cleaned
                self.pending_operator = ''
                self.full_expression = ''
                self.waiting_for_operand = False  # ← Важно!
                self.update_display()
        except tk.TclError:
            pass
        return "break"  

    def format_result(self, result):
        if isinstance(result, (int, float)):
            if abs(result) >= 1e13 or (0 < abs(result) < 1e-12):  # Пороги под 13 символов
                return f"{result:.10e}"  # .10e для точности в пределах 13 символов
        # Если float целое, преобразуем в int-строку (без .0)
            if isinstance(result, float) and result.is_integer():
                return str(int(result))[:13]
            else:
                s = str(result)
                if '.' in s:
                    integer, decimal = s.split('.')
                    if len(integer) >= 13:
                        return integer[:13]
                    max_dec = 13 - len(integer) - 1
                    decimal = decimal[:max_dec].rstrip('0')  # Убрать trailing 0
                    return integer + ('.' + decimal if decimal else '')  # Если decimal пустой, без точки
                return s[:13]
        return str(result)[:13]

    def create_button_regions(self):
        col_width = 350 // 5  # Approx 82
        display_height = 160   # Adjust if display position changes
        row_height = (400 - display_height) // 5  # Approx 78
        start_x = 35
        start_y = display_height

        buttons = [
            # Row 0
            {'tag': 'btn_msi', 'row': 0, 'col': 0, 'span_col': 1, 'command': lambda: self.append('*msi_calc*')},  # √
            #{'tag': 'btn_MR', 'row': 0, 'col': 1, 'span_col': 1, 'command': self.memory_recall},
            #{'tag': 'btn_M-', 'row': 0, 'col': 2, 'span_col': 1, 'command': self.memory_subtract},
            #{'tag': 'btn_M+', 'row': 0, 'col': 3, 'span_col': 1, 'command': self.memory_add},
            {'tag': 'btn_sqrt', 'row': 0, 'col': 4, 'span_col': 1, 'command': self.square_root},  # √

            # Row 1
            {'tag': 'btn_sign', 'row': 1, 'col': 0, 'span_col': 1, 'command': self.delete_last},  # +/-
            {'tag': 'btn_MR', 'row': 1, 'col': 1, 'span_col': 1, 'command': self.memory_recall},
            {'tag': 'btn_M-', 'row': 1, 'col': 2, 'span_col': 1, 'command': self.memory_subtract},
            {'tag': 'btn_M+', 'row': 1, 'col': 3, 'span_col': 1, 'command': self.memory_add},
            {'tag': 'btn_div', 'row': 1, 'col': 4, 'span_col': 1, 'command': lambda: self.append('/')},  # ÷

            # Row 2
            {'tag': 'btn_plus>', 'row': 2, 'col': 0, 'span_col': 1, 'command': self.sign_change},  # +/-
            {'tag': 'btn_7', 'row': 2, 'col': 1, 'span_col': 1, 'command': lambda: self.append('7')},
            {'tag': 'btn_8', 'row': 2, 'col': 2, 'span_col': 1, 'command': lambda: self.append('8')},
            {'tag': 'btn_9', 'row': 2, 'col': 3, 'span_col': 1, 'command': lambda: self.append('9')},
            {'tag': 'btn_mult', 'row': 2, 'col': 4, 'span_col': 1, 'command': lambda: self.append('*')},

            # Row 3
            {'tag': 'btn_percent', 'row': 3, 'col': 0, 'span_col': 1, 'command': self.percent},  # %
            {'tag': 'btn_4', 'row': 3, 'col': 1, 'span_col': 1, 'command': lambda: self.append('4')},
            {'tag': 'btn_5', 'row': 3, 'col': 2, 'span_col': 1, 'command': lambda: self.append('5')},
            {'tag': 'btn_6', 'row': 3, 'col': 3, 'span_col': 1, 'command': lambda: self.append('6')},
            {'tag': 'btn_minus', 'row': 3, 'col': 4, 'span_col': 1, 'command': lambda: self.append('-')},

            # Row 4
            {'tag': 'btn_AC', 'row': 4, 'col': 0, 'span_col': 1, 'command': self.all_clear},
            {'tag': 'btn_1', 'row': 4, 'col': 1, 'span_col': 1, 'command': lambda: self.append('1')},
            {'tag': 'btn_2', 'row': 4, 'col': 2, 'span_col': 1, 'command': lambda: self.append('2')},
            {'tag': 'btn_3', 'row': 4, 'col': 3, 'span_col': 1, 'command': lambda: self.append('3')},
            {'tag': 'btn_plus', 'row': 4, 'col': 4, 'span_col': 1, 'command': lambda: self.append('+')},
            
            # Row 5
            {'tag': 'btn_ce', 'row': 5, 'col': 0, 'span_col': 1, 'command': self.clear_entry},  # /AC as clear_entry (CE)
            {'tag': 'btn_0', 'row': 5, 'col': 1, 'span_col': 1, 'command': lambda: self.append('0')},
            {'tag': 'btn_dot', 'row': 5, 'col': 2, 'span_col': 1, 'command': lambda: self.append('.')},
            {'tag': 'btn_equal', 'row': 5, 'col': 3, 'span_col': 1, 'command': self.calculate},           # =
            {'tag': 'btn_plus', 'row': 5, 'col': 4, 'span_col': 1, 'command': lambda: self.append('+')},
        ]

        for btn in buttons:
            row = btn['row']
            col = btn['col']
            span_col = btn.get('span_col', 1)
            x1 = start_x + col * col_width
            y1 = start_y + row * 47
            x2 = x1 + span_col * col_width
            y2 = y1 + 47
            self.canvas.create_rectangle(x1, y1, x2, y2, fill='', outline='', tags=btn['tag']) # red потом удалить
            self.canvas.tag_bind(btn['tag'], '<Button-1>', lambda e, cmd=btn['command']: cmd())

if __name__ == "__main__":
    Calculator()