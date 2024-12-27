import os
import numpy as np
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox

from TestU01.TestU01GUI import CustomButton, Input, LabelTag, TestItem


class Main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=master)
        self._master = master
        self.init_variables()
        self.init_window()

    def init_variables(self):
        self._test_type = [
            "01. Small Crush Test",
            "02. Crush Test",
            "03. Big Crush Test"
        ]

        self._test_functions = {
            0: self.small_crush_test,
            1: self.crush_test,
            2: self.big_crush_test,
        }

        self._test_results = []

    def init_window(self):
        frame_title = "TestU01 Randomness Test Suite"
        title_label = LabelTag(self.master, frame_title, 0, 5, 1260)

        input_label_frame = LabelFrame(self.master, text="Input Data")
        input_label_frame.config(font=("Calibri", 14))
        input_label_frame.place(x=20, y=30, width=1260, height=150)

        # Binary Data Input
        self.__binary_input = Input(input_label_frame, "Binary Data", 10, 5)
        self.__binary_file_input = Input(
            input_label_frame, "Binary Data File", 10, 35, has_button=True, action=self.select_binary_file
        )

        # String Data Input
        # self.__string_data_input = Input(input_label_frame, "String Data", 10, 65)
        self.__string_file_input = Input(
            input_label_frame, "String Data File", 10, 65, has_button=True, action=self.select_string_file
        )

        self._test_selection_label_frame = LabelFrame(self.master, text="Randomness Testing")
        self._test_selection_label_frame.config(font=("Calibri", 14))
        self._test_selection_label_frame.place(x=20, y=185, width=1260, height=400)

        self._tests = []

        for i, test_name in enumerate(self._test_type):
            y_offset = 35 + (i * 30)
            test_item = TestItem(self._test_selection_label_frame, test_name, 10, y_offset)
            self._tests.append(test_item)

        self._result_field = self._tests

        execute_button = CustomButton(self.master, "Execute Test", 20, 615, 100, self.execute)
        save_button = CustomButton(self.master, "Save Results", 125, 615, 100, self.save_results)
        reset_button = CustomButton(self.master, "Reset", 230, 615, 100, self.reset)
        exit_button = CustomButton(self.master, "Exit", 335, 615, 100, self.exit)

    def select_binary_file(self):
        self.__file_name = askopenfilename(initialdir=os.getcwd(), title="Select Binary Input File.")
        if self.__file_name:
            self.__binary_input.set_data("")
            self.__binary_file_input.set_data(self.__file_name)

    def select_string_file(self):
        self.__file_name = askopenfilename(initialdir=os.getcwd(), title="Select String Input File.")
        if self.__file_name:
            self.__string_data_input.set_data("")
            self.__string_file_input.set_data(self.__file_name)

    def execute(self):
        if not self.__binary_input.get_data() and not self.__binary_file_input.get_data() and not self.__string_data_input.get_data() and not self.__string_file_input.get_data():
            messagebox.showwarning("Warning", "You must provide binary or string data or select a file.")
            return

        input_data = []
        if self.__binary_input.get_data():
            input_data.append(self.__binary_input.get_data())
        elif self.__binary_file_input.get_data():
            with open(self.__file_name, "r") as file:
                input_data.append(file.read())
        elif self.__string_data_input.get_data():
            input_data.append(self.__string_data_input.get_data())
        elif self.__string_file_input.get_data():
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
        output_file = asksaveasfile(mode="w", defaultextension=".txt")
        if output_file:
            output_file.write("TestU01 Results\n\n")
            for idx, result in enumerate(self._test_results[0]):
                output_file.write(f"{self._test_type[idx]}: P-Value = {result[0]}, Result = {result[1]}\n")
            output_file.close()
            messagebox.showinfo("Save", "Results saved successfully.")

    def reset(self):
        self.__binary_input.set_data("")
        self.__binary_file_input.set_data("")
        self.__string_data_input.set_data("")
        self.__string_file_input.set_data("")
        for test_item in self._tests:
            test_item.reset()
        self._test_results = []

    def exit(self):
        self._master.quit()

    # Placeholder methods for the TestU01 tests
    def small_crush_test(self, data):
        # Implement Small Crush Test logic here
        return 0.99, "Random"

    def crush_test(self, data):
        # Implement Crush Test logic here
        return 0.01, "Non-Random"

    def big_crush_test(self, data):
        # Implement Big Crush Test logic here
        return 0.50, "Random"


# if __name__ == "__main__":
#     np.seterr("raise")
#     root = Tk()
#     root.resizable(0, 0)
#     root.geometry("1300x700")
#     root.title("TestU01 Randomness Test Suite")
#     app = Main(root)
#     app.mainloop()

def run_testu01_gui():
    """Launches the NIST GUI."""
    np.seterr('raise')  # Make exceptions fatal
    root = Tk()
    root.resizable(0, 0)
    root.geometry("1300x650")
    root.title("TestU01 Randomness Test Suite")
    app = Main(root)
    app.focus_displayof()
    root.mainloop()
run_testu01_gui()

