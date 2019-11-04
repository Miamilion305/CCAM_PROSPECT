import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
from pkg.InputType import InputType
from pkg.relativeReflectanceCalibration import calibrate_relative_reflectance


class MainApplication(tk.Frame):
    input_type_switcher = {
        1: InputType.FILE,
        2: InputType.FILE_LIST,
        3: InputType.DIRECTORY
    }

    def __init__(self, window, *args, **kwargs):
        tk.Frame.__init__(self, window, *args, **kwargs)
        # CREATE COMPONENTS

        # input label, entry, button
        self.input_label = tk.Label(window, text="Input: ")
        # radio button group and entries for input and output dir
        self.inputType = tk.IntVar()
        self.fileBtn = tk.Radiobutton(window, text='File', value=InputType.FILE.value, variable=self.inputType)
        self.fileBtn.select()  # select file by default
        self.listBtn = tk.Radiobutton(window, text='List Of Files', value=InputType.FILE_LIST.value,
                                      variable=self.inputType)
        self.directoryBtn = tk.Radiobutton(window, text='Directory', value=InputType.DIRECTORY.value,
                                           variable=self.inputType)
        self.in_filename_entry = tk.Entry(window, width=30)

        # output stuff
        self.separator1 = ttk.Separator(window, orient="horizontal")
        self.out_label = tk.Label(window, text="Output Directory: ")
        self.out_directory_type = tk.IntVar()
        self.use_default_out_btn = tk.Radiobutton(window, text="Use default\n (same as input dir)", value=1,
                                                  variable=self.out_directory_type, command=self.select_output_directory)
        self.use_default_out_btn.select()
        self.use_custom_out_btn = tk.Radiobutton(window, text="Use custom", value=2, variable=self.out_directory_type,
                                                 command=self.select_output_directory)
        self.out_directory = tk.Entry(window, width=15, state="disabled")
        self.outBrowseBtn = tk.Button(window, text='Browse', command=self.out_clicked, state="disabled")

        # config stuff for relative reflectance
        self.separator2 = ttk.Separator(window, orient="horizontal")
        self.relative_config = tk.IntVar()
        self.relative_label = tk.Label(window, text="Relative Reflectance Calibration:")
        self.custom_dir = tk.Entry(window, text="custom directory", width=15, state="disabled")
        self.custom_dir_browse = tk.Button(window, text="Browse", state="disabled")
        self.browseBtn = tk.Button(window, text='Browse', command=self.browse_clicked)
        self.use_default_btn = tk.Radiobutton(window, text="Use default\n (target 11 sol 76)", value=1,
                                              variable=self.relative_config, command=self.select_custom)
        self.use_default_btn.select()
        self.use_custom_btn = tk.Radiobutton(window, text="Use custom", value=2, variable=self.relative_config,
                                             command=self.select_custom)

        # 'GO' button
        self.calibrate_button = tk.Button(window, text="Calibrate", command=self.start_calibration)

        # setup the GUI layout
        self.input_label.grid(column=0, row=0, columnspan=4, sticky="w", padx=(10, 0))
        self.fileBtn.grid(column=0, row=1, sticky="w", padx=(10, 0))
        self.listBtn.grid(column=1, row=1, sticky="w")
        self.directoryBtn.grid(column=2, row=1, sticky="w")
        self.in_filename_entry.grid(column=0, row=2, columnspan=3, sticky="w", padx=(10, 0))
        self.browseBtn.grid(column=3, row=2, sticky="w")
        self.separator1.grid(column=0, row=4, columnspan=5, sticky="ew", pady=(10, 10))
        self.out_label.grid(column=0, row=6, columnspan=4, sticky="w", padx=(10, 0))
        self.use_default_out_btn.grid(column=0, row=7, rowspan=3, columnspan=3, sticky="w", padx=(10, 0))
        self.use_custom_out_btn.grid(column=2, row=7, rowspan=2, sticky="w")
        self.out_directory.grid(column=2, row=9, columnspan=2)
        self.outBrowseBtn.grid(column=4, row=9)
        self.separator2.grid(column=0, row=10, columnspan=5, sticky="ew", pady=(10, 10))
        self.relative_label.grid(column=0, row=11, columnspan=4, sticky="w", padx=(10, 0))
        self.use_default_btn.grid(column=0, row=12, rowspan=3, columnspan=3, sticky="w", padx=(10, 0))
        self.use_custom_btn.grid(column=2, row=12, rowspan=2, sticky="w")
        self.custom_dir.grid(column=2, row=14, columnspan=2)
        self.custom_dir_browse.grid(column=4, row=14)
        self.calibrate_button.grid(column=0, row=15, columnspan=5, sticky="ew", pady=(20, 0), padx=(10, 10))

    def browse_clicked(self):
        file_type = self.inputType.get()
        if file_type == InputType.FILE.value:  # file
            file = filedialog.askopenfilename()
            # get directory and set output directory
            self.out_directory.delete(0, "end")
            self.out_directory.insert(0, os.path.dirname(file)+"/")
        elif file_type == InputType.FILE_LIST.value:  # list of files
            file = filedialog.askopenfilename()
            # get directory and set output directory
            self.out_directory.delete(0, "end")
            self.out_directory.insert(0, os.path.dirname(file)+"/")
        elif file_type == InputType.DIRECTORY.value:  # directory
            file = filedialog.askdirectory()
            if not file.endswith("/"):
                file = file + "/"
            # set output directory to this directory
            self.out_directory.delete(0, "end")
            self.out_directory.insert(0, file)
        self.in_filename_entry.delete(0, "end")
        self.in_filename_entry.insert(0, file)

    def out_clicked(self):
        file = filedialog.askdirectory()
        self.out_directory.delete(0, "end")
        self.out_directory.insert(0, file)

    def select_custom(self):
        btn = self.relative_config.get()
        if btn == 1:
            self.custom_dir.config(state="disabled")
            self.custom_dir_browse.config(state="disabled")
        else:
            self.custom_dir.config(state="normal")
            self.custom_dir_browse.config(state="normal")

    def start_calibration(self):
        file_type = self.input_type_switcher.get(self.inputType.get(), "Not a valid input type")
        file = self.in_filename_entry.get()
        custom_directory = self.custom_dir.get()
        out_dir = self.out_directory.get()
        if not out_dir.endswith('/'):
            out_dir = out_dir + '/'
        calibrate_relative_reflectance(file_type, file, custom_directory, out_dir)

    def select_output_directory(self):
        btn = self.out_directory_type.get()
        if btn == 1:
            self.out_directory.config(state="disabled")
            self.outBrowseBtn.config(state="disabled")
        else:
            self.out_directory.config(state="normal")
            self.outBrowseBtn.config(state="normal")


def main():
    window = tk.Tk()
    window.title("ChemCham Calibration")
    window.geometry('410x318')
    MainApplication(window)
    window.mainloop()

