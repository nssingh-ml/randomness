import os
import numpy as np
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox
import tkinter as tkk

from TestU01.TestU01GUI import CustomButton, Input, LabelTag, TestItem
# from GUI import Input
# from GUI import LabelTag
# from GUI import TestItem
# from GUI import RandomExcursionTestItem
from Tools import Tools

from TestU01 import TestU01_Runs, TestU01AutoCorrelation, TestU01BirthdaySpacing, TestU01Collision, TestU01CouponCollector

from TestU01 import TestU01Gap, TestU01LinearComplexity, TestU01LoongestRun, TestU01MatrixRank, TestU01Serial, TestU01SimplePoker

class Main(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master=master)
        self._master = master
        self.init_variables()
        self.init_window()

    def init_variables(self):
        self._test_type = ['01. Runs',
                           '02. Auto-Correlation',
                           '03. Birthday Spacings',
                           '04. Collision ',
                           '05. Coupon Collector',
                           '06. Gap',
                           '07. Linear Complexity',
                           '08. Longest Run',
                           '09. Matrix Rank ',
                           '10. Serial',
                           '11. Simple Poker Test']

        self.__test_function = {
            0: TestU01_Runs.runs_test,
            1: TestU01AutoCorrelation.auto_correlation_test,
            2: TestU01BirthdaySpacing.birthday_spacing_test,
            3: TestU01Collision.collision_test,
            4: TestU01CouponCollector.coupon_collector_test,
            5: TestU01Gap.gap_test,
            6: TestU01LinearComplexity.linear_complexity_test,
            7: TestU01LoongestRun.longest_run_test,
            8: TestU01MatrixRank.matrix_rank_test,
            9: TestU01Serial.serial_test,
            10: TestU01SimplePoker.simp_poker_test
        }

        self._test_result = []
        self._test_string = []

    def init_window(self):
        frame_title = 'TestU01 Randomness Test Suite'
        title_label = LabelTag(self.master, frame_title, 0, 5, 1260)

        input_label_frame = LabelFrame(self.master, text="Input Data")
        input_label_frame.config(font=("Calibri", 14))
        input_label_frame.propagate(0)
        input_label_frame.place(x=20, y=30, width=1260, height=125)
        self.__binary_input = Input(input_label_frame, 'Binary Data', 10, 5)
        self.__binary_data_file_input = Input(input_label_frame, 'Binary Data File', 10, 35, True,
                                              self.select_binary_file, button_xcoor=1060, button_width=160)
        self.__string_data_file_input = Input(input_label_frame, 'String Data File', 10, 65, True,
                                              self.select_data_file, button_xcoor=1060, button_width=160)

        self._stest_selection_label_frame = LabelFrame(self.master, text="Randomness Testing", padx=5, pady=5)
        self._stest_selection_label_frame.config(font=("Calibri", 14))
        self._stest_selection_label_frame.place(x=20, y=155, width=1260, height=450)

        test_type_label_01 = LabelTag(self._stest_selection_label_frame, 'Test Type', 10, 5, 250, 11, border=2,
                                      relief="groove")
        p_value_label_01 = LabelTag(self._stest_selection_label_frame, 'P-Value', 265, 5, 235, 11, border=2,
                                     relief="groove")
        result_label_01 = LabelTag(self._stest_selection_label_frame, 'Result', 505, 5, 110, 11, border=2,
                                    relief="groove")

        self._test = []

        y_offset = 35
        for i, test in enumerate(self._test_type):
            test_item = TestItem(self._stest_selection_label_frame, test, 10, y_offset, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
            self._test.append(test_item)
            y_offset += 25

        select_all_button = CustomButton(self.master, 'Select All Test', 20, 615, 100, self.select_all)
        deselect_all_button = CustomButton(self.master, 'De-Select All Test', 125, 615, 150, self.deselect_all)
        execute_button = CustomButton(self.master, 'Execute Test', 280, 615, 100, self.execute)
        save_button = CustomButton(self.master, 'Save as Text File', 385, 615, 100, self.save_result_to_file)
        reset_button = CustomButton(self.master, 'Reset', 490, 615, 100, self.reset)
        exit = CustomButton(self.master, 'Exit Program', 595, 615, 100, self.exit)

    def select_binary_file(self):
        self.__file_name = askopenfilename(initialdir=os.getcwd(), title="Select Binary Input File.")
        if self.__file_name:
            self.__binary_input.set_data('')
            self.__binary_data_file_input.set_data(self.__file_name)
            self.__string_data_file_input.set_data('')

    def select_data_file(self):
        self.__file_name = askopenfilename(initialdir=os.getcwd(), title="Select Data File.")
        if self.__file_name:
            self.__binary_input.set_data('')
            self.__binary_data_file_input.set_data('')
            self.__string_data_file_input.set_data(self.__file_name)

    def select_all(self):
        for item in self._test:
            item.set_check_box_value(1)

    def deselect_all(self):
        for item in self._test:
            item.set_check_box_value(0)

    def execute(self):
        if len(self.__binary_input.get_data().strip()) == 0 and len(self.__binary_data_file_input.get_data().strip()) == 0 and len(self.__string_data_file_input.get_data().strip()) == 0:
            messagebox.showwarning("Warning", 'You must input the binary data or read the data from from the file.')
            return

        input = []

        if not len(self.__binary_input.get_data()) == 0:
            input.append(self.__binary_input.get_data())
        elif not len(self.__binary_data_file_input.get_data()) == 0:
            temp = []
            with open(self.__file_name) as handle:
                for data in handle:
                    temp.append(data.strip())
            input.append(''.join(temp))
        elif not len(self.__string_data_file_input.get_data()) == 0:
            temp = []
            with open(self.__file_name) as handle:
                for data in handle:
                    temp.append(Tools.string_to_binary(data.strip()))
            input.append(''.join(temp))

        try:
            for test_data in input:
                count = 0
                results = [() for _ in range(len(self._test_type))]
                for item in self._test:
                    if item.get_check_box_value() == 1:
                        results[count] = self.__test_function[count](test_data)
                    count += 1
                self._test_result.insert(0, results)

            self.write_results(self._test_result[0])
            messagebox.showinfo("Execute", "Test Complete.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def write_results(self, results):
        count = 0
        for result in results:
            if len(result) == 0:
                self._test[count].set_p_value('')
                self._test[count].set_result_value('')
            else:
                self._test[count].set_p_value(result[0])
                print(result)
                self._test[count].set_result_value(self.get_result_string(result[1]))
            count += 1

    def save_result_to_file(self):
        output_file = asksaveasfile(mode='w', defaultextension=".txt")
        if output_file:
            if len(self.__binary_input.get_data()) != 0:
                output_file.write('Test Data: ' + self.__binary_input.get_data() + '\n\n')
            elif len(self.__binary_data_file_input.get_data()) != 0:
                output_file.write('Test Data File: ' + self.__binary_data_file_input.get_data() + '\n\n')
            elif len(self.__string_data_file_input.get_data()) != 0:
                output_file.write('Test Data File: ' + self.__string_data_file_input.get_data() + '\n\n')

            result = self._test_result[0]
            output_file.write('%-50s\t%-20s\t%-10s\n' % ('Type of Test', 'P-Value', 'Conclusion'))
            self.write_result_to_file(output_file, result)
            output_file.close()
            messagebox.showinfo("Save", "File save finished. Check the output file for complete results.")

    def write_result_to_file(self, output_file, result):
        for count in range(len(self._test_type)):
            if self._test[count].get_check_box_value() == 1:
                output = '%-50s\t%-20s\t%s\n' % (
                    self._test_type[count], str(result[count][0]), self.get_result_string(result[count][1]))
                output_file.write(output)

    def reset(self):
        self.__binary_input.set_data('')
        self.__binary_data_file_input.set_data('')
        self.__string_data_file_input.set_data('')
        for item in self._test:
            item.reset()
        self._test_result = []

    def exit(self):
        exit(0)

    def get_result_string(self, result):
        return 'Random' if result=='Random' else 'Non-Random'

# if __name__ == '__main__':
#     np.seterr('raise')
#     root = Tk()
#     root.resizable(0, 0)
#     root.geometry("1300x650")
#     root.title('TestU01 Randomness Tester')
#     app = Main(root)
#     app.mainloop()

# def run_testu01_gui():
#     """Launches the NIST GUI."""
#     np.seterr('raise')  # Make exceptions fatal
#     root = Tk()
#     root.resizable(0, 0)
#     root.geometry("1300x650")
#     root.title("TestU01 Randomness Test Suite")
#     app = Main(root)
#     app.focus_displayof()
#     root.mainloop()

def run_testu01_gui(parent, on_close):
    """Launches the Diehard GUI."""
    def on_back():
        parent.destroy()
        on_close()

    np.seterr('raise')  # Make exceptions fatal
    testu01_window = tkk.Toplevel(parent)
    testu01_window.resizable(0, 0)
    testu01_window.geometry("1300x650")
    # root.title('Test Suite for NIST Random Numbers')

    testu01_window.wm_attributes("-topmost", 1)
    testu01_window.focus_force()

    exit = CustomButton(testu01_window, 'Back', 695, 615, 100, on_back)
    # back_button = tk.Button(root, text="Back to Main Menu", command=on_back)
    # back_button.pack(side=tk.BOTTOM, pady=10)

    # Ensure the Toplevel window behaves like a modal dialog
    # testu01_window.transient(parent)
    # testu01_window.grab_set()
    # parent.wait_window(testu01_window)
    app = Main(testu01_window)
    # app.focus_displayof()
    testu01_window.mainloop()

# run_testu01_gui()































# import os
# import numpy as np
# from tkinter import *
# from tkinter.filedialog import askopenfilename
# from tkinter.filedialog import asksaveasfile
# from tkinter import messagebox

# from TestU01.TestU01GUI import CustomButton, Input, LabelTag, TestItem


# class Main(Frame):
#     def __init__(self, master=None):
#         Frame.__init__(self, master=master)
#         self._master = master
#         self.init_variables()
#         self.init_window()

#     def init_variables(self):
#         self._test_type = [
#             "01. Small Crush Test",
#             "02. Crush Test",
#             "03. Big Crush Test"
#         ]

#         self._test_functions = {
#             0: self.small_crush_test,
#             1: self.crush_test,
#             2: self.big_crush_test,
#         }

#         self._test_results = []

#     def init_window(self):
#         frame_title = "TestU01 Randomness Test Suite"
#         title_label = LabelTag(self.master, frame_title, 0, 5, 1260)

#         input_label_frame = LabelFrame(self.master, text="Input Data")
#         input_label_frame.config(font=("Calibri", 14))
#         input_label_frame.place(x=20, y=30, width=1260, height=150)

#         # Binary Data Input
#         self.__binary_input = Input(input_label_frame, "Binary Data", 10, 5)
#         self.__binary_file_input = Input(
#             input_label_frame, "Binary Data File", 10, 35, has_button=True, action=self.select_binary_file
#         )

#         # String Data Input
#         # self.__string_data_input = Input(input_label_frame, "String Data", 10, 65)
#         self.__string_file_input = Input(
#             input_label_frame, "String Data File", 10, 65, has_button=True, action=self.select_string_file
#         )

#         self._test_selection_label_frame = LabelFrame(self.master, text="Randomness Testing")
#         self._test_selection_label_frame.config(font=("Calibri", 14))
#         self._test_selection_label_frame.place(x=20, y=185, width=1260, height=400)

#         self._tests = []

#         for i, test_name in enumerate(self._test_type):
#             y_offset = 35 + (i * 30)
#             test_item = TestItem(self._test_selection_label_frame, test_name, 10, y_offset)
#             self._tests.append(test_item)

#         self._result_field = self._tests

#         execute_button = CustomButton(self.master, "Execute Test", 20, 615, 100, self.execute)
#         save_button = CustomButton(self.master, "Save Results", 125, 615, 100, self.save_results)
#         reset_button = CustomButton(self.master, "Reset", 230, 615, 100, self.reset)
#         exit_button = CustomButton(self.master, "Exit", 335, 615, 100, self.exit)

#     def select_binary_file(self):
#         self.__file_name = askopenfilename(initialdir=os.getcwd(), title="Select Binary Input File.")
#         if self.__file_name:
#             self.__binary_input.set_data("")
#             self.__binary_file_input.set_data(self.__file_name)

#     def select_string_file(self):
#         self.__file_name = askopenfilename(initialdir=os.getcwd(), title="Select String Input File.")
#         if self.__file_name:
#             self.__string_data_input.set_data("")
#             self.__string_file_input.set_data(self.__file_name)

#     def execute(self):
#         if not self.__binary_input.get_data() and not self.__binary_file_input.get_data() and not self.__string_data_input.get_data() and not self.__string_file_input.get_data():
#             messagebox.showwarning("Warning", "You must provide binary or string data or select a file.")
#             return

#         input_data = []
#         if self.__binary_input.get_data():
#             input_data.append(self.__binary_input.get_data())
#         elif self.__binary_file_input.get_data():
#             with open(self.__file_name, "r") as file:
#                 input_data.append(file.read())
#         elif self.__string_data_input.get_data():
#             input_data.append(self.__string_data_input.get_data())
#         elif self.__string_file_input.get_data():
#             with open(self.__file_name, "r") as file:
#                 input_data.append(file.read())

#         try:
#             for data in input_data:
#                 results = [()]
#                 for idx, test_item in enumerate(self._tests):
#                     if test_item.get_check_box_value() == 1:
#                         test_func = self._test_functions[idx]
#                         results.append(test_func(data))
#                 self._test_results.append(results)

#             self.write_results(self._test_results[0])
#             messagebox.showinfo("Execute", "Tests completed successfully.")
#         except Exception as e:
#             messagebox.showerror("Error", str(e))

#     def write_results(self, results):
#         for idx, result in enumerate(results):
#             if result:
#                 self._result_field[idx].set_p_value(result[0])
#                 self._result_field[idx].set_result_value(result[1])

#     def save_results(self):
#         output_file = asksaveasfile(mode="w", defaultextension=".txt")
#         if output_file:
#             output_file.write("TestU01 Results\n\n")
#             for idx, result in enumerate(self._test_results[0]):
#                 output_file.write(f"{self._test_type[idx]}: P-Value = {result[0]}, Result = {result[1]}\n")
#             output_file.close()
#             messagebox.showinfo("Save", "Results saved successfully.")

#     def reset(self):
#         self.__binary_input.set_data("")
#         self.__binary_file_input.set_data("")
#         self.__string_data_input.set_data("")
#         self.__string_file_input.set_data("")
#         for test_item in self._tests:
#             test_item.reset()
#         self._test_results = []

#     def exit(self):
#         self._master.quit()

#     # Placeholder methods for the TestU01 tests
#     def small_crush_test(self, data):
#         # Implement Small Crush Test logic here
#         return 0.99, "Random"

#     def crush_test(self, data):
#         # Implement Crush Test logic here
#         return 0.01, "Non-Random"

#     def big_crush_test(self, data):
#         # Implement Big Crush Test logic here
#         return 0.50, "Random"


# # if __name__ == "__main__":
# #     np.seterr("raise")
# #     root = Tk()
# #     root.resizable(0, 0)
# #     root.geometry("1300x700")
# #     root.title("TestU01 Randomness Test Suite")
# #     app = Main(root)
# #     app.mainloop()

# def run_testu01_gui():
#     """Launches the NIST GUI."""
#     np.seterr('raise')  # Make exceptions fatal
#     root = Tk()
#     root.resizable(0, 0)
#     root.geometry("1300x650")
#     root.title("TestU01 Randomness Test Suite")
#     app = Main(root)
#     app.focus_displayof()
#     root.mainloop()

