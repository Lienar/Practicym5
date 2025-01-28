
import tkinter as tk
from tkinter import ttk, Toplevel, messagebox, filedialog
import json
from datetime import datetime
from tkcalendar import DateEntry
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import csv

# Файл для сохранения данных
data_file = 'training_log.json'
file_path = f'{os.path.dirname(__file__)}\\data'
user_name = 'Default'


def load_data():
    """Загрузка данных о тренировках из файла."""
    try:
        with open(data_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_data(data):
    """Сохранение данных о тренировках в файл."""
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)


class TrainingLogApp:
    def __init__(self, root):
        self.root = root
        root.title("Дневник тренировок")
        root.geometry("300x150")
        self.create_widgets()
        self.file_name = f'{user_name}_data'

    def create_widgets(self):
        """Функция для создания основного меню"""
        self.blank_label1 = ttk.Label(self.root, text=" ")
        self.blank_label1.grid(column=0, row=0, sticky=tk.EW, columnspan=1, pady=10)

        self.view_button = ttk.Button(self.root, text="Просмотреть записи", command=self.view_records)
        self.view_button.grid(column=2, row=0, sticky=tk.EW, columnspan=15, pady=10)
        '''Описания кнопки просмотра записей'''
        self.blank_label2 = ttk.Label(self.root, text=" ")
        self.blank_label2.grid(column=17, row=0, sticky=tk.EW, columnspan=1, pady=10)

        self.blank_label3 = ttk.Label(self.root, text=" ")
        self.blank_label3.grid(column=0, row=1, sticky=tk.EW, columnspan=1, pady=10)

        self.save_load_button = ttk.Button(self.root, text="Сохранить/Загрузить данные", command=self.save_load_window)
        self.save_load_button.grid(column=2, row=1, sticky=tk.EW, columnspan=15, pady=10)
        '''Описания кнопки экспорта/импорта данных в csv файлы'''
        self.blank_label4 = ttk.Label(self.root, text=" ")
        self.blank_label4.grid(column=17, row=1, sticky=tk.EW, columnspan=1, pady=10)

        self.blank_label5 = ttk.Label(self.root, text=" ")
        self.blank_label5.grid(column=0, row=2, sticky=tk.EW, columnspan=1, pady=10)

        def run_stat():
            self.show_stat('stat')


        def run_graf():
            self.show_stat('graf')


        self.show_stat_button = ttk.Button(self.root, text="Показать статистику", command=run_stat)
        self.show_stat_button.grid(column=2, row=2, sticky=tk.W, columnspan=4, pady=10)
        '''Описания кнопки создания вывода статистики'''
        self.show_progress_button = ttk.Button(self.root, text="Показать прогресс", command=run_graf)
        self.show_progress_button.grid(column=7, row=2, sticky=tk.E, columnspan=7, pady=10)
        '''Описание кнопки вывода графика'''
        self.blank_label6 = ttk.Label(self.root, text=" ")
        self.blank_label6.grid(column=17, row=2, sticky=tk.EW, columnspan=1, pady=10)

    def add_entry_window(self):
        """Функция создания окна добавления записи"""
        add_window = Toplevel(self.main_window)
        add_window.title("Меню добавления записи")
        self.date_widgets_creator(add_window, 1, 1, False)
        '''Создание зоны отображения ввода даты упражнения'''
        self.exercise_label = ttk.Label(add_window, text="Упражнение:")
        self.exercise_label.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5, columnspan=6)
        self.exercise_entry = ttk.Entry(add_window)
        self.exercise_entry.grid(column=2, row=3, sticky=tk.EW, padx=5, pady=5, columnspan=6)
        '''Создание строки для ввода названия упражнения'''
        self.weight_label = ttk.Label(add_window, text="Вес:")
        self.weight_label.grid(column=1, row=4, sticky=tk.W, padx=5, pady=5, columnspan=6)
        self.weight_entry = ttk.Entry(add_window)
        self.weight_entry.grid(column=2, row=4, sticky=tk.EW, padx=5, pady=5, columnspan=6)
        '''Создание строки для ввода веса задействованного в упражнение'''
        self.repetitions_label = ttk.Label(add_window, text="Повторения:")
        self.repetitions_label.grid(column=1, row=5, sticky=tk.W, padx=5, pady=5, columnspan=6)
        self.repetitions_entry = ttk.Entry(add_window)
        self.repetitions_entry.grid(column=2, row=5, sticky=tk.EW, padx=5, pady=5, columnspan=6)
        '''Создание строки для ввода количества повторений'''
        def add_entry_run():
            """Функция запуска процедуры добавления записи"""
            self.add_entry()
            self.main_window.destroy()
            self.view_records()

        self.add_button = ttk.Button(add_window, text="Добавить", command=add_entry_run)
        self.add_button.grid(column=2, row=6, sticky=tk.W, columnspan=3, pady=10)
        '''Создание кнопки активации добавления'''

    def add_entry(self):
        """Функция добавления записи"""
        date_text = f'{self.date_entry.get()} {self.hour_spin.get()}:{self.minute_spin.get()}:{self.second_spin.get()}'
        date = datetime.now().strftime(date_text)
        exercise = self.exercise_entry.get()
        weight = self.weight_entry.get()
        repetitions = self.repetitions_entry.get()
        '''Сбор данных записи'''

        if not (exercise and weight and repetitions):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return
        '''проверка наличия всех необходимых данных'''
        entry = {
            'date': date,
            'exercise': exercise,
            'weight': weight,
            'repetitions': repetitions
        }
        '''Создание записи по данным'''
        data = load_data()
        data.append(entry)
        data = self.bubble_sort(data)
        save_data(data)
        '''Добавление, сортировка и сохранение записей'''
        self.exercise_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.repetitions_entry.delete(0, tk.END)
        '''Очистка полей для ввода'''
        messagebox.showinfo("Успешно", "Запись успешно добавлена!")
        '''Вывод сообщения об успешном добавлении данных'''

    def save_load_window(self):
        """Функция создания окна контроля импортаэкспорта данных в csv файл"""
        self.save_load_window = Toplevel(self.root)
        self.save_load_window.title("Меню импорта экспорта файла в формате csv")
        def save_run():
            """Функция запуска экспорта"""
            self.save_records()
            self.save_load_window.destroy()

        def load_run():
            """Функция запуска импорта"""
            self.load_records()
            self.save_load_window.destroy()

        self.view_button = ttk.Button(self.save_load_window, text="Сохранить данные", command=save_run)
        self.view_button.grid(column=0, row=1, sticky=tk.W, columnspan=2, pady=10)
        '''Описание кнопки экспорта'''
        self.view_button = ttk.Button(self.save_load_window, text="Загрузить данные", command=load_run)
        self.view_button.grid(column=2, row=1, sticky=tk.E, columnspan=2, pady=10)
        '''Описание кнопки импорта'''

    def save_records(self):
        """Функция экспорта"""
        data = load_data()
        '''Получение данных'''

        file_name = filedialog.asksaveasfilename(
            initialdir="files",
            title="Сохранить как",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        with open(f"{file_name.title()}", 'w', newline='', encoding="windows-1251") as csvfile:
            result = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            data_head = ["date", "exercise", "weight", "repetitions"]
            result.writerow(data_head)
            for row in data:
                data_temp = [f"{row['date']}", f"{row['exercise']}", f"{row['weight']}", f"{row['repetitions']}"]
                result.writerow(data_temp)
        '''Запись данных в файл'''

    def load_records(self):
        """Функция импорта"""
        data_temp = []
        data_temp1 = []
        dic_temp = {}
        result_data = []
        '''Подготовка переменных для импорта'''

        file_name = filedialog.askopenfilename(
            initialdir="files",
            title="Выбрать файл",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        with open(f"{file_name.title()}", "r", encoding="windows-1251", ) as csvfile:
            readed = csv.reader(csvfile, delimiter=",")
            for row in readed:
                data_temp.append(row)
        '''Загрузка данных из файла'''
        for index in range(1, len(data_temp)):
            data_temp1.append(' ')
        '''Создание запасного массива'''
        for index in range(1, len(data_temp)):
            for i in range(0, len(data_temp[0])):
                dic_temp[data_temp[0][i]] = data_temp[index][i]
            data_temp1[index - 1] = dic_temp.copy()
        '''Удаление заголовка файла'''
        data_temp2 = load_data()
        '''Загрузка уже внесенных в таблицу данных'''
        for data in data_temp1:
            is_duble = False
            for data1 in data_temp2:
                if data == data1:
                    is_duble = True
            if is_duble == False:
                result_data.append(data.copy())
        '''Проверка на повторение данных'''
        for data in data_temp2:
            result_data.append(data.copy())
        result_data = self.bubble_sort(result_data)
        save_data(result_data)
        '''Создание результирующих данных и их запись'''

    def bubble_sort(self, data):
        """Функция пузырьковой сортировки данных по дате"""
        data_result = data
        for i in range(0, len(data_result)):
            for j in range(0, len(data_result) - i - 1):
                date1 = datetime.strptime(data_result[j]['date'], '%Y-%m-%d %H:%M:%S')
                date2 = datetime.strptime(data_result[j + 1]['date'], '%Y-%m-%d %H:%M:%S')
                if date1 > date2:
                    tempo = data_result[j]
                    data_result[j] = data_result[j + 1]
                    data_result[j + 1] = tempo
        return (data_result)

    def show_stat(self, show_type):
        """Функция отображения статистики в промежутку дат"""
        window = Toplevel(self.root)
        window.title("Окно статистики")
        column = 1
        row = 1
        '''Создание основного окна'''
        data = load_data()
        if len(data) >= 1:
            data = self.bubble_sort(data)
            start_date = data[0]['date']
            end_date = data[len(data) - 1]['date']
            start_date = self.date_control(start_date)
            end_date = self.date_control(end_date)
            '''Выбор первой и последней дат в списке'''
            start_label = ttk.Label(window, text="Дата начала статистики:")
            start_label.grid(column=column, row=row - 1, sticky=tk.EW, padx=5, pady=5, columnspan=column + 3)
            date_start_entry_label = ttk.Label(window, text="число/месяц/год")
            date_start_entry_label.grid(column=column, row=row, sticky=tk.EW, padx=5, pady=5)
            date_start_entry = DateEntry(window, width=10, background='darkblue', foreground='white',
                                         borderwidth=2, date_pattern='yyyy-mm-dd')
            date_start_entry.grid(column=column, row=row + 1, sticky=tk.W, padx=5, pady=5)
            date_start_entry.set_date(f'{start_date[0][0]}-{start_date[0][1]}-{start_date[0][2]}')
            hour_start_spin_label = ttk.Label(window, text="часы")
            hour_start_spin_label.grid(column=column + 1, row=row, sticky=tk.EW, padx=5, pady=5)
            hour_start_spin = ttk.Spinbox(window, from_=0, to=23, width=3, format="%02.0f", validate='key')
            hour_start_spin.grid(column=column + 1, row=row + 1, sticky=tk.EW, padx=5, pady=5)
            hour_start_spin.insert(0, start_date[1])
            minute_start_spin_label = ttk.Label(window, text="минуты")
            minute_start_spin_label.grid(column=column + 2, row=row, sticky=tk.EW, padx=5, pady=5)
            minute_start_spin = ttk.Spinbox(window, from_=0, to=59, width=3, format="%02.0f", validate='key')
            minute_start_spin.grid(column=column + 2, row=row + 1, sticky=tk.EW, padx=5, pady=5)
            minute_start_spin.insert(0, start_date[2])
            second_start_spin_label = ttk.Label(window, text="секунды")
            second_start_spin_label.grid(column=column + 3, row=row, sticky=tk.EW, padx=5, pady=5)
            second_start_spin = ttk.Spinbox(window, from_=0, to=59, width=3, format="%02.0f", validate='key')
            second_start_spin.grid(column=column + 3, row=row + 1, sticky=tk.EW, padx=5, pady=5)
            second_start_spin.insert(0, start_date[3])
            '''Создание поля для указания начальной даты'''

            end_label = ttk.Label(window, text="Дата окончания статистики:")
            end_label.grid(column=column, row=row + 2, sticky=tk.EW, padx=5, pady=5, columnspan=column + 3)
            date_end_entry_label = ttk.Label(window, text="число/месяц/год")
            date_end_entry_label.grid(column=column, row=row + 3, sticky=tk.EW, padx=5, pady=5)
            date_end_entry = DateEntry(window, width=10, background='darkblue', foreground='white',
                                       borderwidth=2, date_pattern='yyyy-mm-dd')
            date_end_entry.grid(column=column, row=row + 4, sticky=tk.W, padx=5, pady=5)
            date_end_entry.set_date(f'{end_date[0][0]}-{end_date[0][1]}-{end_date[0][2]}')
            hour_end_spin_label = ttk.Label(window, text="часы")
            hour_end_spin_label.grid(column=column + 1, row=row + 3, sticky=tk.EW, padx=5, pady=5)
            hour_end_spin = ttk.Spinbox(window, from_=0, to=23, width=3, format="%02.0f", validate='key')
            hour_end_spin.grid(column=column + 1, row=row + 4, sticky=tk.EW, padx=5, pady=5)
            hour_end_spin.insert(0, end_date[1])
            minute_end_spin_label = ttk.Label(window, text="минуты")
            minute_end_spin_label.grid(column=column + 2, row=row + 3, sticky=tk.EW, padx=5, pady=5)
            minute_end_spin = ttk.Spinbox(window, from_=0, to=59, width=3, format="%02.0f", validate='key')
            minute_end_spin.grid(column=column + 2, row=row + 4, sticky=tk.EW, padx=5, pady=5)
            minute_end_spin.insert(0, end_date[2])
            second_end_spin_label = ttk.Label(window, text="секунды")
            second_end_spin_label.grid(column=column + 3, row=row + 3, sticky=tk.EW, padx=5, pady=5)
            second_end_spin = ttk.Spinbox(window, from_=0, to=59, width=3, format="%02.0f", validate='key')
            second_end_spin.grid(column=column + 3, row=row + 4, sticky=tk.EW, padx=5, pady=5)
            second_end_spin.insert(0, end_date[3])
            '''Создание поля для указания конечной даты'''

            if show_type == 'graf':
                exer_option = self.exer_list_creator(data)
                exer_option.append('')
                exer_label = ttk.Label(window, text="Выбирете упражнение")
                exer_label.grid(column=1, row=row + 5, sticky=tk.EW, padx=5, pady=5, columnspan=2)
                exer_selected = tk.StringVar(window)
                exer_menu = tk.OptionMenu(window, exer_selected, *exer_option)
                exer_menu.grid(column=1, row=row + 6, sticky=tk.EW, padx=5, pady=5, columnspan=2)
                '''Создание выпадающего списка для выбора упражнения'''

            def run_show():
                """Функция запуска фильтрации"""
                try:
                    start_date = datetime.strptime(f'{date_start_entry.get()} {hour_start_spin.get()}'
                                                   f':{minute_start_spin.get()}:{second_start_spin.get()}',
                                                   '%Y-%m-%d %H:%M:%S')
                except:
                    messagebox.showerror("Ошибка", "Неверный формат даты начала фильтрации.")
                    return
                try:
                    end_date = datetime.strptime(f'{date_end_entry.get()} {hour_end_spin.get()}:'
                                                 f'{minute_end_spin.get()}:{second_end_spin.get()}',
                                                 '%Y-%m-%d %H:%M:%S')
                except:
                    messagebox.showerror("Ошибка", "Неверный формат даты окончания фильтрации.")
                    return

                '''Проверка корректности дат'''
                if start_date > end_date:
                    temp_date = start_date
                    start_date = end_date
                    end_date = temp_date
                '''Упорядочевание указанных дат'''
                stat_data = []
                data = load_data()
                for row in data:
                    date = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S')
                    if start_date <= date <= end_date:
                        stat_data.append(row)
                '''Выделение данных из общего пула по датам'''
                if show_type == 'stat':
                    self.stat_window_creator(stat_data, window)
                elif show_type == 'graf':
                    exer = exer_selected.get()
                    stat_date_info = [stat_data, exer, exer_option]
                    self.show_graf(stat_date_info, window)
                '''Отображение результата'''

            if show_type == 'stat':
                filter_button = ttk.Button(window, text="Показать статистику", command=run_show)
                filter_button.grid(column=column, row=row + 5, sticky=tk.EW, padx=5, pady=5, columnspan=column + 3)
            elif show_type == 'graf':
                filter_button = ttk.Button(window, text="Показать график", command=run_show)
                filter_button.grid(column=column, row=row + 7, sticky=tk.EW, padx=5, pady=5, columnspan=column + 3)
            '''Кнопка управления фильтацией'''
        else:
            start_label = ttk.Label(window, text="Недостаточно данных")
            start_label.grid(column=1, row=row - 1, sticky=tk.EW, padx=5, pady=5, columnspan=column + 3)

    def exer_list_creator(self, data):
        """Функция создания листа упражнений и исключения повторов"""
        exer_option_temp = []
        exer_option = []
        indexes = [0, ]
        for record in data:
            exer_option_temp.append(record['exercise'])
        for i in range(1, len(exer_option_temp)):
            index = 0
            for j in range(0, i):
                if exer_option_temp[i] == exer_option_temp[j]:
                    index += 1
            indexes.append(index)
        for i in range(0, len(indexes)):
            if indexes[i] == 0:
                exer_option.append(exer_option_temp[i])
        return (exer_option)

    def stat_window_creator(self, data, window):
        """Функция отображения статистики"""
        stat_window = Toplevel(window)
        stat_window.title("Окно статистики")
        '''Создание окна отображения'''
        stat_data = data
        '''Подготовка основных переменных'''
        exer_option = self.exer_list_creator(stat_data)
        '''Создания списка имен упражнений исключая повторы'''
        stat_info = []
        for exer in exer_option:
            stat_dic = {'exer_name':exer, 'average_weight':0, 'average_rep':0}
            weight = 0
            number = 0
            repetitions = 0
            for row in stat_data:
                if row['exercise'] == stat_dic['exer_name']:
                    weight += int(row['weight'])
                    number += 1
                    repetitions += int(row['repetitions'])
            stat_dic['average_weight'] = int(weight/number)
            stat_dic['average_rep'] = int(repetitions/number)
            stat_info.append(stat_dic)
        '''Создания пула данных статистики'''
        exercise_label = ttk.Label(stat_window, text="Название упражнения")
        exercise_label.grid(column=2, row=0, sticky=tk.EW, columnspan=1, pady=10)
        blank_label1 = ttk.Label(stat_window, text=" ")
        blank_label1.grid(column=3, row=0, sticky=tk.EW, columnspan=1, pady=10)
        average_weight_label = ttk.Label(stat_window, text="Средний вес")
        average_weight_label.grid(column=4, row=0, sticky=tk.EW, columnspan=1, pady=10)
        blank_label2 = ttk.Label(stat_window, text=" ")
        blank_label2.grid(column=5, row=0, sticky=tk.EW, columnspan=1, pady=10)
        average_rep_label = ttk.Label(stat_window, text="Среднее кол-во подходов")
        average_rep_label.grid(column=6, row=0, sticky=tk.EW, columnspan=1, pady=10)
        '''Создание заголовка таблицы статистики'''
        row_index = 1
        for i in range(0, len(stat_info)):
            exer_name_lable = ttk.Label(stat_window, text=f"{stat_info[i]['exer_name']}")
            exer_name_lable.grid(column=2, row=((i+1)*row_index), sticky=tk.EW, columnspan=2, pady=10)
            average_weight_lable = ttk.Label(stat_window, text=f"{stat_info[i]['average_weight']}")
            average_weight_lable.grid(column=4, row=((i+1) * row_index), sticky=tk.EW, columnspan=2, pady=10)
            average_rep_lable = ttk.Label(stat_window, text=f"{stat_info[i]['average_rep']}")
            average_rep_lable.grid(column=6, row=((i+1) * row_index), sticky=tk.EW, columnspan=2, pady=10)
        '''Отображение данных статистики'''

    def show_graf(self, date_info, window):
        """Функция отрисовки графика"""
        graf_window = Toplevel(window)
        graf_window.title("Графика статистики")
        data = date_info[0]# date type str
        control_exer = date_info[1]
        exer_list = date_info[2]
        for i in range(0, len(exer_list)):
            if exer_list[i] == '':
                exer_list.pop(i)#удаление пустого символа в списке упражнений
        exer_rep_data = []
        exer_date_data = []
        exer_weight_data = []
        for row in data:
            temp_date = self.date_control(row['date'])
            row['date'] = temp_date
        date_list_temp = []
        date_list = []
        indexes = [0, ]
        for record in data:
            date_list_temp.append(record['date'])
        for i in range(1, len(date_list_temp)):
            index = 0
            for j in range(0, i):
                if date_list_temp[i][0] == date_list_temp[j][0]:
                    index += 1
            indexes.append(index)
        for i in range(0, len(indexes)):
            if indexes[i] == 0:
                date_list.append(date_list_temp[i])
        '''Обработка дополнительных переменных'''

        if control_exer == '':
            for exer in exer_list:
                exer_weight_data.append(0)
                exer_rep_data.append(0)
            '''Подготовка длины списка данных'''
            for row in data:
                for i in range(0, len(exer_list)):
                    if row['exercise'] == exer_list[i]:
                        exer_rep_data[i] += int(row['repetitions'])
                        exer_weight_data[i] += int(row['weight'])
            '''Задание данных для графика при не указанном упражнение'''
            fig1 = Figure(figsize=(8, 6), dpi=100)
            weight_ax = fig1.add_subplot(111)
            weight_ax.plot(exer_list, exer_rep_data, marker='o', label='Кол-во повторов', color='blue')
            weight_ax.set_title(f"График повторов упражнениий за периуд")
            weight_ax.set_ylabel("Кол-во повторов")
            weight_ax.grid()
            graf_window.title("График повторов")
            graf_window.geometry("800x600")
            canvas1 = FigureCanvasTkAgg(fig1, master=graf_window)
            canvas1.draw()
            canvas1.get_tk_widget().pack(expand=True, fill=tk.BOTH)
            '''Отрисовка графика'''

        elif control_exer != '':
            for date in date_list:
                exer_date_data.append(date[0])
                exer_weight_data.append(0)
                exer_rep_data.append(0)
            '''Подготовка длины списка данных'''
            for row in data:
                for i in range(0, len(exer_date_data)):
                    if row['date'][0] == exer_date_data[i] and row['exercise'] == control_exer:
                        exer_rep_data[i] += int(row['repetitions'])
                        exer_weight_data[i] += int(row['weight'])
            for i in range(0, len(exer_date_data)):
                exer_date_data[i] = datetime.strptime(f'{exer_date_data[i][0]}-{exer_date_data[i][1]}'
                                                      f'-{exer_date_data[i][2]}', '%Y-%m-%d')
            '''Задание данных для графика при указанном упражнение'''
            fig1 = Figure(figsize=(8, 6), dpi=100)
            weight_ax = fig1.add_subplot(111)
            weight_ax.plot(exer_date_data, exer_rep_data, marker='o', label='Кол-во повторов', color='blue')
            weight_ax.set_title(f"График повторов упражнения <{control_exer}>")
            weight_ax.set_ylabel("Кол-во повторов")
            weight_ax.grid()
            graf_window.title("График повторов")
            graf_window.geometry("800x600")
            canvas1 = FigureCanvasTkAgg(fig1, master=graf_window)
            canvas1.draw()
            canvas1.get_tk_widget().pack(expand=True, fill=tk.BOTH)
            '''Отрисовка графика'''

    def window_creator(self, window, data):
        """Функция создания таблицы отоброжения записей"""
        tree = ttk.Treeview(self.main_window, columns=("Индекс", "Дата", "Упражнение", "Вес", "Повторения"),
                            show="headings")
        tree.column("Индекс", width=60, stretch=True)
        tree.heading('Индекс', text="Индекс")
        tree.heading('Дата', text="Дата")
        tree.heading('Упражнение', text="Упражнение")
        tree.heading('Вес', text="Вес")
        tree.heading('Повторения', text="Повторения")
        '''Настройка таблицы'''
        index = 1
        for entry in data:
            tree.insert('', tk.END, values=(index, entry['date'], entry['exercise'], entry['weight'],
                                            entry['repetitions']))
            index += 1
        '''Заполнение таблицы'''
        tree.pack(expand=True, fill=tk.BOTH)
        return (tree)

    def view_records(self, data=None):
        """Функция создания окна отображения <Днивнека занятий> """
        if data is None:
            data = load_data()
        '''Проверка на наличие входных данных'''
        self.main_window = Toplevel(self.root)
        self.main_window.title("Записи тренировок")
        '''Создание основы окна таблицы'''
        tree = self.window_creator(self.main_window, data)
        '''Создание таблицы'''
        def tree_row_choser():
            """Функция выбора позиции из списка"""
            try:
                selected_item = tree.selection()[0]  # Получаем выбранную строку
                values = tree.item(selected_item, "values")  # Считываем данные строки
                return (values)
            except IndexError:
                messagebox.showerror("Ошибка!", "Выберите запись для редактирования")
                return

        def run_edit_records():
            """Функция запуска процедуры изменения строки"""
            temp_edit_data = tree_row_choser()
            self.edit_record(temp_edit_data)

        def run_remove_records():
            """Функция запуска процедуры удаления строки"""
            temp_remove_data = tree_row_choser()
            self.remove_record(temp_remove_data)

        ttk.Button(self.main_window, text="Добавить", command=self.add_entry_window).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(self.main_window, text="Редактировать", command=run_edit_records).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(self.main_window, text="Удалить", command=run_remove_records).pack(side=tk.LEFT, padx=5, pady=5)
        if len(data) >= 5:
            ttk.Button(self.main_window, text="Фильтровать по дате",
                       command=self.filter_by_date_window).pack(side=tk.LEFT, padx=5, pady=5)
            ttk.Button(self.main_window, text="Фильтровать по упражнению",
                       command=self.filter_by_exer_window).pack(side=tk.LEFT, padx=5, pady=5)
        else:
            ttk.Button(self.main_window, text="Меньше 5 записей, мало данных для фильтра",
                       command=self.add_entry_window).pack(side=tk.LEFT, padx=5, pady=5)
        '''Описание кнопок управления'''

    def remove_record(self, data):
        """Функция удаления записи"""
        index = int(data[0])-1
        inner_data = load_data()
        remove_window = Toplevel(self.main_window)
        remove_window.geometry("400x150")
        remove_window.title("Окно удаления записи")
        '''Подготовка окна удаления'''
        def inner_delet():
            """Функция удаления записи"""
            inner_data.pop(index)
            save_data(inner_data)
            self.main_window.destroy()
            self.view_records()

        def inner_close():
            """Функция отмены удаления"""
            self.main_window.destroy()
            self.view_records()

        exercise_label = ttk.Label(remove_window, text="Дата:")
        exercise_label.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)
        exercise_label_quantity = ttk.Label(remove_window, text=f"{inner_data[index]['date']}")
        exercise_label_quantity.grid(column=2, row=1, sticky=tk.W, padx=5, pady=5, columnspan=6)
        '''Создание поля отображения даты выбранной записи'''
        exercise_label = ttk.Label(remove_window, text="Упражнение:")
        exercise_label.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)
        exercise_label_quantity = ttk.Label(remove_window, text=f"{inner_data[index]['exercise']}")
        exercise_label_quantity.grid(column=2, row=2, sticky=tk.W, padx=5, pady=5, columnspan=6)
        '''Создание поля отображения названия упражнения из выбранной записи'''
        weight_label = ttk.Label(remove_window, text="Вес:")
        weight_label.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)
        weight_label_quantity = ttk.Label(remove_window, text=f"{inner_data[index]['weight']}")
        weight_label_quantity.grid(column=2, row=3, sticky=tk.W, padx=5, pady=5, columnspan=6)
        '''Создание поля отображения веса из выбранной записи'''
        repetitions_label = ttk.Label(remove_window, text="Повторения:")
        repetitions_label.grid(column=1, row=4, sticky=tk.W, padx=5, pady=5)
        repetitions_label_quantity = ttk.Label(remove_window, text=f"{inner_data[index]['repetitions']}")
        repetitions_label_quantity.grid(column=2, row=4, sticky=tk.W, padx=5, pady=5, columnspan=6)
        '''Создание поля отображения колва повторов из выбранной записи'''
        ttk.Label(remove_window, text="Удалить запись?").grid(column=1, row=6, sticky=tk.W, padx=5, pady=5)
        ttk.Button(remove_window, text="Да", command=inner_delet).grid(column=2, row=6, sticky=tk.W, padx=5, pady=5)
        ttk.Button(remove_window, text="Нет", command=inner_close).grid(column=3, row=6, sticky=tk.W, padx=5, pady=5)
        '''Создание кнопок управления'''

    def edit_record(self, data):
        """Функция редаектирования записи"""
        index = int(data[0])
        date = self.date_control(data[1])
        exercise = data[2]
        weight = data[3]
        repetitions = data[4]
        '''Запись начальных данных из записи'''
        edit_window = Toplevel(self.main_window)
        edit_window.title("Редактирование записи")
        edit_window.geometry("275x200")
        '''Создание базового окна для отображения'''
        self.date_widgets_creator(edit_window, 1, 1, True, date)
        '''Создание поля отображения записи'''
        self.exercise_label = ttk.Label(edit_window, text="Упражнение:")
        self.exercise_label.grid(column=1, row=4, sticky=tk.W, padx=5, pady=5)
        self.exercise_entry = ttk.Entry(edit_window)
        self.exercise_entry.grid(column=2, row=4, sticky=tk.EW, padx=5, pady=5, columnspan=6)
        self.exercise_entry.insert(0, exercise)
        '''Создание поля изменения названия упразжнения'''
        self.weight_label = ttk.Label(edit_window, text="Вес:")
        self.weight_label.grid(column=1, row=5, sticky=tk.W, padx=5, pady=5)
        self.weight_entry = ttk.Entry(edit_window)
        self.weight_entry.grid(column=2, row=5, sticky=tk.EW, padx=5, pady=5, columnspan=6)
        self.weight_entry.insert(0, weight)
        '''Создание поля изменения веса'''
        self.repetitions_label = ttk.Label(edit_window, text="Повторения:")
        self.repetitions_label.grid(column=1, row=6, sticky=tk.W, padx=5, pady=5)
        self.repetitions_entry = ttk.Entry(edit_window)
        self.repetitions_entry.grid(column=2, row=6, sticky=tk.EW, padx=5, pady=5, columnspan=6)
        self.repetitions_entry.insert(0, repetitions)
        '''Создание поля изменения кол-ва подходов'''

        def save_new_data():
            """Функция сохранения измененных данных"""
            inner_data = load_data()
            inner_date = (f'{self.date_entry.get()} {self.hour_spin.get()}:'
                          f'{self.minute_spin.get()}:{self.second_spin.get()}')
            inner_exercise = self.exercise_entry.get()
            inner_weight = self.weight_entry.get()
            inner_repetitions = self.repetitions_entry.get()
            inner_data[index-1]['date'] = inner_date
            inner_data[index-1]['exercise'] = inner_exercise
            inner_data[index-1]['weight'] = inner_weight
            inner_data[index-1]['repetitions'] = inner_repetitions
            result_data = self.bubble_sort(inner_data)
            save_data(result_data)
            self.main_window.destroy()
            self.view_records()

        save_button = ttk.Button(edit_window, text="Сохранить", command=save_new_data)
        save_button.grid(column=1, row=8, sticky=tk.EW, padx=5, pady=5, columnspan=7)
        '''Описание кнопки сохранения'''

    def date_widgets_creator(self, window, column, row, use_date, date=[['2024', '12', '31'], '00', '00', '00']):
        """Функция создания поля отображения даты"""
        if not use_date:
            date = self.date_control(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        '''Проверка на наличие базовой даты'''
        self.date_entry_label = ttk.Label(window, text="число/месяц/год")
        self.date_entry_label.grid(column=column, row=row, sticky=tk.EW, padx=5, pady=5)
        self.date_entry = DateEntry(window, width=10, background='darkblue', foreground='white',
                                    borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(column=column, row=row + 1, sticky=tk.W, padx=5, pady=5)
        self.date_entry.set_date(f'{date[0][0]}-{date[0][1]}-{date[0][2]}')
        '''Создание поля отображения данных год-месяц-число'''
        self.hour_spin_label = ttk.Label(window, text="часы")
        self.hour_spin_label.grid(column=column + 1, row=row, sticky=tk.EW, padx=5, pady=5)
        self.hour_spin = ttk.Spinbox(window, from_=0, to=23, width=3, format="%02.0f", validate='key')
        self.hour_spin.grid(column=column + 1, row=row + 1, sticky=tk.EW, padx=5, pady=5)
        self.hour_spin.insert(0, date[1])
        '''Создание поля отображения часа'''
        self.minute_spin_label = ttk.Label(window, text="минуты")
        self.minute_spin_label.grid(column=column + 2, row=row, sticky=tk.EW, padx=5, pady=5)
        self.minute_spin = ttk.Spinbox(window, from_=0, to=59, width=3, format="%02.0f", validate='key')
        self.minute_spin.grid(column=column + 2, row=row + 1, sticky=tk.EW, padx=5, pady=5)
        self.minute_spin.insert(0, date[2])
        '''Создание поля отображения минуты'''
        self.second_spin_label = ttk.Label(window, text="секунды")
        self.second_spin_label.grid(column=column + 3, row=row, sticky=tk.EW, padx=5, pady=5)
        self.second_spin = ttk.Spinbox(window, from_=0, to=59, width=3, format="%02.0f", validate='key')
        self.second_spin.grid(column=column + 3, row=row + 1, sticky=tk.EW, padx=5, pady=5)
        self.second_spin.insert(0, date[3])
        '''Создание поля отображения секунды'''

    def filter_by_date_window(self):
        """Функция фильтрации записий по промежутку дат"""
        window = Toplevel(self.main_window)
        column = 1
        row = 1
        '''Создание основного окна'''
        start_label = ttk.Label(window, text="Дата начала фильтра:")
        start_label.grid(column=column, row=row - 1, sticky=tk.EW, padx=5, pady=5, columnspan=column + 3)
        date_start_entry_label = ttk.Label(window, text="число/месяц/год")
        date_start_entry_label.grid(column=column, row=row, sticky=tk.EW, padx=5, pady=5)
        date_start_entry = DateEntry(window, width=10, background='darkblue', foreground='white',
                                    borderwidth=2, date_pattern='yyyy-mm-dd')
        date_start_entry.grid(column=column, row=row + 1, sticky=tk.W, padx=5, pady=5)
        hour_start_spin_label = ttk.Label(window, text="часы")
        hour_start_spin_label.grid(column=column + 1, row=row, sticky=tk.EW, padx=5, pady=5)
        hour_start_spin = ttk.Spinbox(window, from_=0, to=23, width=3, format="%02.0f", validate='key')
        hour_start_spin.grid(column=column + 1, row=row + 1, sticky=tk.EW, padx=5, pady=5)
        minute_start_spin_label = ttk.Label(window, text="минуты")
        minute_start_spin_label.grid(column=column + 2, row=row, sticky=tk.EW, padx=5, pady=5)
        minute_start_spin = ttk.Spinbox(window, from_=0, to=59, width=3, format="%02.0f", validate='key')
        minute_start_spin.grid(column=column + 2, row=row + 1, sticky=tk.EW, padx=5, pady=5)
        second_start_spin_label = ttk.Label(window, text="секунды")
        second_start_spin_label.grid(column=column + 3, row=row, sticky=tk.EW, padx=5, pady=5)
        second_start_spin = ttk.Spinbox(window, from_=0, to=59, width=3, format="%02.0f", validate='key')
        second_start_spin.grid(column=column + 3, row=row + 1, sticky=tk.EW, padx=5, pady=5)
        '''Создание поля для указания начальной даты окна'''

        end_label = ttk.Label(window, text="Дата окончания фильтра:")
        end_label.grid(column=column, row=row+2, sticky=tk.EW, padx=5, pady=5, columnspan=column + 3)
        date_end_entry_label = ttk.Label(window, text="число/месяц/год")
        date_end_entry_label.grid(column=column, row=row + 3, sticky=tk.EW, padx=5, pady=5)
        date_end_entry = DateEntry(window, width=10, background='darkblue', foreground='white',
                                     borderwidth=2, date_pattern='yyyy-mm-dd')
        date_end_entry.grid(column=column, row=row + 4, sticky=tk.W, padx=5, pady=5)
        hour_end_spin_label = ttk.Label(window, text="часы")
        hour_end_spin_label.grid(column=column + 1, row=row + 3, sticky=tk.EW, padx=5, pady=5)
        hour_end_spin = ttk.Spinbox(window, from_=0, to=23, width=3, format="%02.0f", validate='key')
        hour_end_spin.grid(column=column + 1, row=row + 4, sticky=tk.EW, padx=5, pady=5)
        minute_end_spin_label = ttk.Label(window, text="минуты")
        minute_end_spin_label.grid(column=column + 2, row=row + 3, sticky=tk.EW, padx=5, pady=5)
        minute_end_spin = ttk.Spinbox(window, from_=0, to=59, width=3, format="%02.0f", validate='key')
        minute_end_spin.grid(column=column + 2, row=row + 4, sticky=tk.EW, padx=5, pady=5)
        second_end_spin_label = ttk.Label(window, text="секунды")
        second_end_spin_label.grid(column=column + 3, row=row + 3, sticky=tk.EW, padx=5, pady=5)
        second_end_spin = ttk.Spinbox(window, from_=0, to=59, width=3, format="%02.0f", validate='key')
        second_end_spin.grid(column=column + 3, row=row + 4, sticky=tk.EW, padx=5, pady=5)
        '''Создание поля для указания конечной даты окна'''

        def run_filter():
            """Функция запуска фильтрации"""
            try:
                start_date = datetime.strptime(f'{date_start_entry.get()} {hour_start_spin.get()}'
                                               f':{minute_start_spin.get()}:{second_start_spin.get()}',
                                               '%Y-%m-%d %H:%M:%S')
            except:
                messagebox.showerror("Ошибка", "Неверный формат даты начала фильтрации.")
                return
            try:
                end_date = datetime.strptime(f'{date_end_entry.get()} {hour_end_spin.get()}:'
                                             f'{minute_end_spin.get()}:{second_end_spin.get()}',
                                             '%Y-%m-%d %H:%M:%S')
            except:
                messagebox.showerror("Ошибка", "Неверный формат даты окончания фильтрации.")
                return
            '''Проверка корректности дат'''
            if start_date > end_date:
                temp_date = start_date
                start_date = end_date
                end_date = temp_date
            '''Упорядочевание указанных дат'''
            filter_info = ['date', start_date, end_date]
            result_data = self.data_filter(filter_info)
            '''Запуск фильтра'''
            self.main_window.destroy()
            self.view_records(result_data)
            '''Отображение результата'''

        filter_button = ttk.Button(window, text="Фильтровать", command=run_filter)
        filter_button.grid(column=column, row=row + 5, sticky=tk.EW, padx=5, pady=5, columnspan=column + 3)
        '''Кнопка управления фильтацией'''

    def filter_by_exer_window(self):
        """Функция настройки фильтра по названию упражнения"""
        data = load_data()
        '''Подготовка дополнительных переменных'''
        window = Toplevel(self.main_window)
        '''Создание окна для отображения'''
        exer_option = self.exer_list_creator(data)
        '''Создание списка доступных упражнений с исключением повторов'''
        def run_filter(choice):
            """Функция запуска фильтра"""
            control_exer = choice
            filter_info = ['exer', control_exer]
            result_data = self.data_filter(filter_info)
            '''Подготовка данных для фильтрации'''
            self.main_window.destroy()
            self.view_records(result_data)
            '''Отображение результата'''

        exer_label = ttk.Label(window, text="Выбирете упражнение для фильтра")
        exer_label.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5, columnspan=2)
        exer_selected = tk.StringVar(window)
        exer_menu = tk.OptionMenu(window, exer_selected, *exer_option, command=run_filter)
        exer_menu.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5, columnspan=2)
        '''Создание выпадающего списка для выбора упражнения'''

    def data_filter(self, filter_info):
        """Функция фильтра по указанным данным"""
        data = load_data()
        if filter_info[0] == 'date':
            '''Проведение фильтра по окну дат'''
            result_data = []
            for record in data:
                record_date = datetime.strptime(record['date'],'%Y-%m-%d %H:%M:%S')
                if filter_info[2] >= record_date >= filter_info[1]:
                    result_data.append(record)
            result_data = self.bubble_sort(result_data)
            return (result_data)
        elif filter_info[0] == 'exer':
            '''Проведение фильтра по названию упражениня'''
            result_data = []
            for record in data:
                record_exer = record['exercise']
                if record_exer == filter_info[1]:
                    result_data.append(record)
            result_data = self.bubble_sort(result_data)
            return (result_data)

    def date_control(self, data):
        """Функция преобразования формата даты"""
        data_separators = ['-', ' ', ':']
        data_separators_index = []
        index = 0
        '''Подготовка дополнительных переменных'''
        for simv in data:
            for separator in data_separators:
                if simv == separator:
                    data_separators_index.append(index)
            index += 1
        '''Поиск символов разделителей в записи даты'''
        result_data = [[' ', ' ', ' '], ' ', ' ', ' ']
        result_data[0][0] = data[:data_separators_index[0]]
        for i in range(1, len(data_separators_index)):
            if i < 3:
                result_data[0][i] = data[data_separators_index[i - 1] + 1:data_separators_index[i]]
            else:
                result_data[i-2] = data[data_separators_index[i - 1] + 1:data_separators_index[i]]
        result_data[len(result_data)-1] = data[data_separators_index[4] + 1:]
        '''апись даты в новом формате'''
        return (result_data)

def main():
    root = tk.Tk()
    app = TrainingLogApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()