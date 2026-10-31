import customtkinter as ctk
import datetime
import settingstab
import starttab

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
frame_start = starttab.budowa(app)

# Zakładka Ustawienia
frame_ustawienia = settingstab.budowa(app)

pokaz_start() 
app.mainloop()
