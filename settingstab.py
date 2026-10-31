import customtkinter as ctk

def budowa(master):
    frame = ctk.CTkFrame(master, corner_radius=10)

    tytul = ctk.CTkLabel(frame, text="⚙️ Panel Ustawień", font=("Arial", 24, "bold"))
    tytul.pack(pady=20)

#Powiadomienia
    switch = ctk.CTkSwitch(frame, text="Powiadomienia dzwiękowe")
    switch.pack(pady=10)


#motyw
    label_motyw = ctk.CTkLabel(frame, text="Wygląd aplikacji:", font=("Arial", 16))
    label_motyw.pack(pady=(10, 5))

    def zmien_motyw(wybor):
        if wybor == "Jasny":
            ctk.set_appearance_mode("Light")
        elif wybor == "Ciemny":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("system")

    menu = ctk.CTkOptionMenu(frame, values=["System", "Jasny", "Ciemny"], command=zmien_motyw)
    menu.pack(pady=10)

#Zapisz
    save = ctk.CTkButton(frame, text="Zapisz zmiany", fg_color="green")
    save.pack(pady=20)

    return frame 




