"""Vision layer."""
import tkinter as tk
import tkinter.ttk as ttk
import typing
from app import constants
from app.controller import Controller


class View(tk.Tk):
    """
    View layer.
    Load all widgets to create a graphical interface.
    """
    def __init__(self) -> None:
        super().__init__()
        self.controller = Controller(view=self)

        self.screens_container = ttk.Frame(master=self)
        self.screens_container.pack(side='top', fill='both', expand=True)
        self.registers_screen = RegistersScreen(master=self.screens_container)
        self.show_registers_screen()
        self.form_display()
        self.apply_style()

        self.form_submit_button.configure(command=self.form_submit)
        self.form_display_button.configure(command=self.form_display)
        self.form_update_button.configure(command=self.form_update)
        self.form_delete_button.configure(command=self.form_delete)
        self.registers_treeview.bind(
            '<<TreeviewSelect>>', lambda e: self.fill_form()
        )

    def apply_style(self) -> None:
        def travel(widget: tk.Misc, font: str) -> None:
            """little trick to change all entry directly."""
            if isinstance(widget, ttk.Entry):
                widget.configure(font=font)
            for children in widget.winfo_children():
                travel(children, font)

        theme = 'clam'
        default_font = 'Arial 16 normal'
        label_font = 'Consolas 16 normal'
        entry_font = 'Georgia 16 normal'
        button_font = 'Consolas 14 bold'
        arrowsize = 30
        rowheight = 40

        style = ttk.Style()
        style.theme_use(theme)
        style.configure('.', font=default_font)
        style.configure('.', background='#fff')
        style.configure('Treeview', rowheight=rowheight)
        style.configure('Treeview.Heading', font=label_font)
        style.configure('TCombobox', arrowsize=arrowsize)
        self.option_add('*TCombobox*Listbox*Font', entry_font)
        style.configure('Vertical.TScrollbar', arrowsize=arrowsize)
        style.configure('TLabel', font=label_font)
        style.configure('TLabelframe.Label', font=label_font)
        style.configure('TButton', font=button_font)
        style.configure('TRadiobutton', font=entry_font)
        travel(self, entry_font)

    def show_registers_screen(self) -> None:
        for children in self.screens_container.winfo_children():
            children.pack_forget()
        self.title('Registers')
        self.geometry('1400x700+0+0')
        self.registers_screen.pack(side='top', fill='both', expand=True)

    def form_submit(self) -> None:
        form = self.registers_screen.form
        name = form.name()
        email = form.email()
        sex = form.sex()
        branch = form.branch()
        programming = form.programming()
        self.controller.insert_student(name, email, sex, branch, programming)

    def form_display(self) -> None:
        table = self.registers_screen.table
        students = self.controller.select_students()
        table.set_rows(students)

    def form_update(self) -> None:
        table = self.registers_screen.table
        form = self.registers_screen.form
        name = form.name()
        email = form.email()
        sex = form.sex()
        programming = form.programming()
        branch = form.branch()
        primary_key = None

        selection = table.selection()
        if selection:
            primary_key = selection[0]
        self.controller.update_student(
            primary_key, name, email, sex, branch, programming
        )

    def form_delete(self) -> None:
        table = self.registers_screen.table
        selection = table.selection()
        primary_key = None
        if selection:
            primary_key = selection[0]
        self.controller.delete_student(primary_key)

    def clear_form_fields(self) -> None:
        form = self.registers_screen.form
        form.name_input.set_text('')
        form.email_input.set_text('')

    def clear_form_feedback(self) -> None:
        form = self.registers_screen.form
        form.name_input.set_feedback('')
        form.email_input.set_feedback('')

    def show_form_feedback(self, field: str, message: str) -> None:
        form = self.registers_screen.form
        fields: typing.Dict[str, TextInput] = dict()
        fields['name'] = form.name_input
        fields['email'] = form.email_input
        if field in fields.keys():
            fields[field].set_feedback(message)

    def showinfo(self, title: str, message: str) -> None:
        InfoMessage(master=self, title=title, message=message)

    def showwarning(self, title: str, message: str) -> None:
        WarningMessage(master=self, title=title, message=message)

    def fill_form(self) -> None:
        form = self.registers_screen.form
        table = self.registers_screen.table
        selection = table.selection()

        if selection:
            primary_key = selection[0]
            student = self.controller.select_student_by_primary_key(
                primary_key
            )
            name = student[1]
            email = student[2]
            sex = student[3]
            branch = student[4]
            programming = student[5]
            form.set_name(name)
            form.set_email(email)
            form.set_sex(sex)
            form.set_branch(branch)
            form.set_programming(programming)

    @property
    def form_submit_button(self) -> ttk.Button:
        return self.registers_screen.form.submit_button

    @property
    def form_display_button(self) -> ttk.Button:
        return self.registers_screen.form.display_button

    @property
    def form_update_button(self) -> ttk.Button:
        return self.registers_screen.form.update_button

    @property
    def form_delete_button(self) -> ttk.Button:
        return self.registers_screen.form.delete_button

    @property
    def registers_treeview(self) -> ttk.Treeview:
        return self.registers_screen.table.treeview


