import os
import numpy as np
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter import messagebox

from GUI import CustomButton, Input, LabelTag, TestItem
from diehardtest.DiehardBirthdaySpacings import DiehardBirthdaySpacings
from diehardtest.DiehardOperm5 import DiehardOPERM5
from diehardtest.DiehardBinaryRank32x32 import Diehard32x32BinaryRank
from diehardtest.DiehardBinaryRank6x8 import Diehard6x8BinaryRank
from diehardtest.DiehardBitstream import DiehardBitstream
from diehardtest.DiehardOPSO import  DiehardOPSOTest
from diehardtest.DiehardOQSO import DiehardOQSOTest
from diehardtest.DiehardDNA import DiehardDNATest
from diehardtest.DiehardCount1Stream import DiehardCountOnes
from diehardtest.DiehardCount1Byte import DiehardCountOnesByte
from diehardtest.DiehardParkingLot import DiehardParkingLotTest
from diehardtest.DiehardMinimumDistance import DiehardMinimumDistance
from diehardtest.Diehard3DSphere import Diehard3DSphereTest
from diehardtest.DiehardSqueeze import DiehardSqueezeTest
from diehardtest.DiehardOverlappingSums import DiehardOverlappingSums
from diehardtest.DiehardRuns import DiehardRuns
from diehardtest.DiehardCraps import DiehardCraps

