import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from Main import run_nist_gui
from diehardtest.Main1 import run_diehard_gui
from TestU01.TestU01Main import run_testu01_gui

class RandomnessTesterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Statistical Tests for Randomness in Cryptographic Applications")
        self.root.geometry("600x400")
        
        # Main Menu
        self.main_menu()

    def main_menu(self):
        """Display the main menu with test options."""
        self.clear_window()
        
        tk.Label(self.root, text="Select Randomness Test", font=("Arial", 16)).pack(pady=20)

        # Add buttons for each test
        tk.Button(self.root, text="NIST Test", font=("Arial", 12),
                  command=self.open_nist_window).pack(pady=10)
        tk.Button(self.root, text="Dieharder Test", font=("Arial", 12),
                  command=self.open_dieharder_window).pack(pady=10)
        tk.Button(self.root, text="TestU01", font=("Arial", 12),
                  command=self.open_testu01_window).pack(pady=10)
        tk.Button(self.root, text="Custom Test", font=("Arial", 12),
                  command=self.open_custom_test_window).pack(pady=10)
        
        # Exit Button
        tk.Button(self.root, text="Exit", font=("Arial", 12), command=self.root.quit).pack(pady=20)

    def open_nist_window(self):
        """Redirect to the NIST randomness test window."""
        # self.root.destroy()  # Close the main menu window
        # run_nist_gui()

        # self.root.withdraw()  # Hide the main menu window

        # def return_to_main_menu():
        #     """Close the NIST GUI and return to the main menu."""
        #     nist_root.destroy()  # Close the NIST test window
        #     self.root.deiconify()  # Show the main menu window

        # # Create a new top-level window for the NIST test
        # nist_root = tk.Toplevel()

        # # Initialize the NIST test GUI
        # from Main import Main
        # app = Main(nist_root)

        # # Add a Back button to return to the main menu
        # back_button = tk.Button(nist_root, text="Back to Main Menu", font=("Arial", 12),
        #                         command=return_to_main_menu)
        # back_button.pack(side=tk.BOTTOM, pady=10)


        self.hide_main_window()
        nist_root = tk.Toplevel()
        nist_root.title("NIST Randomness Tests")
        run_nist_gui(parent=nist_root, on_close=self.show_main_window)

    def open_dieharder_window(self):
        """Redirect to the Dieharder randomness test window."""
        # self.root.destroy()
        # # self.randomness_test_window("Dieharder Test")
        # run_diehard_gui()
        # # self.root.withdraw()

        self.hide_main_window()
        nist_root = tk.Toplevel()
        nist_root.title("Diehard Randomness Tests")
        run_diehard_gui(parent=nist_root, on_close=self.show_main_window)

    def open_testu01_window(self):
        """Redirect to the TestU01 randomness test window."""
        # self.clear_window()
        # # self.randomness_test_window("TestU01")
        # self.root.destroy()
        # run_testu01_gui()
        # self.root.withdraw()


        self.hide_main_window()
        nist_root = tk.Toplevel()
        nist_root.title("TestU01 Randomness Tests")
        run_testu01_gui(parent=nist_root, on_close=self.show_main_window)

    def open_custom_test_window(self):
        """Redirect to the Custom randomness test window."""
        self.clear_window()
        self.randomness_test_window("Custom Test")

    def randomness_test_window(self, test_name):
        """Generic window for randomness tests."""
        tk.Label(self.root, text=f"{test_name} Options", font=("Arial", 16)).pack(pady=20)

        # File Selection
        tk.Label(self.root, text="Select Files for Testing:", font=("Arial", 12)).pack(pady=5)
        self.file_list = tk.Listbox(self.root, selectmode=tk.MULTIPLE)
        self.file_list.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        tk.Button(self.root, text="Add Files", font=("Arial", 12),
                  command=self.add_files).pack(pady=10)
        
        # Run Button
        tk.Button(self.root, text=f"Run {test_name}", font=("Arial", 12),
                  command=lambda: self.run_test(test_name)).pack(pady=10)
        
        # Back Button
        tk.Button(self.root, text="Back to Main Menu", font=("Arial", 12),
                  command=self.main_menu).pack(pady=10)

    def add_files(self):
        """Add files to the file list."""
        files = filedialog.askopenfilenames()
        for file in files:
            self.file_list.insert(tk.END, file)

    def run_test(self, test_name):
        """Run the selected test (placeholder logic)."""
        selected_files = [self.file_list.get(idx) for idx in self.file_list.curselection()]
        if not selected_files:
            messagebox.showerror("Error", "No files selected!")
            return

        messagebox.showinfo("Running Test", f"Running {test_name} on {len(selected_files)} file(s).")
        # Add specific test logic here (e.g., calling external tools or libraries)
        print(f"Running {test_name} on files: {selected_files}")

    def clear_window(self):
        """Clear all widgets from the current window."""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def hide_main_window(self):
        self.root.withdraw()
    
    def show_main_window(self):
        self.root.deiconify()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = RandomnessTesterApp(root)
    root.mainloop()




