import sqlite3

from imports import *


def get_data():
    db = DBConnection()
    data = db.select_items()
    del db
    print(data)
    return data


def find(key):
    # проверка слова
    # устновка progressbar
    # парсинг данных
    parse(key)
    ResultTable()


class Ui:
    def __init__(self, master):
        self.master = master
        master.title("Pharmacy desktop")
        master.iconphoto(True, tk.PhotoImage(file='../third_party/cross.png'))
        mainmenu = tk.Menu(master)
        master.config(menu=mainmenu)
        mainmenu.add_command(label='Помощь', command=Help)
        mainmenu.add_command(label='О программе', command=About)
        mainmenu.add_command(label='Контакты', command=Contact)

        self.label = tk.Label(master, text="Поиск товаров")
        self.label.place(relx=.5, rely=.1, anchor="c", width=100, height=20)

        self.message = tk.StringVar()
        self.entry_row = tk.Entry(textvariable=self.message)
        self.entry_row.place(relx=.5, rely=.18, anchor="c", width=100, height=20)

        self.find_button = tk.Button(master, text="Найти", command=self.get_message)
        self.find_button.place(relx=.92, rely=.92, anchor="c", width=75, height=40)

    def get_message(self):
        message = self.message.get()
        find(message)


class Help(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title('Помощь')
        self.geometry('400x300')
        self.label = tk.Label(self, text='Помощь: \nПрограмма осуществляет сбор данных с онлайн \nмагазинов аптек по введенной ключевой фразе. \n\nВ поле ввода вводим ключевое слово->\nНажимае кнопку "Найти"->\nОжидаем результата выполнения программы->\nАнализируем сформированные данные таблицы.\n\nСбор данных занимает некоторое время. После сбора \nданных, результат отобразится на появившемся окне в таблице.')
        self.label.place(relx=.5, rely=.45, anchor="c", width=370, height=200)


class Contact(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title('Контакты')
        self.geometry('400x200')
        self.label = tk.Label(self, text='Контакты: \nEmail: krivenkov.vladimir.1973@mail.ru')
        self.label.place(relx=.5, rely=.4, anchor="c", width=300, height=50)


class About(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.geometry('500x200')
        self.title('О программе')
        self.label = tk.Label(self, text='Pharmacy desktop v1.0 \nGithub updates: \nhttps://github.com/VladimirKov-pr/Pharmacy_desktop.git')
        self.label.place(relx=.5, rely=.4, anchor="c", width=700, height=50)


class ResultTable(tk.Toplevel, Ui):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title('Результат')
        self.columns = ('#1', '#2', '#3')
        self.tree = ttk.Treeview(self, show="headings", columns=self.columns)
        self.tree.heading("#1", text="Ссылка")
        self.tree.heading("#2", text="Описание")
        self.tree.heading("#3", text="Цена")
        ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)
        data = get_data()
        for row in data:
            self.tree.insert("", tk.END, values=row)
        self.tree.grid(row=0, column=0)
        ysb.grid(row=0, column=1, sticky=tk.N + tk.S)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.target_tree = None

    def show_row(self):
        self.target_tree = None
        self.target_tree = ttk.Treeview(self, show="headings", columns=self.columns)
        self.target_tree.heading("#1", text="Ссылка")
        self.target_tree.heading("#2", text="Описание")
        self.target_tree.heading("#3", text="Цена")
        self.target_tree.grid(row=0, column=0)

        # вывод выбранной строки


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x300")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    my_gui = Ui(root)
    root.mainloop()
