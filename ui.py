import tkinter as tk
from tkinter import ttk
from converter import CONVERSIONS, get_stats

BG = "#0d0d1a"
BG2 = "#12122a"
BG3 = "#1a1a3e"
BG4 = "#222244"
FG = "#e8e8ff"
FG2 = "#8888aa"
ACCENT = "#7c4dff"
ACCENT2 = "#651fff"
GREEN = "#00e676"
ERROR = "#ff5252"
WARNING = "#ffab40"
FONT_UI = ("Segoe UI", 10)
FONT_MONO = ("Consolas", 11)
FONT_TITLE = ("Segoe UI", 15, "bold")


class CaseShiftApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CaseShift")
        self.root.geometry("950x650")
        self.root.configure(bg=BG)
        self.root.minsize(700, 500)

        self._build_header()
        self._build_input()
        self._build_results()
        self._build_statusbar()

    def _build_header(self):
        header = tk.Frame(self.root, bg=BG3, pady=14)
        header.pack(fill=tk.X)
        tk.Label(header, text="🔤 CaseShift", bg=BG3, fg=FG, font=FONT_TITLE).pack(side=tk.LEFT, padx=16)
        tk.Label(header, text="  —  Text Case Converter", bg=BG3, fg=FG2, font=FONT_UI).pack(side=tk.LEFT)

    def _build_input(self):
        outer = tk.Frame(self.root, bg=BG, pady=16)
        outer.pack(fill=tk.X, padx=24)

        header = tk.Frame(outer, bg=BG)
        header.pack(fill=tk.X, pady=(0, 8))

        tk.Label(header, text="Texto de entrada", bg=BG, fg=FG2, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)

        tk.Button(
            header, text="🗑 Limpiar", bg=BG3, fg=ERROR,
            font=("Segoe UI", 9), relief=tk.FLAT,
            padx=10, pady=3, cursor="hand2",
            activebackground=BG4, activeforeground=ERROR,
            command=self._clear
        ).pack(side=tk.RIGHT)

        tk.Button(
            header, text="📋 Pegar", bg=BG3, fg=ACCENT,
            font=("Segoe UI", 9), relief=tk.FLAT,
            padx=10, pady=3, cursor="hand2",
            activebackground=BG4, activeforeground=ACCENT,
            command=self._paste
        ).pack(side=tk.RIGHT, padx=4)

        self.input_text = tk.Text(
            outer, bg=BG2, fg=FG, font=FONT_MONO,
            insertbackground=FG, selectbackground=ACCENT,
            relief=tk.FLAT, padx=12, pady=10, height=5, wrap=tk.WORD
        )
        self.input_text.pack(fill=tk.X)
        self.input_text.bind("<KeyRelease>", self._on_text_change)

        self.stats_label = tk.Label(outer, text="", bg=BG, fg=FG2, font=("Segoe UI", 9))
        self.stats_label.pack(anchor=tk.W, pady=(6, 0))

    def _build_results(self):
        outer = tk.Frame(self.root, bg=BG, pady=8)
        outer.pack(fill=tk.BOTH, expand=True, padx=24)

        tk.Label(outer, text="Conversiones", bg=BG, fg=FG2, font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(0, 8))

        canvas_frame = tk.Frame(outer, bg=BG2)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg=BG2, highlightthickness=0)
        scroll = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.results_frame = tk.Frame(self.canvas, bg=BG2)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.results_frame, anchor="nw")

        self.results_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        self.result_labels = {}
        for name, func, example in CONVERSIONS:
            self._build_result_row(name, func, example)

    def _build_result_row(self, name, func, example):
        row = tk.Frame(self.results_frame, bg=BG3, pady=8, padx=12)
        row.pack(fill=tk.X, padx=4, pady=3)

        header = tk.Frame(row, bg=BG3)
        header.pack(fill=tk.X)

        tk.Label(header, text=name, bg=BG3, fg=ACCENT, font=("Segoe UI", 9, "bold"), width=20, anchor="w").pack(side=tk.LEFT)

        copy_btn = tk.Button(
            header, text="Copiar", bg=BG3, fg=ACCENT,
            font=("Segoe UI", 9), relief=tk.FLAT,
            padx=10, pady=2, cursor="hand2",
            activebackground=BG4, activeforeground=ACCENT,
            command=lambda f=func: self._copy_result(f)
        )
        copy_btn.pack(side=tk.RIGHT)

        result_label = tk.Label(
            row, text=example, bg=BG3, fg=FG,
            font=FONT_MONO, anchor="w", justify=tk.LEFT,
            wraplength=800
        )
        result_label.pack(fill=tk.X, pady=(4, 0))

        self.result_labels[name] = (result_label, func)

    def _build_statusbar(self):
        bar = tk.Frame(self.root, bg=BG3, pady=5)
        bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_label = tk.Label(bar, text="Listo", bg=BG3, fg=FG2, font=("Segoe UI", 9))
        self.status_label.pack(side=tk.LEFT, padx=12)
        tk.Label(bar, text="CaseShift v1.0", bg=BG3, fg=FG2, font=("Segoe UI", 9)).pack(side=tk.RIGHT, padx=12)

    def _set_status(self, text, color=None):
        self.status_label.config(text=text, fg=color or FG2)

    def _on_text_change(self, event=None):
        text = self.input_text.get("1.0", tk.END).rstrip("\n")

        for name, (label, func) in self.result_labels.items():
            if text:
                try:
                    result = func(text)
                    if not result:
                        result = "(vacío)"
                except Exception:
                    result = "(error)"
            else:
                _, _, example = next(c for c in CONVERSIONS if c[0] == name)
                result = example
            label.config(text=result, fg=FG if text else FG2)

        if text:
            stats = get_stats(text)
            self.stats_label.config(
                text=f"Líneas: {stats['lines']}  |  Palabras: {stats['words']}  |  "
                     f"Caracteres: {stats['chars']}  |  Sin espacios: {stats['chars_no_spaces']}"
            )
        else:
            self.stats_label.config(text="")

    def _copy_result(self, func):
        text = self.input_text.get("1.0", tk.END).rstrip("\n")
        if not text:
            self._set_status("⚠ Escribe algo primero", WARNING)
            return
        try:
            result = func(text)
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            self._set_status("✓ Copiado al portapapeles", GREEN)
        except Exception:
            self._set_status("❌ Error al convertir", ERROR)

    def _paste(self):
        try:
            content = self.root.clipboard_get()
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", content)
            self._on_text_change()
            self._set_status("✓ Texto pegado", GREEN)
        except Exception:
            self._set_status("⚠ Portapapeles vacío", WARNING)

    def _clear(self):
        self.input_text.delete("1.0", tk.END)
        self._on_text_change()
        self._set_status("Limpiado")