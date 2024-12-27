import os
import numpy as np
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox

from GUI import CustomButton
from GUI import Input
from GUI import LabelTag
from GUI import TestItem
from diehardtest.DiehardBirthdaySpacings import DiehardBirthdaySpacings
# from DiehardBirthdaySpacings import DiehardBirthdaySpacings
from diehardtest.DiehardRuns import DiehardRuns
from diehardtest.DiehardOverlappingSums import DiehardOverlappingSums
from diehardtest.DiehardCraps import DiehardCraps

class Main(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master=master)
        self._master = master
        self.init_variables()
        self.init_window()

    def init_variables(self):
        self._test_type = [
            '01. Birthday Spacings Test',
            '02. Runs Test',
            '03. Overlapping Sums Test',
            '04. Craps Test'
        ]

        self._test_functions = {
            0: DiehardBirthdaySpacings.run_test,
            1: DiehardRuns.run_test,
            2: DiehardOverlappingSums.run_test,
            3: DiehardCraps.run_test,
        }

        self._test_results = []
        self._test_string = []

    def init_window(self):
        frame_title = "Diehard Randomness Test Suite"
        title_label = LabelTag(self.master, frame_title, 0, 5, 1260)

        input_label_frame = LabelFrame(self.master, text="Input Data")
        input_label_frame.config(font=("Calibri", 14))
        input_label_frame.place(x=20, y=30, width=1260, height=125)

        self.__binary_input = Input(input_label_frame, 'Binary Data', 10, 5)
        self.__binary_file_input = Input(input_label_frame, 'Binary Data File', 10, 35, True,
                                         self.select_binary_file, button_xcoor=1060, button_width=160)

        self._test_selection_label_frame = LabelFrame(self.master, text="Randomness Testing")
        self._test_selection_label_frame.config(font=("Calibri", 14))
        self._test_selection_label_frame.place(x=20, y=155, width=1260, height=400)


     

        self._tests = []

        for i, test_name in enumerate(self._test_type):
            y_offset = 35 + (i * 30)
            test_item = TestItem(self._test_selection_label_frame, test_name, 10, y_offset,
                                 p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
            self._tests.append(test_item)

        self._result_field = self._tests

        execute_button = CustomButton(self.master, 'Execute Test', 20, 615, 100, self.execute)
        save_button = CustomButton(self.master, 'Save Results', 125, 615, 100, self.save_results)
        reset_button = CustomButton(self.master, 'Reset', 230, 615, 100, self.reset)
        exit_button = CustomButton(self.master, 'Exit', 335, 615, 100, self.exit)

    def select_binary_file(self):
        self.__file_name = askopenfilename(initialdir=os.getcwd(), title="Select Binary Input File.")
        if self.__file_name:
            self.__binary_input.set_data("")
            self.__binary_file_input.set_data(self.__file_name)
            self.__is_binary_file = True

    def execute(self):
        if not self.__binary_input.get_data() and not self.__binary_file_input.get_data():
            messagebox.showwarning("Warning", "You must provide binary data or select a file.")
            return

        input_data = []
        if self.__binary_input.get_data():
            input_data.append(self.__binary_input.get_data())
        elif self.__binary_file_input.get_data():
            with open(self.__file_name, "r") as file:
                input_data.append(file.read())

        try:
            for data in input_data:
                results = [()]
                for idx, test_item in enumerate(self._tests):
                    if test_item.get_check_box_value() == 1:
                        test_func = self._test_functions[idx]
                        results.append(test_func(data))
                self._test_results.append(results)

            self.write_results(self._test_results[0])
            messagebox.showinfo("Execute", "Tests completed successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def write_results(self, results):
        for idx, result in enumerate(results):
            if result:
                self._result_field[idx].set_p_value(result[0])
                self._result_field[idx].set_result_value(result[1])

    def save_results(self):
        output_file = asksaveasfile(mode='w', defaultextension=".txt")
        if output_file:
            output_file.write("Diehard Test Results\n\n")
            for idx, result in enumerate(self._test_results[0]):
                output_file.write(f"{self._test_type[idx]}: P-Value = {result[0]}, Result = {result[1]}\n")
            output_file.close()
            messagebox.showinfo("Save", "Results saved successfully.")

    def reset(self):
        self.__binary_input.set_data("")
        self.__binary_file_input.set_data("")
        for test_item in self._tests:
            test_item.reset()
        self._test_results = []

    def exit(self):
        self._master.quit()


# if __name__ == '__main__':
#     np.seterr('raise')
#     root = Tk()
#     root.resizable(0, 0)
#     root.geometry("1300x650")
#     root.title("Diehard Randomness Test Suite")
#     app = Main(root)
#     app.mainloop()

def run_diehard_gui():
    """Launches the Diehard GUI."""
    np.seterr('raise')  # Make exceptions fatal
    root = Tk()
    root.resizable(0, 0)
    root.geometry("1300x650")
    root.title("Diehard Randomness Test Suite")
    app = Main(root)
    app.focus_displayof()
    root.mainloop()
