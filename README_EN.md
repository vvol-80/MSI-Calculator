# MSI Calculator 4.3 (Tkinter)

Language: English (alternative README)  
Original project: `msi_calc_4_3.pyw`

A small Windows-style calculator clone written in **Python + Tkinter**, using a **skinned UI image** (MSI-like look) with clickable regions and keyboard input.

## Features

- GUI calculator (no CLI)
- Basic arithmetic: `+`, `-`, `*`, `/`
- Percent operation (`%`)
- Square root (`√`)
- Sign toggle (`+/-`)
- Backspace/delete last digit
- Clear entry (CE) and all clear (AC)
- Keyboard support (including numpad operators)
- Clipboard shortcuts:
  - Copy: `Ctrl+C`
  - Paste: `Ctrl+V` (digits and `.`/`-` are kept; other characters are ignored)
- Packaged-app friendly: supports loading assets when bundled with **PyInstaller** (`sys._MEIPASS`)

## Requirements

- Windows 10/11 (recommended; other OSes may work if Tkinter is available)
- Python 3.x with Tkinter (usually included with the standard Windows installer)
- Runtime asset (UI skin image):
  - Preferred: `msi_calculator471.png` placed next to `msi_calc_4_3.pyw`
  - Fallback attempt (current working directory): `msi_calculator471_3.png`

## Installation

### Option A — Run from source (recommended)

1. Install Python 3 from https://www.python.org/downloads/windows/
2. Download/clone this repository.
3. Ensure the image file is present:
   - Put `msi_calculator471.png` in the same folder as `msi_calc_4_3.pyw`.

No third‑party libraries are required.

### Option B — (Optional) Package to EXE with PyInstaller

If you want a single-folder app:

```bat
pip install pyinstaller
pyinstaller --noconsole --onefile --add-data "msi_calculator471.png;." msi_calc_4_3.pyw
```

Notes:
- The script checks `sys.frozen` and will load the image from `sys._MEIPASS` when bundled.
- Adjust the `--add-data` separator if you build on non-Windows.

## How to Run (Windows)

From File Explorer:
- Double-click `msi_calc_4_3.pyw`.

From Command Prompt / PowerShell:

```bat
cd /d "D:\Program Files\msi_calc\msi_calc_res"
python msi_calc_4_3.pyw
```

If `python` is not found, try:

```bat
py msi_calc_4_3.pyw
```

## Usage

### Mouse

- Click the calculator buttons on the skinned UI.
- The clickable areas are implemented as transparent rectangles on a Tkinter `Canvas`.

### Keyboard

- Digits: `0`–`9`
- Decimal point: `.`
- Operators: `+` `-` `*` `/` (works with main keyboard and numpad)
- Evaluate: `Enter`
- All clear: `Esc`
- Clear entry: `Delete`
- Backspace: `Backspace`
- Square root: press the `s` key (as implemented in the script)
- Percent: `%`

### Usage examples

You can type expressions step-by-step (like on a normal calculator):

- `12` `+` `7` `Enter` → `19`
- `50` `%` → `0.5` (or if there is a previous operand/operator, it calculates a percentage of the previous value)
- `9` `s` → `3` (square root)

Clipboard examples:

- `Ctrl+C` copies the current displayed number.
- `Ctrl+V` pastes a number; only characters in `0123456789.-` are kept.

## Configuration

No configuration file and no command-line options.

Behavior is controlled directly in the script, including:

- Window size: `412x471`
- Image filename(s): `msi_calculator471.png` (preferred) and `msi_calculator471_3.png` (fallback)
- Display formatting and max display length (~13 characters)

## Troubleshooting / FAQ

### The calculator opens with a gray background / no skin image

- Ensure `msi_calculator471.png` is in the same folder as `msi_calc_4_3.pyw`.
- The script prints the attempted image path to the console. If you run by double-clicking `.pyw`, you won’t see console output—run from `cmd`/PowerShell to view messages.
- As a fallback, the script tries `msi_calculator471_3.png` in the **current working directory**.

### Nothing happens when I press some keys

- Some keys are intentionally ignored (Ctrl/Alt/Shift).
- Operators are handled by `keysym` to work across keyboard layouts; use `+ - * /` or numpad operator keys.
- Square root is bound to the `s` key in the current version.

### I get `Error` on the display

Common reasons:
- Division by zero
- Invalid expression state
- Square root of a negative number

Press `Esc` (AC) to reset.

### Does it save history or write files?

No. All calculations are in-memory only.

## Security note

The app uses Python’s `eval()` internally to evaluate the expression it builds from button/key inputs. In normal use this is constrained to calculator input, but you should avoid pasting untrusted text into the app.

## License

TODO: MIT License.

