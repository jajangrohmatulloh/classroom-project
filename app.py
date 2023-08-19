from tkinter import *
from detect import detection
import customtkinter as ctk

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

root = ctk.CTk()
root.title("Real Time Detection")
root.geometry(f"{1100}x{580}")


frame1 = ctk.CTkFrame(root, width=1000, height=1000,
                      corner_radius=8, fg_color='#2A2A2A')
frame1.place(relx=0.5, rely=0.5, anchor=CENTER)

label = ctk.CTkLabel(frame1, text="Select Mode")
label.pack()

btn_absence = ctk.CTkButton(
    frame1, text="Absence Mode", command=lambda: detection('attendance'))
btn_absence.pack(padx=24, pady=16)
btn_learn = ctk.CTkButton(frame1, text="Learn Mode",
                          command=lambda: detection('learn'))
btn_learn.pack(padx=24, pady=16)
btn_exam = ctk.CTkButton(frame1, text="Exam Mode",
                         command=lambda: detection('exam'))
btn_exam.pack(padx=24, pady=16)

root.mainloop()
