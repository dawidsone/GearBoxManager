from datetime import datetime
import customtkinter as ctk

# Ustawienia motywu
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- ROZBUDOWANE SZTUCZNE DANE ---
MOCK_SCHEDULE = [
    {
        "id": 101,
        "dzien": "Poniedziałek",
        "godzina": "08:00 - 09:30",
        "przedmiot": "Matematyka Dyskretna",
        "typ": "Wykład",
        "prowadzacy": "dr Jan Kowalski",
        "sala": "A1",
        "notatka": "",
    },
    {
        "id": 102,
        "dzien": "Poniedziałek",
        "godzina": "09:45 - 11:15",
        "przedmiot": "Podstawy Programowania",
        "typ": "Laboratorium",
        "prowadzacy": "mgr Anna Nowak",
        "sala": "C3",
        "notatka": "Pamiętać o wysłaniu projektu do niedzieli!",
    },
    {
        "id": 103,
        "dzien": "Wtorek",
        "godzina": "11:30 - 13:00",
        "przedmiot": "Mikroekonomia",
        "typ": "Ćwiczenia",
        "prowadzacy": "prof. Piotr Wiśniewski",
        "sala": "B12",
        "notatka": "",
    },
    {
        "id": 104,
        "dzien": "Środa",
        "godzina": "10:00 - 11:30",
        "przedmiot": "Bazy Danych",
        "typ": "Laboratorium",
        "prowadzacy": "dr inż. Adam Malinowski",
        "sala": "D10",
        "notatka": "",
    },
    {
        "id": 105,
        "dzien": "Czwartek",
        "godzina": "13:15 - 14:45",
        "przedmiot": "Statystyka Opisowa",
        "typ": "Wykład",
        "prowadzacy": "dr Ewa Zielińska",
        "sala": "A5",
        "notatka": "",
    },
    {
        "id": 106,
        "dzien": "Piątek",
        "godzina": "08:00 - 09:30",
        "przedmiot": "Język Angielski C1",
        "typ": "Ćwiczenia",
        "prowadzacy": "mgr John Smith",
        "sala": "L1",
        "notatka": "",
    },
    {
        "id": 107,
        "dzien": "Sobota",
        "godzina": "09:00 - 12:15",
        "przedmiot": "Projekt Zespołowy",
        "typ": "Laboratorium",
        "prowadzacy": "dr inż. Marek Nowak",
        "sala": "Lab 4",
        "notatka": "",
    },
    {
        "id": 108,
        "dzien": "Niedziela",
        "godzina": "10:00 - 11:30",
        "przedmiot": "Seminarium Dyplomowe",
        "typ": "Seminarium",
        "prowadzacy": "prof. dr hab. Anna Kowalczyk",
        "sala": "Online",
        "notatka": "",
    },
]

DNI_TYGODNIA = [
    "Poniedziałek",
    "Wtorek",
    "Środa",
    "Czwartek",
    "Piątek",
    "Sobota",
    "Niedziela",
]

# Kolory dla poszczególnych typów zajęć
TYP_COLORS = {
    "Wykład": "#8E44AD",  # Fioletowy
    "Ćwiczenia": "#2980B9",  # Niebieski
    "Laboratorium": "#27AE60",  # Zielony
    "Seminarium": "#D35400",  # Pomarańczowy
}


class ScheduleApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("UEKat Student Planner — Pro")
        self.geometry("1000x700")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Zmienne stanu
        self.selected_day = "Poniedziałek"
        self.sidebar_visible = True
        self.day_buttons = {}

        # Budowa interfejsu
        self._setup_sidebar()
        self._setup_main_area()

        # Uruchomienie zegara i wyrenderowanie planu
        self._update_clock()
        self._render_schedule()

    def _setup_sidebar(self):
        """Boczny panel z logo, zegarem, przyciskami i statystykami"""
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # 1. Logo / Tytuł
        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="🎓 Student\nPlanner",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        self.logo_label.pack(padx=20, pady=(20, 15))

        # 2. WIDGET ZEGARA
        self.clock_frame = ctk.CTkFrame(self.sidebar, fg_color="#2b2b2b")
        self.clock_frame.pack(padx=15, pady=10, fill="x")

        self.lbl_clock = ctk.CTkLabel(
            self.clock_frame,
            text="00:00:00",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1f6aa5",
        )
        self.lbl_clock.pack(pady=(8, 0))

        self.lbl_date = ctk.CTkLabel(
            self.clock_frame,
            text="Ładowanie daty...",
            font=ctk.CTkFont(size=11),
            text_color="#aaaaaa",
        )
        self.lbl_date.pack(pady=(0, 8))

        # Separator
        ctk.CTkFrame(self.sidebar, height=2, fg_color="#3a3a3a").pack(
            fill="x", padx=15, pady=15
        )

        # 3. Przycisk Akcji
        self.btn_import = ctk.CTkButton(
            self.sidebar,
            text="🔄 Pobierz z USOS",
            font=ctk.CTkFont(weight="bold"),
            command=self.import_usos,
        )
        self.btn_import.pack(padx=15, pady=5, fill="x")

        # 4. Przełącznik Motywu na dole
        self.theme_switch = ctk.CTkSwitch(
            self.sidebar, text="Tryb Ciemny", command=self.toggle_theme
        )
        self.theme_switch.pack(padx=20, pady=(30, 20), side="bottom")
        self.theme_switch.select()

    def _setup_main_area(self):
        """Prawy panel: wyszukiwarka, dni tygodnia i kafelki"""
        self.right_container = ctk.CTkFrame(self, fg_color="transparent")
        self.right_container.grid(
            row=0, column=1, padx=20, pady=15, sticky="nsew"
        )
        self.right_container.grid_columnconfigure(0, weight=1)
        self.right_container.grid_rowconfigure(2, weight=1)

        # GÓRNY PASEK: Przycisk Toggle + Wyszukiwarka
        self.top_bar = ctk.CTkFrame(
            self.right_container, fg_color="transparent"
        )
        self.top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        btn_toggle = ctk.CTkButton(
            self.top_bar,
            text="☰",
            width=35,
            fg_color="transparent",
            hover_color="#1f6aa5",
            command=self.toggle_sidebar,
        )
        btn_toggle.pack(side="left", padx=(0, 10))

        # WYSZUKIWARKA NA ŻYWO
        self.search_entry = ctk.CTkEntry(
            self.top_bar,
            placeholder_text="🔍 Szukaj przedmiotu, sali lub prowadzącego...",
            height=35,
        )
        self.search_entry.pack(side="left", fill="x", expand=True)
        # Reagowanie na każde wpisanie litery
        self.search_entry.bind("<KeyRelease>", lambda event: self._render_schedule())

        # PASEK DNI TYGODNIA
        self.days_frame = ctk.CTkScrollableFrame(
            self.right_container,
            orientation="horizontal",
            height=45,
            fg_color="transparent",
        )
        self.days_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        for dzien in DNI_TYGODNIA:
            btn = ctk.CTkButton(
                self.days_frame,
                text=dzien,
                width=110,
                fg_color=(
                    "#1f6aa5" if dzien == self.selected_day else "#3a3a3a"
                ),
                command=lambda d=dzien: self.select_day(d),
            )
            btn.pack(side="left", padx=4)
            self.day_buttons[dzien] = btn

        # GŁÓWNY OBSZAR PRZEWIJANY
        self.main_frame = ctk.CTkScrollableFrame(
            self.right_container,
            label_text=f"Plan Zajęć — {self.selected_day}",
        )
        self.main_frame.grid(row=2, column=0, sticky="nsew")

    def _update_clock(self):
        """Aktualizuje zegar cyfrowy co 1 sekundę"""
        now = datetime.now()
        self.lbl_clock.configure(text=now.strftime("%H:%M:%S"))
        self.lbl_date.configure(text=now.strftime("%A, %d.%m.%Y r."))
        self.after(1000, self._update_clock)

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar.grid_forget()
            self.sidebar_visible = False
        else:
            self.sidebar.grid(row=0, column=0, sticky="nsew")
            self.sidebar_visible = True

    def select_day(self, dzien):
        self.selected_day = dzien

        for d, btn in self.day_buttons.items():
            btn.configure(
                fg_color="#1f6aa5" if d == dzien else "#3a3a3a"
            )

        self.main_frame.configure(
            label_text=f"Plan Zajęć — {self.selected_day}"
        )
        self._render_schedule()

    def _render_schedule(self):
        """Czyści widok i generuje kafelki uwzględniając wybrany dzień oraz wyszukiwarkę"""
        for child in self.main_frame.winfo_children():
            child.destroy()

        query = self.search_entry.get().lower().strip()

        # Filtrowanie danych
        filtered = [
            item for item in MOCK_SCHEDULE if item["dzien"] == self.selected_day
        ]

        if query:
            filtered = [
                item
                for item in filtered
                if query in item["przedmiot"].lower()
                or query in item["prowadzacy"].lower()
                or query in item["sala"].lower()
                or query in item["typ"].lower()
            ]

        # Pasek podsumowania na samej górze planu
        stats_text = (
            f"Liczba zajęć: {len(filtered)}"
            if not query
            else f"Wyniki wyszukiwania dla '{query}': {len(filtered)}"
        )
        lbl_stats = ctk.CTkLabel(
            self.main_frame, text=stats_text, text_color="#8a8a8a"
        )
        lbl_stats.pack(anchor="w", padx=10, pady=(5, 10))

        if not filtered:
            lbl_empty = ctk.CTkLabel(
                self.main_frame,
                text="Brak zajęć spełniających kryteria! 🎉",
                font=ctk.CTkFont(size=16),
            )
            lbl_empty.pack(pady=50)
            return

        # Generowanie nowoczesnych kafelków
        for item in filtered:
            card = ctk.CTkFrame(self.main_frame, corner_radius=12)
            card.pack(fill="x", padx=5, pady=8)

            # Górny wiersz kafelka: Godzina, Sala i Kolorowa Pigułka Typu Zajęć
            header_frame = ctk.CTkFrame(card, fg_color="transparent")
            header_frame.pack(fill="x", padx=15, pady=(10, 2))

            lbl_time = ctk.CTkLabel(
                header_frame,
                text=f"⏰ {item['godzina']}   |   📍 Sala: {item['sala']}",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#a0a0a0",
            )
            lbl_time.pack(side="left")

            # Pigułka Typu (np. Wykład / Lab)
            badge_color = TYP_COLORS.get(item["typ"], "#1f6aa5")
            lbl_type = ctk.CTkLabel(
                header_frame,
                text=f" {item['typ']} ",
                font=ctk.CTkFont(size=11, weight="bold"),
                fg_color=badge_color,
                corner_radius=6,
            )
            lbl_type.pack(side="right")

            # Nazwa przedmiotu
            lbl_title = ctk.CTkLabel(
                card,
                text=item["przedmiot"],
                font=ctk.CTkFont(size=17, weight="bold"),
            )
            lbl_title.pack(anchor="w", padx=15, pady=(2, 2))

            # Prowadzący
            lbl_teacher = ctk.CTkLabel(
                card, text=f"👤 {item['prowadzacy']}", text_color="#cccccc"
            )
            lbl_teacher.pack(anchor="w", padx=15, pady=(0, 10))

            # SEKCJA NOTATKI (jeśli istnieje, wyświetla się ładne szare pole)
            if item["notatka"]:
                note_box = ctk.CTkFrame(card, fg_color="#2b2b2b", corner_radius=8)
                note_box.pack(fill="x", padx=15, pady=(0, 10))

                lbl_note_title = ctk.CTkLabel(
                    note_box,
                    text="📌 Notatka:",
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#1f6aa5",
                )
                lbl_note_title.pack(anchor="w", padx=10, pady=(5, 0))

                lbl_note_content = ctk.CTkLabel(
                    note_box, text=item["notatka"], wraplength=500, justify="left"
                )
                lbl_note_content.pack(anchor="w", padx=10, pady=(0, 5))

            # Przycisk dodawania/edycji notatki
            btn_note_text = "✏️ Edytuj notatkę" if item["notatka"] else "📝 Dodaj notatkę"
            btn_note = ctk.CTkButton(
                card,
                text=btn_note_text,
                width=120,
                height=28,
                fg_color="#3a3a3a",
                hover_color="#555555",
                command=lambda i=item: self.open_note_dialog(i),
            )
            btn_note.pack(anchor="e", padx=15, pady=(0, 10))

    def open_note_dialog(self, item):
        """Otwiera okno edycji i natychmiast odświeża kafelek po zapisie"""
        dialog = ctk.CTkInputDialog(
            text=f"Wpisz/edytuj notatkę dla:\n{item['przedmiot']}",
            title="Notatka",
        )
        # Wpisanie dotychczasowej notatki w konsoli jako informacja
        note_text = dialog.get_input()

        if note_text is not None:
            item["notatka"] = note_text.strip()
            self._render_schedule()  # Odświeżenie widoku na żywo!

    def import_usos(self):
        print("[TEST] Pobieranie z USOS...")

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")


if __name__ == "__main__":
    app = ScheduleApp()
    app.mainloop()