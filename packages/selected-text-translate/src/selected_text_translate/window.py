"""Tkinter window and asynchronous request handling for translations."""

from __future__ import annotations

import queue
import re
import socket
import threading

from .engines import TRANSLATORS
from .instance import start_message_server


def run_window(initial_text: str, server: socket.socket, default_engine: str = "Google Translate") -> None:
    import tkinter as tk
    from tkinter import ttk
    from tkinter.scrolledtext import ScrolledText

    root = tk.Tk()
    root.title("Translate selected text")
    root.geometry("760x600")

    toolbar = ttk.Frame(root, padding=(12, 10))
    toolbar.pack(fill="x")
    ttk.Label(toolbar, text="Translation engine:").pack(side="left")
    if default_engine not in TRANSLATORS:
        raise ValueError(f"Unknown translation engine: {default_engine}")
    engine_var = tk.StringVar(value=default_engine)
    selector = ttk.Combobox(
        toolbar,
        textvariable=engine_var,
        values=tuple(TRANSLATORS),
        state="readonly",
        width=20,
    )
    selector.pack(side="left", padx=(8, 0))

    content = ScrolledText(root, wrap="word", padx=16, pady=12, font=("Segoe UI", 11))
    content.pack(fill="both", expand=True)
    content.tag_configure("heading", font=("Segoe UI", 11, "bold"), foreground="#1769aa")
    content.tag_configure("error", foreground="#aa2222")

    updates: queue.Queue[str] = queue.Queue()
    results: queue.Queue[tuple[int, str, str, str | None]] = queue.Queue()
    request_number = 0
    active_text = ""

    def render(
        source: str,
        translation: str | None = None,
        error: str | None = None,
        engine: str | None = None,
    ) -> None:
        content.configure(state="normal")
        content.delete("1.0", "end")
        content.insert("end", "Selected text\n", "heading")
        content.insert("end", source + "\n\n")
        content.insert("end", f"Korean translation - {engine or engine_var.get()}\n", "heading")
        if error:
            content.insert("end", error + "\n", "error")
        elif translation is None:
            content.insert("end", "Translating...\n")
        else:
            content.insert("end", translation + "\n")
        content.configure(state="disabled")

    def translate(source: str) -> None:
        nonlocal request_number, active_text
        active_text = source
        request_number += 1
        request_id = request_number
        engine_name = engine_var.get()
        translator = TRANSLATORS[engine_name]
        root.title(f"Translate selected text - {engine_name}")
        render(source, engine=engine_name)
        root.deiconify()
        root.lift()
        root.focus_force()

        def worker() -> None:
            try:
                results.put((request_id, source, translator.translate(source), None))
            except Exception as exc:
                results.put((request_id, source, "", str(exc)))

        threading.Thread(target=worker, daemon=True).start()

    def change_engine(_event: object) -> None:
        if active_text.strip():
            translate(active_text)

    def poll() -> None:
        while True:
            try:
                source = updates.get_nowait()
            except queue.Empty:
                break
            translate(re.sub(r"\s+", " ", source).strip())

        while True:
            try:
                request_id, source, translation, error = results.get_nowait()
            except queue.Empty:
                break
            if request_id == request_number:
                render(source, translation, error)
        root.after(100, poll)

    selector.bind("<<ComboboxSelected>>", change_engine)
    start_message_server(server, "text", updates.put)
    translate(initial_text)
    poll()
    root.mainloop()
