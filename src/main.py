import math
import tkinter as tk
from tkinter import ttk


class AudioLabApp:
    BACKGROUND = "#10131c"
    PANEL = "#171b27"
    ACCENT = "#8b7cff"
    CYAN = "#52e0d0"
    TEXT = "#f3f4fa"
    MUTED = "#9299ad"

    def __init__(self, root):
        self.root = root
        self.root.title("Audio Lab")
        self.root.geometry("960x600")
        self.root.minsize(700, 440)
        self.root.configure(background=self.BACKGROUND)

        self.phase = 0.0
        self.running = True
        self.after_id = None

        self._configure_styles()
        self._build_layout()
        self._draw_visualizer()
        self._animate()
        self.root.protocol("WM_DELETE_WINDOW", self._close)

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Accent.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(16, 12),
            foreground=self.TEXT,
            background=self.ACCENT,
            borderwidth=0,
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#a095ff"), ("pressed", "#7464e8")],
        )
        style.configure(
            "Subtle.TButton",
            font=("Segoe UI", 11),
            padding=(16, 12),
            foreground=self.TEXT,
            background="#292e3e",
            borderwidth=0,
        )
        style.map(
            "Subtle.TButton",
            background=[("active", "#373d51"), ("pressed", "#222635")],
        )
        style.configure(
            "Mode.TCombobox",
            font=("Segoe UI", 10),
            padding=8,
            foreground=self.TEXT,
            fieldbackground="#292e3e",
            background="#292e3e",
            arrowcolor=self.CYAN,
        )

    def _build_layout(self):
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        sidebar = tk.Frame(self.root, width=245, bg=self.PANEL, padx=28, pady=32)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)

        tk.Label(
            sidebar,
            text="AUDIO LAB",
            font=("Segoe UI", 10, "bold"),
            fg=self.CYAN,
            bg=self.PANEL,
        ).pack(anchor="w")
        tk.Label(
            sidebar,
            text="Sound in\nmotion.",
            font=("Segoe UI", 27, "bold"),
            fg=self.TEXT,
            bg=self.PANEL,
            justify="left",
        ).pack(anchor="w", pady=(18, 10))
        tk.Label(
            sidebar,
            text="A little visualizer for your next big idea.",
            font=("Segoe UI", 10),
            fg=self.MUTED,
            bg=self.PANEL,
            wraplength=185,
            justify="left",
        ).pack(anchor="w", pady=(0, 30))

        ttk.Button(
            sidebar,
            text="▶   Start",
            style="Accent.TButton",
            command=self.start,
        ).pack(fill="x", pady=5)
        ttk.Button(
            sidebar,
            text="Ⅱ   Pause",
            style="Subtle.TButton",
            command=self.pause,
        ).pack(fill="x", pady=5)
        tk.Label(
            sidebar,
            text="VISUALIZATION",
            font=("Segoe UI", 9, "bold"),
            fg=self.MUTED,
            bg=self.PANEL,
        ).pack(anchor="w", pady=(18, 5))
        self.mode = tk.StringVar(value="Wave + Orbit")
        self.mode_menu = ttk.Combobox(
            sidebar,
            textvariable=self.mode,
            values=("Wave + Orbit", "Waveform", "Orbit"),
            state="readonly",
            style="Mode.TCombobox",
        )
        self.mode_menu.pack(fill="x", pady=5)
        self.mode_menu.bind("<<ComboboxSelected>>", self._change_mode)

        speed_header = tk.Frame(sidebar, bg=self.PANEL)
        speed_header.pack(fill="x", pady=(18, 0))
        tk.Label(
            speed_header,
            text="ANIMATION SPEED",
            font=("Segoe UI", 9, "bold"),
            fg=self.MUTED,
            bg=self.PANEL,
        ).pack(side="left")
        self.speed = tk.DoubleVar(value=1.0)
        self.speed_value = tk.Label(
            speed_header,
            text="1.0×",
            font=("Segoe UI", 9),
            fg=self.TEXT,
            bg=self.PANEL,
        )
        self.speed_value.pack(side="right")
        tk.Scale(
            sidebar,
            variable=self.speed,
            from_=0.25,
            to=2.5,
            resolution=0.05,
            orient="horizontal",
            showvalue=False,
            command=self._change_speed,
            bg=self.PANEL,
            fg=self.TEXT,
            troughcolor="#292e3e",
            activebackground=self.ACCENT,
            highlightthickness=0,
            sliderlength=16,
            bd=0,
        ).pack(fill="x", pady=(2, 5))

        self.status = tk.Label(
            sidebar,
            text="●  PLAYING",
            font=("Segoe UI", 9, "bold"),
            fg=self.CYAN,
            bg=self.PANEL,
        )
        self.status.pack(anchor="w", side="bottom")

        self.canvas = tk.Canvas(
            self.root,
            background=self.BACKGROUND,
            highlightthickness=0,
        )
        self.canvas.grid(row=0, column=1, sticky="nsew", padx=24, pady=24)
        self.canvas.bind("<Configure>", lambda _event: self._draw_visualizer())

    def _draw_visualizer(self):
        if not hasattr(self, "canvas"):
            return

        canvas = self.canvas
        canvas.delete("all")
        width = max(canvas.winfo_width(), 1)
        height = max(canvas.winfo_height(), 1)
        center_x, center_y = width / 2, height / 2
        radius = min(width, height) * 0.27

        for ring_radius, color in (
            (radius * 1.7, "#1c2231"),
            (radius * 1.35, "#242a3b"),
            (radius * 0.92, "#292d43"),
        ):
            canvas.create_oval(
                center_x - ring_radius,
                center_y - ring_radius,
                center_x + ring_radius,
                center_y + ring_radius,
                outline=color,
                width=1,
            )

        if self.mode.get() in ("Wave + Orbit", "Waveform"):
            points = []
            for index in range(121):
                x = width * 0.12 + width * 0.76 * index / 120
                offset = index / 120 * math.tau
                envelope = math.sin(math.pi * index / 120) ** 0.55
                y = center_y + math.sin(offset * 2.2 + self.phase) * radius * 0.38 * envelope
                y += math.sin(offset * 5.1 - self.phase * 0.7) * radius * 0.12 * envelope
                points.extend((x, y))
            canvas.create_line(*points, fill=self.ACCENT, width=3, smooth=True)

        if self.mode.get() in ("Wave + Orbit", "Orbit"):
            orbit_radius = radius * 0.72
            for index in range(8):
                angle = self.phase * 0.65 + index * math.tau / 8
                x = center_x + math.cos(angle) * orbit_radius
                y = center_y + math.sin(angle) * orbit_radius
                size = 4 + 2 * (1 + math.sin(self.phase + index)) / 2
                canvas.create_oval(
                    x - size,
                    y - size,
                    x + size,
                    y + size,
                    fill=self.CYAN if index % 2 == 0 else "#bd8aff",
                    outline="",
                )

        glow = 15 + 4 * math.sin(self.phase * 1.4)
        canvas.create_oval(
            center_x - glow,
            center_y - glow,
            center_x + glow,
            center_y + glow,
            fill=self.CYAN,
            outline="",
        )
        canvas.create_text(
            center_x,
            center_y + radius * 1.8,
            text=self.mode.get().upper(),
            fill=self.MUTED,
            font=("Segoe UI", 9, "bold"),
        )

    def _animate(self):
        if not self.running:
            self.after_id = None
            return

        self.phase += 0.07 * self.speed.get()
        self._draw_visualizer()
        self.after_id = self.root.after(33, self._animate)

    def start(self):
        if self.running:
            return
        self.running = True
        self.status.configure(text="●  PLAYING", fg=self.CYAN)
        self._animate()

    def pause(self):
        if not self.running:
            return
        self.running = False
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.status.configure(text="●  PAUSED", fg="#f1bd6c")

    def _change_mode(self, _event=None):
        self._draw_visualizer()

    def _change_speed(self, value):
        self.speed_value.configure(text=f"{float(value):.1f}×")

    def _close(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
        self.root.destroy()


if __name__ == "__main__":
    window = tk.Tk()
    AudioLabApp(window)
    window.mainloop()