class RegistersScreen(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        paned = ttk.Panedwindow(master=self, orient='horizontal')
        paned.pack(side='top', fill='both', expand=True)

        self.computing_img = tk.PhotoImage(file=constants.COMPUTING_IMG)
        self.form = Form(master=paned, padding=15)
        self.form.header.configure(image=self.computing_img)
        paned.add(self.form, weight=1)

        columns = ['id', 'name', 'email', 'sex', 'branch', 'programming']
        self.database_img = tk.PhotoImage(file=constants.DATABASE_IMG)
        self.table = Table(master=paned, padding=15)
        self.table.header.configure(image=self.database_img)
        self.table.set_columns(columns)
        paned.add(self.table, weight=2)


class Form(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid_propagate(False)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)

        self.header = ttk.Label(master=self)
        self.header.configure(anchor='center')
        self.header.grid(row=0, column=0, columnspan=2, sticky='ns')

        self.name_input = TextInput(master=self)
        self.name_input.label.configure(text='Full name')
        self.name_input.grid(row=1, column=0, columnspan=2, sticky='nsew')

        self.email_input = TextInput(master=self)
        self.email_input.label.configure(text='Email')
        self.email_input.grid(row=2, column=0, columnspan=2, sticky='nsew')

        sexes = ['male', 'female']
        self.sex_input = RadioInput(master=self)
        self.sex_input.configure(text='Sex')
        self.sex_input.set_values(sexes)
        self.sex_input.grid(row=3, column=0, columnspan=2, sticky='nsew')

        languages = ['python', 'java', 'c']
        self.programming_input = RadioInput(master=self)
        self.programming_input.configure(text='Programming')
        self.programming_input.set_values(languages)
        self.programming_input.grid(
            row=4, column=0, columnspan=2, sticky='nsew'
        )

        branches = ['CSE', 'MECH', 'ENTC', 'CIVIL']
        self.branch_input = ComboboxInput(master=self)
        self.branch_input.set_values(branches)
        self.branch_input.label.configure(text='Branch')
        self.branch_input.grid(row=5, column=0, columnspan=2, sticky='nsew')

        self.submit_button = ttk.Button(master=self, text='Submit')
        self.submit_button.grid(row=6, column=0, sticky='nsew')

        self.display_button = ttk.Button(master=self, text='Display')
        self.display_button.grid(row=6, column=1, sticky='nsew')

        self.update_button = ttk.Button(master=self, text='Update')
        self.update_button.grid(row=7, column=0, sticky='nsew')

        self.delete_button = ttk.Button(master=self, text='Delete')
        self.delete_button.grid(row=7, column=1, sticky='nsew')

    def name(self) -> str:
        return self.name_input.text()

    def set_name(self, name: str) -> None:
        self.name_input.set_text(name)

    def email(self) -> str:
        return self.email_input.text()

    def set_email(self, email: str) -> None:
        self.email_input.set_text(email)

    def sex(self) -> str:
        return self.sex_input.selection()

    def set_sex(self, sex: str) -> None:
        self.sex_input.set_selection(sex)

    def programming(self) -> str:
        return self.programming_input.selection()

    def set_programming(self, programming: str) -> None:
        self.programming_input.set_selection(programming)

    def branch(self) -> str:
        return self.branch_input.selection()

    def set_branch(self, branch: str) -> None:
        self.branch_input.set_selection(branch)


class Table(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.pack_propagate(False)

        self.header = ttk.Label(master=self, anchor='center')
        self.header.pack(side='top', fill='x')

        self.treeview = ttk.Treeview(master=self, show='headings')
        self.treeview.pack(side='left', fill='both', expand=True)

        self.scrollbar = ttk.Scrollbar(master=self)
        self.scrollbar.pack(side='left', fill='y')

        self.scrollbar.configure(command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.scrollbar.set)

    def set_columns(self, columns: typing.List[str]) -> None:
        self.treeview.configure(columns=columns)
        for column in columns:
            self.treeview.heading(column, text=column)
            self.treeview.column(column, width=1, stretch=True)

    def set_rows(self, rows: typing.List[typing.Tuple]) -> None:
        self.treeview.delete(*self.treeview.get_children())
        for row in rows:
            self.treeview.insert('', 'end', values=row)

    def selection(self) -> typing.Optional[typing.Tuple]:
        selections = self.treeview.selection()
        if selections:
            return tuple(self.treeview.item(selections[0])['values'])

        return None


class TextInput(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.label = ttk.Label(master=self)
        self.label.configure(anchor='center')
        self.label.pack(side='top', fill='x')

        self.entry = ttk.Entry(master=self)
        self.entry.configure(justify='center')
        self.entry.pack(side='top', fill='x')

        self.feedback = ttk.Label(master=self)
        self.feedback.configure(anchor='center')
        self.feedback.configure(foreground='red')
        self.feedback.pack(side='top', fill='x')

    def text(self) -> str:
        return self.entry.get().strip()

    def set_text(self, text: str) -> None:
        self.entry.delete(0, 'end')
        self.entry.insert('end', text)

    def set_feedback(self, feedback: str) -> None:
        self.feedback.configure(text=feedback)


class RadioInput(ttk.Labelframe):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.configure(labelanchor='n')
        self.radio_var = tk.StringVar()

    def set_values(self, values: typing.List[str]) -> None:
        for children in self.winfo_children():
            children.destroy()

        for value in values:
            radio = ttk.Radiobutton(master=self)
            radio.configure(text=value)
            radio.configure(value=value)
            radio.configure(variable=self.radio_var)
            radio.pack(side='left', expand=True)

        self.radio_var.set(values[0])

    def selection(self) -> str:
        return self.radio_var.get()

    def set_selection(self, selection: str) -> None:
        self.radio_var.set(selection)


class ComboboxInput(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.label = ttk.Label(master=self)
        self.label.configure(anchor='center')
        self.label.pack(side='top', fill='x')

        self.combobox_var = tk.StringVar()
        self.combobox = ttk.Combobox(master=self)
        self.combobox.configure(textvariable=self.combobox_var)
        self.combobox.pack(side='top', fill='x')

    def set_values(self, values: typing.List[str]) -> None:
        self.combobox_var.set(values[0])
        self.combobox.configure(values=values)

    def selection(self) -> str:
        return self.combobox_var.get()

    def set_selection(self, selection: str) -> None:
        self.combobox_var.set(selection)


class InfoMessage(tk.Toplevel):
    def __init__(self, master: tk.Misc, message: str, title: str = '') -> None:
        super().__init__(master)
        self.title(title)
        self.resizable(False, False)
        self.bind('<Key>', lambda event: self.destroy())

        self.label = ttk.Label(master=self)
        self.label.configure(anchor='center')
        self.label.configure(text=message)
        self.label.pack(side='top', fill='x')


class WarningMessage(InfoMessage):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.label.configure(foreground='red')
