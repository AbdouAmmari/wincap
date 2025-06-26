import os
import time
import datetime
from PIL import ImageGrab, Image
from pywinauto import Desktop
import keyboard
import pygetwindow as gw

SAVE_DIR = "screenshots"
GIF_DIR = "gifs"
LOG_FILE = "command_log.txt"
os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(GIF_DIR, exist_ok=True)

typed_buffer = []
selected_window = None
target_rect = None
selected_hwnd = None
awaiting_next_command = False
saved_screenshots = []
GIF_FRAME_COUNT = 10  

def select_window():
    global selected_window, target_rect, selected_hwnd

    windows = [
        w for w in Desktop(backend="win32").windows()
        if w.is_visible()
        and w.window_text().strip() != ""
        and w.rectangle().width() > 100
        and w.rectangle().height() > 100
    ]

    print("Visible windows:\n")
    for i, win in enumerate(windows):
        print(f"[{i}] {win.window_text().strip()}")

    while True:
        try:
            idx = int(input("\nSelect window number to monitor: "))
            selected_window = windows[idx]
            target_rect = selected_window.rectangle()
            selected_hwnd = selected_window.handle
            print(f"[*] Monitoring: {selected_window.window_text()}")
            break
        except (ValueError, IndexError):
            print("Invalid selection. Try again.")

def take_screenshot(tag=""):
    global saved_screenshots

    rect = target_rect
    img = ImageGrab.grab(bbox=(rect.left, rect.top, rect.right, rect.bottom))
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(SAVE_DIR, f"{timestamp}{tag}.png")
    img.save(filename)
    saved_screenshots.append(filename)
    print(f"[+] Screenshot saved: {filename}")

    
    if len(saved_screenshots) >= GIF_FRAME_COUNT:
        make_gif(saved_screenshots[-GIF_FRAME_COUNT:])

def make_gif(frame_paths):
    frames = [Image.open(p).convert("RGB") for p in frame_paths]
    gif_name = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".gif"
    gif_path = os.path.join(GIF_DIR, gif_name)
    
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=700,  
        loop=0
    )
    print(f"[🎞️] GIF created: {gif_path}")

def on_key(event):
    global typed_buffer, awaiting_next_command

    active_win = gw.getActiveWindow()
    if active_win is None or active_win._hWnd != selected_hwnd:
        return

    if event.name == 'enter':
        command = ''.join(typed_buffer).strip()
        if command:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"{datetime.datetime.now()} - {command}\n")
            print(f"[LOG] Command: {command}")
        typed_buffer = []

        take_screenshot("_before_output")
        awaiting_next_command = True

    elif event.name == 'backspace' and typed_buffer:
        typed_buffer.pop()
    elif len(event.name) == 1:
        typed_buffer.append(event.name)
        if awaiting_next_command:
            time.sleep(0.3)
            take_screenshot("_after_output")
            awaiting_next_command = False
    elif event.name == 'space':
        typed_buffer.append(' ')

def main():
    global GIF_FRAME_COUNT

    select_window()
    user_input = input(f"[*] Enter number of screenshots per GIF (default {GIF_FRAME_COUNT}): ").strip()
    if user_input.isdigit():
        GIF_FRAME_COUNT = int(user_input)
        print(f"[*] Will generate a GIF after every {GIF_FRAME_COUNT} screenshots.")

    print("[*] Listening for keyboard input. Press ESC to quit.")
    keyboard.on_press(on_key)
    keyboard.wait('esc')

if __name__ == "__main__":
    main()
