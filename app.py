from tkinter import *
from detect import personDetection
import customtkinter as ctk

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

root = Tk()
root.title("CustomTkinter complex_example.py")
root.geometry(f"{1100}x{580}")

# configure grid layout (4x4)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure((2, 3), weight=0)
root.grid_rowconfigure((0, 1, 2), weight=1)

# create sidebar frame with widgets
root.sidebar_frame = ctk.CTkFrame(
    root, width=140, corner_radius=80, fg_color='red')
root.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
root.sidebar_frame.grid_rowconfigure(4, weight=1)
root.logo_label = ctk.CTkLabel(
    root.sidebar_frame, text="ctk", font=ctk.CTkFont(size=20, weight="bold"))
root.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
root.sidebar_button_1 = ctk.CTkButton(
    root.sidebar_frame)
root.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
root.sidebar_button_2 = ctk.CTkButton(
    root.sidebar_frame)
root.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
root.sidebar_button_3 = ctk.CTkButton(
    root.sidebar_frame)
root.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
root.appearance_mode_label = ctk.CTkLabel(
    root.sidebar_frame, text="Appearance Mode:", anchor="w")
root.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
root.appearance_mode_optionemenu = ctk.CTkOptionMenu(
    root.sidebar_frame, values=["Light", "Dark", "System"])
root.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
root.scaling_label = ctk.CTkLabel(
    root.sidebar_frame, text="UI Scaling:", anchor="w")
root.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
root.scaling_optionemenu = ctk.CTkOptionMenu(
    root.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"])
root.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))


# frame1 = ctk.CTkFrame(root, width=500, height=500)
# frame1.pack()

# btn_absence = ctk.CTkButton(frame1, text="Absence Mode")
# btn_absence.pack()
# btn_learn = ctk.CTkButton(frame1, text="Learn Mode")
# btn_learn.pack()
# btn_exam = ctk.CTkButton(frame1, text="Exam Mode")
# btn_exam.pack()

root.mainloop()
