# 🖼️ WinCap – Cross-Platform Screenshot Logger with Auto GIFs

**WinCap** is a powerful Python-based monitoring tool that automatically captures and documents terminal commands and their output across **Windows and Linux**. It intelligently listens for keyboard events, takes screenshots of your selected window at critical moments, and creates animated GIFs for easy sharing and review.

---

## 🚀 Features

✅ **Cross-Platform Support** – Works seamlessly on Windows and Linux  
✅ **Smart Window Selection** – Choose any visible window to monitor (terminals, IDEs, browsers, etc.)  
✅ **Intelligent Screenshot Timing** – Automatically captures:
* Screenshot when **Enter** is pressed (command executed)
* Screenshot when typing resumes (output captured)

✅ **Command Logging** – All typed commands saved with timestamps  
✅ **Automated GIF Creation** – Combines screenshots into animated GIFs  
✅ **Configurable Settings** – Customizable frames per GIF with persistent configuration  
✅ **Real-time Monitoring** – Live status updates and manual screenshot capability  
✅ **Professional Logging** – Comprehensive error handling and activity logging

---

## 🖥️ Platform Support

| Platform | Window Manager | Screenshot Method | Status |
|----------|----------------|-------------------|--------|
| **Windows** | pywinauto + pygetwindow | PIL ImageGrab | ✅ Fully Supported |
| **Linux** | X11 (python-xlib) | pyscreenshot | ✅ Fully Supported |
| **macOS** | - | - | ❌ Not yet supported |

---

## 📦 Output Structure

```
project/
├── screenshots/          # Individual PNG screenshots
│   ├── 20241226_143022_before_output.png
│   ├── 20241226_143025_after_output.png
│   └── 20241226_143030_manual.png
├── gifs/                 # Animated GIFs (N frames each)
│   ├── 20241226_143045.gif
│   └── 20241226_143102.gif
├── command_log.txt       # Timestamped command history
├── monitor.log           # Application logs
└── config.json           # Persistent settings
```

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AbdouAmmari/wincap
cd wincap
```

### 2. Install Platform-Specific Dependencies

**For Linux (X11 required):**
```bash
# Install Python packages
pip install pyscreenshot python-xlib psutil pillow keyboard

# Install system dependencies
# Ubuntu/Debian:
sudo apt-get install python3-dev libx11-dev

# Fedora/RHEL/CentOS:
sudo dnf install python3-devel libX11-devel

# Arch Linux:
sudo pacman -S python libx11
```

**For Windows:**
```bash
pip install pywinauto pygetwindow pillow keyboard
```

**Cross-Platform Dependencies:**
```bash
pip install pillow keyboard
```

### 3. Verify Installation

```bash
python crosscap.py
```

---

## 🖥️ Usage

### Basic Usage

```bash
python wincap.py
```

### Step-by-Step Process

1. **Platform Detection** – Automatically detects Windows or Linux
2. **Window Selection** – Choose from available windows with size information
3. **Configuration** – Set GIF frame count (saves automatically)
4. **Monitoring** – Focus on selected window and start typing
5. **Screenshot Capture** – Automatic screenshots on Enter key and typing resume
6. **GIF Generation** – Automatic GIF creation after N screenshots
7. **Exit** – Press ESC to stop monitoring

### Hotkeys During Monitoring

| Key | Action |
|-----|--------|
| `ESC` | Stop monitoring and exit |
| `F1` | Display current status |
| `F2` | Take manual screenshot |

---

## 🔧 Configuration

Settings are automatically saved in `config.json`:

```json
{
  "gif_frame_count": 10,
  "platform": "Linux",
  "last_updated": "2024-12-26T14:30:22.123456"
}
```

**Configurable Options:**
- GIF frame count (1-50 screenshots per GIF)
- Settings persist between sessions
- Platform-specific optimizations

---

## 🎯 Use Cases

### Development & DevOps
- Document deployment processes
- Capture build and test sequences
- Create visual CI/CD documentation

### Security & Testing
- Record penetration testing sessions
- Document vulnerability analysis
- Create proof-of-concept demonstrations

### Training & Tutorials
- Generate step-by-step command tutorials
- Create animated documentation
- Share workflow demonstrations

### Debugging & Support
- Capture error reproduction steps
- Document troubleshooting processes
- Visual debugging timelines

---

## 📝 Example Workflow

**Command Execution:**
```bash
$ nmap -sV 192.168.1.0/24
Starting Nmap 7.80 ( https://nmap.org )
[... scan results ...]
Nmap done: 256 IP addresses scanned
```

**CrossCap Process:**
1. 📸 Screenshot taken when `Enter` pressed
2. ⏳ Waits for command completion
3. 📸 Screenshot taken when you start typing next command
4. 🎞️ After 10 screenshots → Automatic GIF creation
5. 📝 Command logged with timestamp

---

## 🐧 Linux-Specific Notes

- **X11 Required** – Currently supports X11 display server only
- **Wayland Support** – Not yet implemented (X11 compatibility mode may work)
- **Permissions** – May require running with appropriate X11 permissions
- **Display Variables** – Ensure `DISPLAY` environment variable is set

---

## 🪟 Windows-Specific Notes

- **Administrator Rights** – Required for global keyboard hooks
- **Window Detection** – Uses Windows API for accurate window management
- **Compatibility** – Works with CMD, PowerShell, Windows Terminal, WSL

---

## 🔒 Security & Privacy

- **Local Processing** – All data remains on your machine
- **No Network Access** – Tool operates entirely offline
- **Sensitive Data** – Be cautious when monitoring windows with passwords/keys
- **Log Management** – Regularly review and clean command logs

---

## 🚀 Advanced Features

### Professional Logging
```python
# Comprehensive logging system
2024-12-26 14:30:22 - INFO - Screenshot saved: 20241226_143022_001.png
2024-12-26 14:30:25 - INFO - GIF created: 20241226_143025.gif (2.3MB)
```

### Threading & Performance
- Non-blocking GIF creation
- Optimized image processing
- Memory management for long sessions

### Error Recovery
- Graceful window loss handling
- Automatic screenshot optimization
- Platform-specific error recovery

---

## ⚠️ Limitations

- **macOS Support** – Not yet implemented
- **Wayland** – Linux Wayland compositor not supported
- **Remote Sessions** – May not work properly over SSH/RDP without display forwarding
- **Special Characters** – Complex keyboard layouts may need adjustment

---

## 🐛 Troubleshooting

### Linux Issues
```bash
# X11 connection issues
export DISPLAY=:0

# Permission issues
xhost +local:

# Missing dependencies
pip install --upgrade pyscreenshot python-xlib
```

### Windows Issues
```bash
# Run as Administrator for keyboard hooks
# Ensure pywinauto dependencies are installed
pip install --upgrade pywinauto pygetwindow
```

### Common Issues
- **No windows detected** – Ensure target windows are visible and named
- **Screenshots not saving** – Check directory permissions
- **Keyboard not responding** – Verify administrator/root permissions


---

## 📄 License

MIT License - Use responsibly and ethically.

---

**Made with ❤️ for developers, security professionals, and anyone who needs to document their command-line workflows visually.**