# import tkinter as tk
# from tkinter import ttk, filedialog, messagebox
# from Main import run_nist_gui
# from diehardtest.Main1 import run_diehard_gui
# from TestU01.TestU01Main import run_testu01_gui

# class RandomnessTesterApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Statistical Tests for Randomness in Cryptographic Applications")
#         self.root.geometry("600x400")
#         self.root.config(bg="#f0f0f0")  # Set a light background color

#         # Main Menu
#         self.main_menu()

#     def main_menu(self):
#         """Display the main menu with test options."""
#         self.clear_window()
        
#         # Title Label
#         tk.Label(self.root, text="Select Randomness Test", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=30)

#         # Create a frame for the buttons
#         button_frame = tk.Frame(self.root, bg="#f0f0f0")
#         button_frame.pack()

#         # Add buttons for each test with styles
#         self.create_button(button_frame, "NIST Test", self.open_nist_window)
#         self.create_button(button_frame, "Dieharder Test", self.open_dieharder_window)
#         self.create_button(button_frame, "TestU01", self.open_testu01_window)
#         self.create_button(button_frame, "Custom Test", self.open_custom_test_window)

#         # Exit Button
#         self.create_button(self.root, "Exit", self.root.quit, bg_color="#ff6347", fg_color="white", font_size=14)

#     def create_button(self, parent, text, command, bg_color="#4CAF50", fg_color="white", font_size=12):
#         """Helper function to create styled buttons."""
#         button = tk.Button(parent, text=text, font=("Arial", font_size), command=command,
#                            bg=bg_color, fg=fg_color, relief="flat", padx=20, pady=10)
#         button.pack(pady=8, ipadx=10)

#     def open_nist_window(self):
#         """Redirect to the NIST randomness test window."""
#         self.hide_main_window()
#         nist_root = tk.Toplevel()
#         nist_root.title("NIST Randomness Tests")
#         run_nist_gui(parent=nist_root, on_close=self.show_main_window)

#     def open_dieharder_window(self):
#         """Redirect to the Dieharder randomness test window."""
#         self.hide_main_window()
#         nist_root = tk.Toplevel()
#         nist_root.title("Diehard Randomness Tests")
#         run_diehard_gui(parent=nist_root, on_close=self.show_main_window)

#     def open_testu01_window(self):
#         """Redirect to the TestU01 randomness test window."""
#         self.hide_main_window()
#         nist_root = tk.Toplevel()
#         nist_root.title("TestU01 Randomness Tests")
#         run_testu01_gui(parent=nist_root, on_close=self.show_main_window)

#     def open_custom_test_window(self):
#         """Redirect to the Custom randomness test window."""
#         self.clear_window()
#         self.randomness_test_window("Custom Test")

#     def randomness_test_window(self, test_name):
#         """Generic window for randomness tests."""
#         tk.Label(self.root, text=f"{test_name} Options", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=30)

#         # File Selection
#         tk.Label(self.root, text="Select Files for Testing:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
#         self.file_list = tk.Listbox(self.root, selectmode=tk.MULTIPLE, height=6)
#         self.file_list.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

#         # Add files button
#         self.create_button(self.root, "Add Files", self.add_files)

#         # Run Button
#         self.create_button(self.root, f"Run {test_name}", lambda: self.run_test(test_name), bg_color="#4CAF50")

#         # Back Button
#         self.create_button(self.root, "Back to Main Menu", self.main_menu, bg_color="#ff6347", fg_color="white", font_size=14)

#     def add_files(self):
#         """Add files to the file list."""
#         files = filedialog.askopenfilenames()
#         for file in files:
#             self.file_list.insert(tk.END, file)

#     def run_test(self, test_name):
#         """Run the selected test (placeholder logic)."""
#         selected_files = [self.file_list.get(idx) for idx in self.file_list.curselection()]
#         if not selected_files:
#             messagebox.showerror("Error", "No files selected!")
#             return

#         messagebox.showinfo("Running Test", f"Running {test_name} on {len(selected_files)} file(s).")
#         # Add specific test logic here (e.g., calling external tools or libraries)
#         print(f"Running {test_name} on files: {selected_files}")

#     def clear_window(self):
#         """Clear all widgets from the current window."""
#         for widget in self.root.winfo_children():
#             widget.destroy()
    
#     def hide_main_window(self):
#         """Hide the main window."""
#         self.root.withdraw()
    
#     def show_main_window(self):
#         """Show the main window."""
#         self.root.deiconify()

# # Run the application
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = RandomnessTesterApp(root)
#     root.mainloop()
