import os
import numpy as np
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter import messagebox
import tkinter as tk

from GUI import CustomButton, Input, LabelTag, TestItem
from diehardtest.DiehardBirthdaySpacings import DiehardBirthdaySpacings
from diehardtest.DiehardOperm5 import DiehardOPERM5
from diehardtest.DiehardBinaryRank32x32 import Diehard32x32BinaryRank
from diehardtest.DiehardBinaryRank6x8 import Diehard6x8BinaryRank
from diehardtest.DiehardBitstream import DiehardBitstream
from diehardtest.DiehardOPSO import DiehardOPSOTest
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
            12: Diehard3DSphereTest.run_test,
            13: DiehardSqueezeTest.run_test,
            14: DiehardOPSOTest.run_test,
            15: DiehardOQSOTest.run_test,
            16: DiehardDNATest.run_test,
        }

        self._test_results = []

    def init_window(self):
        # Set window title and background color
        frame_title = "Diehard Randomness Test Suite"
        self.master.configure(bg="#f0f0f0")  # Light gray background

        LabelTag(self.master, frame_title, 0, 5, 1260)

        input_label_frame = LabelFrame(self.master, text="Input Data", font=("Calibri", 14), bg="#f0f0f0", fg="#333")
        input_label_frame.place(x=20, y=30, width=1260, height=125)

        # Styling Input fields with background color and borders
        self.__binary_input = Input(input_label_frame, "Binary Data", 10, 5, bg="#ffffff", fg="#333", relief="solid", bd=2)
        self.__binary_file_input = Input(input_label_frame, "Binary Data File", 10, 35, True,
                                         self.select_binary_file, button_xcoor=1060, button_width=160, bg="#ffffff", fg="#333", relief="solid", bd=2)
        self.__string_data_file_input = Input(input_label_frame, 'String Data File', 10, 65, True,
                                              self.select_data_file, button_xcoor=1060, button_width=160, bg="#ffffff", fg="#333", relief="solid", bd=2)

        # Create test section frame
        self.test_label_frame = LabelFrame(self.master, text="Randomness Testing                          (alpha=0.01)", padx=15, pady=15, font=("Calibri", 14), bg="#f0f0f0", fg="#333")
        self.test_label_frame.place(x=20, y=155, width=1260, height=300)

        # Label styling with border and light colors
        test_type_label_01 = LabelTag(self.test_label_frame, 'Test Type', 10, 5, 250, 11, border=2, relief="groove", bg="#f9f9f9")
        p_value_label_01 = LabelTag(self.test_label_frame, 'P-Value', 265, 5, 235, 11, border=2, relief="groove", bg="#f9f9f9")
        result_label_01 = LabelTag(self.test_label_frame, 'Result', 505, 5, 110, 11, border=2, relief="groove", bg="#f9f9f9")

        test_type_label_02 = LabelTag(self.test_label_frame, 'Test Type', 620, 5, 250, 11, border=2, relief="groove", bg="#f9f9f9")
        p_value_label_02 = LabelTag(self.test_label_frame, 'P-Value', 875, 5, 235, 11, border=2, relief="groove", bg="#f9f9f9")
        result_label_02 = LabelTag(self.test_label_frame, 'Result', 1115, 5, 110, 11, border=2, relief="groove", bg="#f9f9f9")

        self._test = []

        # Adding Test Items with consistent styling
        self._birthday_spacing = TestItem(self.test_label_frame, self._test_type[0], 10, 35, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._birthday_spacing)

        # Repeat for other tests...

        # Buttons with rounded corners, background color and borders
        save_button = CustomButton(self.master, "Save Results", 385, 535, 100, self.save_results, bg="#5cb85c", fg="white", relief="solid", bd=2)
        select_all_button = CustomButton(self.master, 'Select All Test', 20, 535, 100, self.select_all, bg="#0275d8", fg="white", relief="solid", bd=2)
        deselect_all_button = CustomButton(self.master, 'De-Select All Test', 125, 535, 150, self.deselect_all, bg="#d9534f", fg="white", relief="solid", bd=2)
        execute_button = CustomButton(self.master, 'Execute Test', 280, 535, 100, self.execute, bg="#5bc0de", fg="white", relief="solid", bd=2)
        reset_button = CustomButton(self.master, 'Reset', 490, 535, 100, self.reset, bg="#f0ad4e", fg="white", relief="solid", bd=2)
        exit = CustomButton(self.master, 'Exit Program', 595, 535, 100, self.exit, bg="#d9534f", fg="white", relief="solid", bd=2)

    def select_binary_file(self):
        self.__file_name = askopenfilename(initialdir=os.getcwd(), title="Select Binary Input File.")
        if self.__file_name:
            self.__binary_input.set(self.__file_name)

    def select_data_file(self):
        self.__file_name = askopenfilename(initialdir=os.getcwd(), title="Select String Data File.")
        if self.__file_name:
            self.__string_data_file_input.set(self.__file_name)

    def save_results(self):
        output_file = asksaveasfile(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if output_file:
            # Process the results and save to file
            pass

    def select_all(self):
        for test_item in self._test:
            test_item.select()

    def deselect_all(self):
        for test_item in self._test:
            test_item.deselect()

    def execute(self):
        for test_item in self._test:
            test_item.execute()

    def reset(self):
        # Reset the application state
        pass

    def exit(self):
        self.master.quit()

# Create the main window
# def run_diehard_gui():
#     np.seterr("raise")
#     root = Tk()
#     root.resizable(0, 0)
#     root.geometry("1300x650")
#     root.title("Diehard Randomness Test Suite")
#     app = Main(root)
#     app.mainloop()

def run_diehard_gui(parent, on_close):
    """Launches the Diehard GUI."""
    def on_back():
        parent.destroy()
        on_close()

    np.seterr('raise')  # Make exceptions fatal
    diehard_window = tk.Toplevel(parent)
    diehard_window.resizable(0, 0)
    diehard_window.geometry("1300x650")
    # root.title('Test Suite for NIST Random Numbers')

    # diehard_window.wm_attributes("-topmost", 1)
    # diehard_window.focus_force()

    exit = CustomButton(diehard_window, 'Back', 695, 535, 100, on_back)
    # back_button = tk.Button(root, text="Back to Main Menu", command=on_back)
    # back_button.pack(side=tk.BOTTOM, pady=10)

    # Ensure the Toplevel window behaves like a modal dialog
    diehard_window.transient(parent)
    diehard_window.grab_set()
    # parent.wait_window(diehard_window)
    app = Main(diehard_window)
    # app.focus_displayof()
    diehard_window.mainloop()
