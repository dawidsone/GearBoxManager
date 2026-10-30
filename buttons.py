import customtkinter as ctk

app = ctk.CTk()
app.geometry("800x500")

sidebar_frame = ctk.CTkFrame(app, width=200, corner_radius= 0)
sidebar_frame.grid(row= 0, column =0, padx =0, sticky ="nesw")

label = ctk.CTkLabel(sidebar_frame, text="Menu Główne", font=("Arial", 20, "bold"))
label.grid(row=0, column =0, padx= 20, pady= 20)

#Przyciski 

button1 = ctk.CTkButton(master=sidebar_frame, text="Ustawienia")
button1.grid(row=0, column=0, padx=20, pady=20)

button2 = ctk.CTkButton(master=sidebar_frame, text="Cos")
button2.grid(row=0, column=0, padx=20, pady=20)

app.mainloop()
