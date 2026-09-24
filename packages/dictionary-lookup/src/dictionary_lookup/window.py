"""Tkinter window for dictionary definitions."""

from __future__ import annotations

import queue
import re
import socket
import threading

from .engines import ENGINES
from .instance import start_message_server
from .lookup import LookupResult, lookup_all_lemmas
from .text import trim


def run_window(initial_word: str, server: socket.socket, default_engine: str = "Oxford") -> None:
    import tkinter as tk
    from tkinter import ttk
    from tkinter.scrolledtext import ScrolledText

    root = tk.Tk()
    root.geometry("620x460")
    toolbar = ttk.Frame(root, padding=(8, 6))
    toolbar.pack(fill="x")
    ttk.Label(toolbar, text="Dictionary:").pack(side="left")
    if default_engine not in ENGINES:
        raise ValueError(f"Unknown dictionary engine: {default_engine}")
    selected_engine = tk.StringVar(value=default_engine)
    selector = ttk.Combobox(
        toolbar,
        textvariable=selected_engine,
        values=tuple(ENGINES),
        state="readonly",
        width=16,
    )
    selector.pack(side="left", padx=(6, 0))

    text = ScrolledText(root, wrap="word", padx=16, pady=12, font=("Segoe UI", 11))
    text.pack(fill="both", expand=True)
    text.tag_configure("title", font=("Segoe UI", 18, "bold"), foreground="#1769aa")
    text.tag_configure("error", foreground="#aa2222")
    updates: queue.Queue[str] = queue.Queue()
    result_queue: queue.Queue[tuple[int, str, str, LookupResult | None, str | None]] = queue.Queue()
    current_request = 0
    current_word = ""

    def dictionary_heading(engine_name: str) -> str:
        return "Oxford Advanced Learner's Dictionary" if engine_name == "Oxford" else "Naver English Dictionary"

    def show_word(word: str) -> None:
        nonlocal current_request, current_word
        current_word = word
        current_request += 1
        request_id = current_request
        engine = ENGINES[selected_engine.get()]
        root.title(f"{engine.window_title}: {word}")
        text.configure(state="normal")
        text.delete("1.0", "end")
        text.insert("end", word + "\n", "title")
        text.insert("end", f"{dictionary_heading(engine.name)}\n\nLooking up...\n")
        text.configure(state="disabled")
        root.deiconify()
        root.lift()
        root.focus_force()

        def fetch() -> None:
            try:
                result_queue.put((request_id, word, engine.name, lookup_all_lemmas(engine, word), None))
            except Exception as exc:
                result_queue.put((request_id, word, engine.name, None, f"Could not search {engine.name}: {exc}"))

        threading.Thread(target=fetch, daemon=True).start()

    def render_results() -> None:
        while True:
            try:
                request_id, word, engine_name, result, error = result_queue.get_nowait()
            except queue.Empty:
                return
            if request_id != current_request:
                continue
            text.configure(state="normal")
            text.delete("1.0", "end")
            text.insert("end", word + "\n", "title")
            text.insert("end", f"{dictionary_heading(engine_name)}\n\n")
            if error:
                text.insert("end", error + "\n", "error")
            elif result and result.matches:
                number = 0
                for match in result.matches:
                    if match.searched_word != word:
                        text.insert("end", f"Results for {match.searched_word}:\n", "title")
                    for definition in match.definitions:
                        number += 1
                        text.insert("end", f"{number}. {definition}\n\n")
            elif engine_name == "Oxford":
                text.insert("end", "No definition was found on the Oxford entry page.\n")
            else:
                text.insert("end", "No definition was found on the Naver English Dictionary search page.\n")
            text.configure(state="disabled")

    def change_engine(_event: object) -> None:
        if current_word:
            show_word(current_word)

    def poll() -> None:
        while True:
            try:
                word = updates.get_nowait()
            except queue.Empty:
                break
            word = trim(re.sub(r"\s+", " ", word))
            if word:
                show_word(word)
        render_results()
        root.after(100, poll)

    selector.bind("<<ComboboxSelected>>", change_engine)
    start_message_server(server, "word", updates.put)
    show_word(initial_word)
    poll()
    root.mainloop()
