#!/usr/bin/env python3
"""Simple aircraft registration generator by country with CLI + GUI."""

from __future__ import annotations

import argparse
import random
import string
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable


def _letters(count: int) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=count))


def _digits(count: int) -> str:
    return "".join(random.choices(string.digits, k=count))


def _us() -> str:
    # Simplified fixed-length N-number: 5 total characters.
    # Example format: N1234
    return f"N{_digits(4)}"


def _canada() -> str:
    return f"C-F{_letters(3)}"


def _uk() -> str:
    return f"G-{_letters(4)}"


def _germany() -> str:
    return f"D-{_letters(4)}"


def _france() -> str:
    return f"F-{_letters(4)}"


def _australia() -> str:
    return f"VH-{_letters(3)}"


def _japan() -> str:
    return f"JA{_digits(4)}"


COUNTRY_PATTERNS: dict[str, tuple[str, Callable[[], str]]] = {
    "us": ("United States", _us),
    "usa": ("United States", _us),
    "united states": ("United States", _us),
    "canada": ("Canada", _canada),
    "uk": ("United Kingdom", _uk),
    "united kingdom": ("United Kingdom", _uk),
    "germany": ("Germany", _germany),
    "france": ("France", _france),
    "australia": ("Australia", _australia),
    "japan": ("Japan", _japan),
}

CANONICAL_COUNTRIES = sorted({name for name, _ in COUNTRY_PATTERNS.values()})


def generate_registration(country: str) -> str:
    """Generate a random aircraft registration for the given country."""
    key = country.strip().lower()
    if key not in COUNTRY_PATTERNS:
        supported = ", ".join(CANONICAL_COUNTRIES)
        raise ValueError(f"Unsupported country '{country}'. Supported countries: {supported}")

    _, generator = COUNTRY_PATTERNS[key]
    return generator()


def _aliases_for(canonical_country: str) -> list[str]:
    aliases: list[str] = []
    for alias, (name, _) in COUNTRY_PATTERNS.items():
        if name == canonical_country:
            aliases.append(alias)
    return aliases


def generate_many(country: str, count: int) -> list[str]:
    if count < 1:
        raise ValueError("count must be at least 1")
    return [generate_registration(country) for _ in range(count)]


def run_gui() -> None:
    root = tk.Tk()
    root.title("Aircraft Registration Generator")
    root.geometry("520x380")

    frame = ttk.Frame(root, padding=16)
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text="Country:").grid(row=0, column=0, sticky="w", pady=(0, 8))
    country_var = tk.StringVar(value="United States")
    country_combo = ttk.Combobox(
        frame,
        textvariable=country_var,
        values=CANONICAL_COUNTRIES,
        state="readonly",
        width=32,
    )
    country_combo.grid(row=0, column=1, sticky="ew", pady=(0, 8))

    ttk.Label(frame, text="Count:").grid(row=1, column=0, sticky="w", pady=(0, 8))
    count_var = tk.IntVar(value=1)
    count_spin = ttk.Spinbox(frame, from_=1, to=100, textvariable=count_var, width=8)
    count_spin.grid(row=1, column=1, sticky="w", pady=(0, 8))

    output = tk.Text(frame, height=14, wrap="word", state="disabled")
    output.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(8, 0))

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=output.yview)
    scrollbar.grid(row=3, column=2, sticky="ns", pady=(8, 0))
    output.configure(yscrollcommand=scrollbar.set)

    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(3, weight=1)

    def on_generate() -> None:
        canonical = country_var.get()
        aliases = _aliases_for(canonical)
        if not aliases:
            messagebox.showerror("Error", f"No country mapping found for {canonical}")
            return

        selected_alias = aliases[0]
        try:
            registrations = generate_many(selected_alias, count_var.get())
        except ValueError as exc:
            messagebox.showerror("Error", str(exc))
            return

        output.configure(state="normal")
        output.delete("1.0", tk.END)
        output.insert(tk.END, f"Country: {canonical}\n")
        output.insert(tk.END, "Generated registration(s):\n")
        for reg in registrations:
            output.insert(tk.END, f"- {reg}\n")
        output.configure(state="disabled")

    ttk.Button(frame, text="Generate", command=on_generate).grid(row=2, column=0, columnspan=2, sticky="ew")

    root.mainloop()


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate random aircraft registration by country")
    parser.add_argument("country", nargs="?", help="Country name (e.g. US, Canada, UK, Germany)")
    parser.add_argument("-n", "--count", type=int, default=1, help="Number of registrations to generate")
    parser.add_argument("--gui", action="store_true", help="Launch a simple desktop GUI")
    args = parser.parse_args()

    if args.gui:
        run_gui()
        return 0

    if not args.country:
        parser.error("country is required unless --gui is used")

    if args.count < 1:
        parser.error("--count must be at least 1")

    canonical_name = COUNTRY_PATTERNS.get(args.country.strip().lower(), (args.country, None))[0]

    try:
        registrations = generate_many(args.country, args.count)
    except ValueError as exc:
        print(exc)
        return 1

    print(f"Country: {canonical_name}")
    print("Generated registration(s):")
    for reg in registrations:
        print(f"- {reg}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
