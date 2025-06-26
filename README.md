
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

* 📂 `screenshots/` → Individual PNG screenshots of each terminal event
* 📂 `gifs/` → Animated GIFs containing N screenshots per GIF
* 📄 `command_log.txt` → Plain-text log of all typed commands

---

## 🛠️ Installation

1. Clone or download the repository:

```bash
git clone https://github.com/AbdouAmmari/wincap
cd wincap
```

2. Install dependencies:

**For Linux:**
```bash
pip install pyscreenshot python-xlib psutil pillow keyboard
# Also ensure X11 development libraries are installed:
# Ubuntu/Debian: sudo apt-get install python3-dev libx11-dev
# Fedora/RHEL: sudo dnf install python3-devel libX11-devel
```

**For Windows:**
```bash
pip install pywinauto pygetwindow pillow keyboard
```

**Common dependencies:**
```bash
pip install pillow keyboard
```

## Usage

The usage is identical on both platforms:

```bash
python window_monitor.py
```

The script will:
1. Detect your operating system
2. Load appropriate platform-specific modules
3. Show available windows with their dimensions
4. Allow you to select and monitor any window
5. Capture screenshots and create GIFs based on keyboard activity

This version maintains all the advanced features from the previous version while adding full Linux compatibility through X11 integration.

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