class Main(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master=master)
        self._master = master
        self.init_variables()
        self.init_window()

    def init_variables(self):
        self._test_type = [
                            "01. Birthday Spacings Test",
                            "02. Overlapping Sums Test",
                            "03. Runs Test",
                            "04. Craps Test",
                            "05. 32x32 Binary Rank Test",
                            "06. 6x8 Binary Rank Test",
                            "07. Bitstream Test",
                            "08. Minimum Distance (2D Circle) Test",
                            "09. Count the 1s (Stream) Test",
                            "10. Count the 1s (Byte) Test",
                            "11. Parking Lot Test",
                            "12. OPERM5 Test",
                            "13. 3D Sphere (Minimum Distance) Test",
                            "14. Squeeze Test",
                            "15. OPSO Test",
                            "16. OQSO Test",
                            "17. DNA Test"
                    ]

        self._test_functions = {
            0: DiehardBirthdaySpacings.run_test,
            1: DiehardOverlappingSums.run_test,
            2: DiehardRuns.run_test,
            3: DiehardCraps.run_test,
            4: Diehard32x32BinaryRank.run_test,
            5: Diehard6x8BinaryRank.run_test,
            6: DiehardBitstream.run_test,
            7: DiehardMinimumDistance.run_test,
            8: DiehardCountOnes.run_test,
            9: DiehardCountOnesByte.run_test,
            10: DiehardParkingLotTest.run_test,
            11: DiehardOPERM5.run_test,
            12:Diehard3DSphereTest.run_test,
            13: DiehardSqueezeTest.run_test,
            14: DiehardOPSOTest.run_test,
            15: DiehardOQSOTest.run_test,
            16: DiehardDNATest.run_test,
        }

        self._test_results = []

    def init_window(self):
        frame_title = "Diehard Randomness Test Suite"
        LabelTag(self.master, frame_title, 0, 5, 1260)

        input_label_frame = LabelFrame(self.master, text="Input Data")
        input_label_frame.config(font=("Calibri", 14))
        input_label_frame.place(x=20, y=30, width=1260, height=125)

        self.__binary_input = Input(input_label_frame, "Binary Data", 10, 5)
        self.__binary_file_input = Input(input_label_frame, "Binary Data File", 10, 35, True,
                                         self.select_binary_file, button_xcoor=1060, button_width=160)
        self.__string_data_file_input = Input(input_label_frame, 'String Data File', 10, 65, True,
                                              self.select_data_file, button_xcoor=1060, button_width=160)

        self.test_label_frame = LabelFrame(self.master, text="Randomness Testing", padx=15, pady=15)
        self.test_label_frame.config(font=("Calibri", 14))
        self.test_label_frame.place(x=20, y=155, width=1260, height=300)

        test_type_label_01 = LabelTag(self.test_label_frame, 'Test Type', 10, 5, 250, 11, border=2,
                                   relief="groove")
        p_value_label_01 = LabelTag(self.test_label_frame, 'P-Value', 265, 5, 235, 11, border=2,
                                 relief="groove")
        result_label_01 = LabelTag(self.test_label_frame, 'Result', 505, 5, 110, 11, border=2,
                                relief="groove")

        test_type_label_02 = LabelTag(self.test_label_frame, 'Test Type', 620, 5, 250, 11, border=2,
                                      relief="groove")
        p_value_label_02 = LabelTag(self.test_label_frame, 'P-Value', 875, 5, 235, 11, border=2,
                                    relief="groove")
        result_label_02 = LabelTag(self.test_label_frame, 'Result', 1115, 5, 110, 11, border=2,
                                   relief="groove")

        self._test = []

        self._birthday_spacing = TestItem(self.test_label_frame, self._test_type[0], 10, 35, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._birthday_spacing)

        self._sums = TestItem(self.test_label_frame, self._test_type[1], 620, 35, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._sums)

        self._runs = TestItem(self.test_label_frame, self._test_type[2], 10, 60, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._runs)

        self._craps = TestItem(self.test_label_frame, self._test_type[3], 620, 60, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._craps)

        self._32x32_binary_rank = TestItem(self.test_label_frame, self._test_type[4], 10, 85, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._32x32_binary_rank)

        self._6x8_binary_rank = TestItem(self.test_label_frame, self._test_type[5], 620, 85, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._6x8_binary_rank)

        self._bitstream = TestItem(self.test_label_frame, self._test_type[6], 10, 110, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._bitstream)

        self._2D_min_dist = TestItem(self.test_label_frame, self._test_type[7], 620, 110, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._2D_min_dist)

        self._count_ones_stream = TestItem(self.test_label_frame, self._test_type[8], 10, 135, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._count_ones_stream)

        self._count_ones_byte = TestItem(self.test_label_frame, self._test_type[9], 620, 135, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._count_ones_byte)

        # self._parking_lot = TestItem(self.test_label_frame, self._test_type[10], 10, 160, serial=True, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11, two_columns=True)
        # self._test.append(self._parking_lot)

        self._parking_lot = TestItem(self.test_label_frame, self._test_type[10], 10, 160, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._parking_lot)

        self._operm5 = TestItem(self.test_label_frame, self._test_type[11], 620, 160, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._operm5)

        self._3D_min_dist = TestItem(self.test_label_frame, self._test_type[12], 10, 185, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._3D_min_dist)

        self._squeeze = TestItem(self.test_label_frame, self._test_type[13], 620, 185, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._squeeze)

        self._result_field = [
            self._birthday_spacing,
            self._sums,
            self._runs,
            self._craps,
            self._32x32_binary_rank,
            self._6x8_binary_rank,
            self._bitstream,
            self._2D_min_dist,
            self._count_ones_stream,
            self._count_ones_byte,
            self._parking_lot,
            self._operm5,
            self._3D_min_dist,
            self._squeeze
        ]

       
        # LabelTag(test_label_frame, "Test Type", 10, 5, 150, font_size=12, relief="groove")
        # test_type_label = LabelTag(test_label_frame, 'Test Type', 10, 5, 350, 12, border=2,relief="groove")
        # p_value_label = LabelTag(test_label_frame, 'P-Value', 365, 5, 500, 12, border=2,relief="groove")
        # result_label = LabelTag(test_label_frame, 'Result', 870, 5, 350, 12, border=2,relief="groove")
        # LabelTag(test_label_frame, "P-Value", 350, 5, 180, font_size=12, relief="groove")
        # LabelTag(test_label_frame, "Result", 8770, 5, 350, font_size=12, relief="groove")

        # self._tests = []

        # self.__monobit = TestItem(self.__stest_selection_label_frame, self.__test_type[0], 10, 35)
        # self.__test.append(self.__monobit)

        # self.__cusum_f = TestItem(self.__stest_selection_label_frame, self.__test_type[12], 10, 335)
        # self.__test.append(self.__cusum_f)

        # self.__cusum_r = TestItem(self.__stest_selection_label_frame, self.__test_type[13], 10, 360)
        # self.__test.append(self.__cusum_r)
        # for i, test_name in enumerate(self._test_type):
        #     y_offset = 35 + (i * 30)
        #     test_item = TestItem(test_label_frame, test_name, 10, y_offset,
        #                          p_value_x_coor=365, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        #     self._tests.append(test_item)

        # execute_button = CustomButton(self.master, "Execute Test", 20, 615, 100, self.execute)
        save_button = CustomButton(self.master, "Save Results", 385, 535, 100, self.save_results)
        # reset_button = CustomButton(self.master, "Reset", 230, 615, 100, self.reset)
        # exit_button = CustomButton(self.master, "Exit", 335, 615, 100, self.exit)

        select_all_button = CustomButton(self.master, 'Select All Test', 20, 535, 100, self.select_all)
        deselect_all_button = CustomButton(self.master, 'De-Select All Test', 125, 535, 150, self.deselect_all)
        execute_button = CustomButton(self.master, 'Execute Test', 280, 535, 100, self.execute)
        # save_button = CustomButton(self.master, 'Save as Text File', 385, 615, 100, self.save_result_to_file)
        reset_button = CustomButton(self.master, 'Reset', 490, 535, 100, self.reset)
        exit = CustomButton(self.master, 'Exit Program', 595, 535, 100, self.exit)

    def select_binary_file(self):
        self.__file_name = askopenfilename(initialdir=os.getcwd(), title="Select Binary Input File.")
        if self.__file_name:
            self.__binary_input.set_data("")
            self.__binary_file_input.set_data(self.__file_name)
            self.__is_binary_file = True
            self.__is_data_file = False
    
    def select_data_file(self):
        """
        Called tkinter.askopenfilename to give user an interface to select the string input file and perform the following:
        1.  Clear Binary Data Input Field. (The textfield)
        2.  Clear Binary Data File Input Field.
        3.  Set selected file name to String Data File Input Field.

        :return: None
        """
        print('Select Data File')
        self.__file_name = askopenfilename(initialdir=os.getcwd(), title="Select Data File.")
        if self.__file_name:
            self.__binary_input.set_data('')
            self.__binary_file_input.set_data('')
            self.__string_data_file_input.set_data(self.__file_name)
            self.__is_binary_file = False
            self.__is_data_file = True


    def execute(self):
        print("Executing selected Tests")

        # if len(self.__binary_input.get_data().strip().rstrip()) == 0 and\
        #         len(self.__binary_data_file_input.get_data().strip().rstrip()) == 0 and\
        #         len(self.__string_data_file_input.get_data().strip().rstrip()) == 0:
        #     messagebox.showwarning("Warning",
        #                            'You must input the binary data or read the data from from the file.')

        if not self.__binary_input.get_data() and not self.__binary_file_input.get_data() and self.__string_data_file_input.get_data():
            messagebox.showwarning("Warning", "You must provide binary data or select a file.")
            return None
        
        elif len(self.__binary_input.get_data().strip().rstrip()) > 0 and\
                len(self.__binary_file_input.get_data().strip().rstrip()) > 0 and\
                len(self.__string_data_file_input.get_data().strip().rstrip()) > 0:
            messagebox.showwarning("Warning",
                                   'You can either input the binary data or read the data from from the file.')
            return None

        input_data = []
        if self.__binary_input.get_data():
            input_data.append(self.__binary_input.get_data())
        elif self.__binary_file_input.get_data():
            with open(self.__file_name, "r") as file:
                input_data.append(file.read().strip())

        try:
            self._test_results = []
            for data in input_data:
                results = []
                for idx, test_item in enumerate(self._test):
                    if test_item.get_check_box_value() == 1:
                        test_func = self._test_functions[idx]
                        p_value, result = test_func(data)
                        # print("test_func,p_value",test_func,p_value)
                        results.append((idx, p_value, result))
                self._test_results.append(results)
            print("diehard_test_results",self._test_results)
            self.write_results(self._test_results[0])
            messagebox.showinfo("Execute", "Tests completed successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def write_results(self, results):
        # for result in results:
        # print(results)
        for result in  results:
            idx = result[0]
            print(self._test[idx],result[1], result[2])
            self._test[idx].set_p_value(result[1])
            self._test[idx].set_result_value(result[2])

    def save_results(self):
        output_file = asksaveasfile(mode="w", defaultextension=".txt")
        if output_file:
            output_file.write("Diehard Test Results\n\n")
            for idx, result in enumerate(self._test_results[0]):
                output_file.write(f"{self._test_type[idx]}: P-Value = {result[0]}, Result = {result[1]}\n")
            output_file.close()
            messagebox.showinfo("Save", "Results saved successfully.")

    def reset(self):
        self.__binary_input.set_data("")
        self.__binary_file_input.set_data("")
        self.__string_data_file_input.set_data('')
        self.__is_binary_file = False
        self.__is_data_file = False
        for test_item in self._test:
            test_item.reset()
        self._test_results = []

    def exit(self):
        self._master.quit()
    
    def select_all(self):
        """
        Select all test type displayed in the GUI. (Check all checkbox)

        :return: None
        """
        print('Select All Test')
        for item in self._test:
            item.set_check_box_value(1)

    def deselect_all(self):
        """
        Unchecked all checkbox

        :return: None
        """
        print('Deselect All Test')
        for item in self._test:
            item.set_check_box_value(0)


def run_diehard_gui():
    np.seterr("raise")
    root = Tk()
    root.resizable(0, 0)
    root.geometry("1300x650")
    root.title("Diehard Randomness Test Suite")
    app = Main(root)
    app.mainloop()

# run_diehard_gui()
