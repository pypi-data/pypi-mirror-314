import customtkinter as ctk
from ctkcalendar import CTkCalendar  # Importando a nova classe CTkCalendar
import tkinter as tk
import datetime
from typing import Callable  # Certifique-se de importar Callable para anotações de tipo


class CTkDateEntry(ctk.CTkFrame):
    def __init__(self,
                 master=None,  # Argumento não padrão deve vir depois de argumentos padrão.
                 width: int = 140, 
                 height: int = 28, 
                 corner_radius: int | None = None, 
                 bg_color: str | tuple = "transparent", 
                 fg_color: str | tuple | None = None, 
                 button_color: str | tuple | None = None, 
                 button_hover_color: str | tuple | None = None, 
                 text_color: str | tuple | None = None, 
                 text_color_disabled: str | tuple | None = None, 
                 calendar_fg_color: str | tuple | None = None, 
                 calendar_hover_color: str | tuple | None = None, 
                 calendar_text_color: str | tuple | None = None, 
                 font: tuple | ctk.CTkFont | None = None, 
                 calendar_font: tuple | ctk.CTkFont | None = None, 
                 values: list | None = None, 
                 variable: tk.Variable | None = None, 
                 state: str = tk.NORMAL, 
                 hover: bool = True, 
                 command: Callable[[str], None] | None = None,  # Correção feita aqui
                 dynamic_resizing: bool = True, 
                 anchor: str = "w", 
                 **kwargs: any):

        super().__init__(master, **kwargs)

        # Variável para armazenar a data selecionada
        self.selected_date = tk.StringVar()

        # Campo de entrada para exibir a data
        self.entry = ctk.CTkEntry(self, textvariable=self.selected_date, width=width)
        self.entry.grid(row=0, column=0, padx=0, pady=0, columnspan=2)

        # Botão para abrir o calendário
        self.calendar_button = ctk.CTkButton(self, text="📅", width=24, command=self.open_calendar, font=('noto sans', 12))
        self.calendar_button.grid(row=0, column=1, padx=0, pady=0, sticky='e')

        # Definir uma data inicial (opcional)
        self.selected_date.set(self.get_current_date())

    def get_current_date(self):
        """Retorna a data atual formatada."""
        return datetime.datetime.now().strftime("%d/%m/%Y")

    def open_calendar(self):
        """Abre o CTkCalendar em uma nova janela."""
        self.calendar_window = ctk.CTkToplevel(self)
        self.calendar_window.resizable(False, False)
        self.calendar_window.title("")
        self.calendar_window.iconbitmap()

        # Traz a janela para o topo e bloqueia a interação com a janela principal
        self.calendar_window.grab_set()
        self.calendar_window.lift()
        self.calendar_window.focus_force()

        # Posição da janela perto do widget
        x = self.winfo_rootx() + self.entry.winfo_x()
        y = self.winfo_rooty() + self.entry.winfo_height()
        self.calendar_window.geometry(f"+{x}+{y}")

        # Adicionar o widget CTkCalendar
        self.cal = CTkCalendar(self.calendar_window, command=self.set_date)
        self.cal.pack(padx=10, pady=10)

    def set_date(self, selected_date):
        """Define a data selecionada no campo de entrada."""
        self.selected_date.set(selected_date)
        self.calendar_window.destroy()

