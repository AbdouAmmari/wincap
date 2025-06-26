
# 🖼️ WinCap – Terminal Screenshot Logger with Auto GIFs

**WinCap** is a Python-based monitoring tool that helps you automatically capture and document terminal commands and their output. It listens for keyboard events, takes screenshots of your terminal window at critical points, and bundles them into animated GIFs for easy sharing and review.

---

## 🚀 Features

✅ Select a visible window to monitor (e.g., Command Prompt, PowerShell, Bash, etc.)
✅ Automatically detect when the **Enter** key is pressed inside that window
✅ Take **two screenshots per command**:

* One right after pressing `Enter` (command executed)
* One when typing begins again (output assumed complete)

✅ Save typed commands in a log file
✅ Combine screenshots into animated **GIFs** (every N screenshots)
✅ Customizable number of frames per GIF

---

## 📦 Output

* 📂 `screenshots_on_enter/` → Individual PNG screenshots of each terminal event
* 📂 `gifs/` → Animated GIFs containing N screenshots per GIF
* 📄 `command_log.txt` → Plain-text log of all typed commands

---

## 🛠️ Installation

1. Clone or download the repository:

```bash
git clone https://github.com/AbdouAmmari/wincap
cd termshot
```

2. Install dependencies:

```bash
pip install pillow pywinauto pygetwindow keyboard
```

> 🔒 On Windows, **run as Administrator** to allow global keyboard hooks.

---

## 🖥️ Usage

```bash
python WinCap.py
```

1. Select the terminal window you want to monitor from the list.
2. Optionally enter how many screenshots you want per GIF (default: 10).
3. Press `Enter` in the terminal — it will take the first screenshot.
4. When you begin typing the next command, the second screenshot is taken.
5. GIFs are created automatically after N screenshots.
6. Press `ESC` to stop the tool.

---

## 🎯 Ideal Use Cases

* Capture demos or command-line tutorials
* Generate visual logs of pentest sessions or security analysis
* Debug command outputs with a visual timeline
* Review or share CLI workflows in a portable format (GIF)

---

## 📝 Example

You run a command:

```bash
nmap -sV 192.168.1.1
```

WinCap will:

1. Save a screenshot when `Enter` is pressed.
2. Wait until you start typing the next command.
3. Save another screenshot (assumed to contain the output).
4. After 10 screenshots, generate an animated GIF showing the process.

---

## ⚠️ Notes

* Works on **Windows only** (uses `pywinauto` for accurate window bounds).
* Must be run in a terminal with a **visible and named** window (like CMD, PowerShell, Windows Terminal).
* Run as admin to allow key hooks (`keyboard` library requires this on Windows).
* Supports simple typed input; special characters may not always be recorded perfectly.

---


## 📃 License

MIT License. Use responsibly and ethically.

---

