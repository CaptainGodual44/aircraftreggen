# Aircraft Registration Generator

A simple Python tool that generates random aircraft registration numbers based on country.

It supports both:
- **CLI mode** for terminal usage
- **GUI mode** using Tkinter for a desktop interface

## Supported Countries

- United States (`us`, `usa`, `united states`)
- Canada (`canada`)
- United Kingdom (`uk`, `united kingdom`)
- Germany (`germany`)
- France (`france`)
- Australia (`australia`)
- Japan (`japan`)

## CLI Usage

```bash
python3 aircraft_registration.py "us"
python3 aircraft_registration.py "canada" --count 3
```

## GUI Usage

```bash
python3 aircraft_registration.py --gui
```

In GUI mode:
1. Select a country from the dropdown.
2. Choose how many registrations to generate.
3. Click **Generate** to view results.

## Example CLI Output

```text
Country: United States
Generated registration(s):
- N4812Q
- N92
```
