import customtkinter as ctk

# Ustawienia motywu
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- SZTUCZNE DANE NA CAŁY TYGODZIEŃ ---
MOCK_SCHEDULE = [
    {
        "id": 101,
        "dzien": "Poniedziałek",
        "godzina": "08:00 - 09:30",
        "przedmiot": "Matematyka Dyskretna",
        "prowadzacy": "dr Jan Kowalski",
        "sala": "A1",
    },
    {
        "id": 102,
        "dzien": "Poniedziałek",
        "godzina": "09:45 - 11:15",
        "przedmiot": "Podstawy Programowania",
        "prowadzacy": "mgr Anna Nowak",
        "sala": "C3",
    },
    {
        "id": 103,
        "dzien": "Wtorek",
        "godzina": "11:30 - 13:00",
        "przedmiot": "Mikroekonomia",
        "prowadzacy": "prof. Piotr Wiśniewski",
        "sala": "B12",
    },
    {
        "id": 104,
        "dzien": "Środa",
        "godzina": "10:00 - 11:30",
        "przedmiot": "Bazy Danych",
        "prowadzacy": "dr inż. Adam Malinowski",
        "sala": "D10",
    },
    {
        "id": 106,
        "dzien": "Piątek",
        "godzina": "08:00 - 09:30",
        "przedmiot": "Język Angielski C1",
        "prowadzacy": "mgr John Smith",
        "sala": "L1",
    },
]

DNI_TYGODNIA = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek","Sobota", "Niedziela"]


class ScheduleApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("UEKat Student Planner")
        self.geometry("950x650")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Domyślnie wybrany dzień i słownik na przyciski
        self.selected_day = "Poniedziałek"
        self.day_buttons = {}

        self._setup_sidebar()
        self._setup_main_area()
        self._render_schedule()

    def _setup_sidebar(self):
        """Panel boczny"""
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="Student Planner",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.pack(padx=20, pady=(20, 20))

        self.btn_import = ctk.CTkButton(
            self.sidebar, text="Pobierz z USOS", command=self.import_usos
        )
        self.btn_import.pack(padx=20, pady=10)

        self.theme_switch = ctk.CTkSwitch(
            self.sidebar, text="Tryb Ciemny", command=self.toggle_theme
        )
        self.theme_switch.pack(padx=20, pady=(30, 10), side="bottom")
        self.theme_switch.select()

    def _setup_main_area(self):
        """Główna przestrzeń z paskiem dni tygodnia"""
        self.right_container = ctk.CTkFrame(self, fg_color="transparent")
        self.right_container.grid(
            row=0, column=1, padx=20, pady=20, sticky="nsew"
        )
        self.right_container.grid_columnconfigure(0, weight=1)
        self.right_container.grid_rowconfigure(1, weight=1)

        # 1. Górny pasek z przyciskami dni tygodnia
        self.days_frame = ctk.CTkFrame(
            self.right_container, fg_color="transparent"
        )
        self.days_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        for dzien in DNI_TYGODNIA:
            btn = ctk.CTkButton(
                self.days_frame,
                text=dzien,
                width=110,
                # Podświetlenie niebieskim kolorem tylko dla wybranego dnia
                fg_color=(
                    "#1f6aa5" if dzien == self.selected_day else "#3a3a3a"
                ),
                command=lambda d=dzien: self.select_day(d),
            )
            btn.pack(side="left", padx=4)
            self.day_buttons[dzien] = btn

        # 2. Przewijany obszar na kafelki z zajęciami
        self.main_frame = ctk.CTkScrollableFrame(
            self.right_container,
            label_text=f"Plan Zajęć — {self.selected_day}",
        )
        self.main_frame.grid(row=1, column=0, sticky="nsew")

    def select_day(self, dzien):
        """Zmienia aktywny dzień i odświeża interfejs"""
        self.selected_day = dzien

        # Zmiana kolorów przycisków
        for d, btn in self.day_buttons.items():
            if d == dzien:
                btn.configure(fg_color="#1ae016")  # Aktywny (niebieski)
            else:
                btn.configure(fg_color="#073d0e")  # Nieaktywny (szary)

        # Zmiana nagłówka ramki i ponowne wyrenderowanie kafelków
        self.main_frame.configure(
            label_text=f"Plan Zajęć — {self.selected_day}"
        )
        self._render_schedule()

    def _render_schedule(self):
        """Czyści poprzednie kafelki i tworzy nowe tylko dla wybranego dnia"""
        # Usunięcie starych kafelków
        for child in self.main_frame.winfo_children():
            child.destroy()

        # Filtrowanie słownika po wybranym dniu
        filtered_schedule = [
            item for item in MOCK_SCHEDULE if item["dzien"] == self.selected_day
        ]

        # Komunikat, gdy w danym dniu brak zajęć
        if not filtered_schedule:
            lbl_empty = ctk.CTkLabel(
                self.main_frame,
                text="Brak zajęć w tym dniu! 🎉",
                font=ctk.CTkFont(size=16),
            )
            lbl_empty.pack(pady=40)
            return

        # Generowanie kafelków
        for item in filtered_schedule:
            card = ctk.CTkFrame(self.main_frame, corner_radius=10)
            card.pack(fill="x", padx=10, pady=10)

            header_text = f"{item['godzina']}  |  Sala: {item['sala']}"
            lbl_time = ctk.CTkLabel(
                card,
                text=header_text,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#8a8a8a",
            )
            lbl_time.pack(anchor="w", padx=15, pady=(10, 2))

            lbl_title = ctk.CTkLabel(
                card,
                text=item["przedmiot"],
                font=ctk.CTkFont(size=16, weight="bold"),
            )
            lbl_title.pack(anchor="w", padx=15, pady=2)

            lbl_teacher = ctk.CTkLabel(
                card, text=item["prowadzacy"], text_color="#bcbcbc"
            )
            lbl_teacher.pack(anchor="w", padx=15, pady=(2, 10))

            btn_note = ctk.CTkButton(
                card,
                text="📝 Notatka",
                width=100,
                command=lambda i=item: self.open_note_dialog(i),
            )
            btn_note.pack(anchor="e", padx=15, pady=(0, 10))

    def open_note_dialog(self, item):
        dialog = ctk.CTkInputDialog(
            text=f"Wpisz notatkę do przedmiotu:\n{item['przedmiot']}",
            title="Dodaj Notatkę",
        )
        note_text = dialog.get_input()

        if note_text is not None:
            print(
                f"[TEST] Zapisuję do bazy pod ID {item['id']}: '{note_text}'"
            )

    def import_usos(self):
        print("[TEST] Przycisk pobierania z USOS kliknięty.")

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")


if __name__ == "__main__":
    app = ScheduleApp()
    app.mainloop()