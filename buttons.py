import customtkinter as ctk
import datetime

# --- 1. GŁÓWNE OKNO ---
app = ctk.CTk()
app.geometry("700x500")
app.title("Test")

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)


def pokaz_start():
    frame_ustawienia.grid_forget()
    frame_start.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

def pokaz_ustawienia():
    frame_start.grid_forget()
    frame_ustawienia.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

def zegar():
    teraz = datetime.datetime.now()
    data = teraz.strftime("%D.%M.%Y")
    czas = teraz.strftime("%H:%M:%S")

    label_data.configure(text=data)
    label_czas.configure(text=czas)
    label_czas.after(1000,zegar)

#lewy panel
sidebar_frame = ctk.CTkFrame(app, width=200, corner_radius=0)
sidebar_frame.grid(row=0, column=0, sticky="nsew")

logo = ctk.CTkLabel(sidebar_frame, text="Menu Główne", font=("Arial", 20, "bold"))
logo.grid(row=0, column=0, padx=20, pady=20)

# Przyciski
btn_start = ctk.CTkButton(sidebar_frame, text="🏠 Start", command=pokaz_start)
btn_start.grid(row=1, column=0, padx=20, pady=10)

btn_ustawienia = ctk.CTkButton(sidebar_frame, text="⚙️ Ustawienia", command=pokaz_ustawienia)
btn_ustawienia.grid(row=2, column=0, padx=20, pady=10)

#Zakladka Start
frame_start = ctk.CTkFrame(app, corner_radius=10)
label_start = ctk.CTkLabel(frame_start, text="Witaj na stronie głównej!", font=("Arial", 24))
label_start.pack(pady=(40, 10))
label_data = ctk.CTkLabel(frame_start, text="dataa", font=("Arial", 18))
label_data.pack(pady=5)

label_czas = ctk.CTkLabel(frame_start, text="czass", font=("Arial", 48, "bold"), text_color="#1f6aa5")
label_czas.pack(pady=10)



# Zakładka Ustawienia
frame_ustawienia = ctk.CTkFrame(app, corner_radius=10)
label_ustawienia = ctk.CTkLabel(frame_ustawienia, text="Panel Ustawień", font=("Arial", 24))
label_ustawienia.place(relx=0.5, rely=0.5, anchor="center")


pokaz_start() 
zegar()
app.mainloop()
