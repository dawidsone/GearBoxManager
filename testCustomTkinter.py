import customtkinter

 #Ustawienia motywu
customtkinter.set_appearance_mode("System")  # Wykrywa ciemny/jasny z systemu
customtkinter.set_default_color_theme("blue") 

app = customtkinter.CTk()
app.geometry("800x600")
app.title("Plan Zajęć")

 #Nowoczesny przycisk
button = customtkinter.CTkButton(master=app, text="Pobierz plan z USOS")
button.pack(padx=20, pady=20)

app.mainloop()