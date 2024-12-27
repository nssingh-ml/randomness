from tkinter import Button, Checkbutton, DISABLED, Entry, IntVar, Label, StringVar


class CustomButton:
    def __init__(self, master, title, x_coor, y_coor, width, action=None):
        button = Button(master, text=title, command=action)
        button.config(font=("Calibri", 10))
        button.place(x=x_coor, y=y_coor, width=width, height=25)


class Input:
    def __init__(self, master, title, x_coor, y_coor, has_button=False, action=None, state="disabled", button_xcoor=1050, button_width=180):
        label = Label(master, text=title)
        label.config(font=("Calibri", 12))
        label.place(x=x_coor, y=y_coor, height=25)

        self.__data = StringVar()
        self.__data_entry = Entry(master, textvariable=self.__data)
        self.__data_entry.place(x=150, y=y_coor, width=900, height=25)

        if has_button:
            self.__data_entry.config(state=state)
            button = Button(master, text=f"Select {title}", command=action)
            button.config(font=("Calibri", 10))
            button.place(x=button_xcoor, y=y_coor, width=button_width, height=25)

    def set_data(self, value):
        self.__data.set(value)

    def get_data(self):
        return self.__data.get()

    def change_state(self, state):
        self.__data_entry.config(state=state)


class LabelTag:
    def __init__(self, master, title, x_coor, y_coor, width, font_size=18, border=0, relief='flat'):
        label = Label(master, text=title, borderwidth=border, relief=relief)
        label.config(font=("Calibri", font_size))
        label.place(x=x_coor, y=y_coor, width=width, height=25)


class TestItem:
    def __init__(self, master, title, x_coor, y_coor, p_value_x_coor=365, p_value_width=500, result_x_coor=870, result_width=350, font_size=12):
        self.__chb_var = IntVar()
        self.__p_value = StringVar()
        self.__result = StringVar()

        checkbox = Checkbutton(master, text=title, variable=self.__chb_var)
        checkbox.config(font=("Calibri", font_size))
        checkbox.place(x=x_coor, y=y_coor)

        p_value_entry = Entry(master, textvariable=self.__p_value)
        p_value_entry.config(state=DISABLED)
        p_value_entry.place(x=p_value_x_coor, y=y_coor, width=p_value_width, height=25)

        result_entry = Entry(master, textvariable=self.__result)
        result_entry.config(state=DISABLED)
        result_entry.place(x=result_x_coor, y=y_coor, width=result_width, height=25)

    def get_check_box_value(self):
        return self.__chb_var.get()

    def set_check_box_value(self, value):
        self.__chb_var.set(value)

    def set_p_value(self, value):
        self.__p_value.set(value)

    def set_result_value(self, value):
        self.__result.set(value)

    def reset(self):
        self.set_check_box_value(0)
        self.set_p_value("")
        self.set_result_value("")
