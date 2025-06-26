import os
import sys
import time
import datetime
import threading
import platform
from pathlib import Path
from PIL import ImageGrab, Image
import keyboard
import json
from typing import List, Optional, Tuple, Dict, Any
import logging
import subprocess

# Platform-specific imports
if platform.system() == "Windows":
    from pywinauto import Desktop
    import pygetwindow as gw
elif platform.system() == "Linux":
    try:
        import pyscreenshot as ImageGrab_Linux
        import Xlib
        from Xlib import X, display
        from Xlib.protocol import request
        import psutil
    except ImportError as e:
        print(f"Linux dependencies missing. Install with: pip install pyscreenshot python-xlib psutil")
        sys.exit(1)

class CrossPlatformWindowManager:
    """Cross-platform window management abstraction."""
    
    def __init__(self):
        self.platform = platform.system()
        if self.platform == "Linux":
            try:
                self.display = display.Display()
                self.root = self.display.screen().root
            except Exception as e:
                logging.error(f"Could not connect to X11 display: {e}")
                raise
    
    def get_windows(self) -> List[Dict[str, Any]]:
        """Get list of visible windows across platforms."""
        if self.platform == "Windows":
            return self._get_windows_windows()
        elif self.platform == "Linux":
            return self._get_windows_linux()
        else:
            return []
    
    def _get_windows_windows(self) -> List[Dict[str, Any]]:
        """Get windows on Windows platform."""
        windows = []
        try:
            for w in Desktop(backend="win32").windows():
                try:
                    if (w.is_visible() and 
                        w.window_text().strip() and 
                        w.rectangle().width() > 100 and 
                        w.rectangle().height() > 100 and
                        not w.window_text().strip().startswith('Program Manager')):
                        
                        rect = w.rectangle()
                        windows.append({
                            'title': w.window_text().strip(),
                            'handle': w.handle,
                            'rect': (rect.left, rect.top, rect.right, rect.bottom),
                            'width': rect.width(),
                            'height': rect.height(),
                            'platform_obj': w
                        })
                except Exception:
                    continue
        except Exception as e:
            logging.error(f"Error getting Windows windows: {e}")
        return windows
    
    def _get_windows_linux(self) -> List[Dict[str, Any]]:
        """Get windows on Linux platform using X11."""
        windows = []
        try:
            # Get all windows
            window_ids = self.root.get_full_property(
                self.display.intern_atom('_NET_CLIENT_LIST'), 
                X.AnyPropertyType
            ).value
            
            for window_id in window_ids:
                try:
                    window = self.display.create_resource_object('window', window_id)
                    
                    # Get window attributes
                    attrs = window.get_attributes()
                    if attrs.map_state != X.IsViewable:
                        continue
                    
                    # Get window geometry
                    geom = window.get_geometry()
                    if geom.width < 100 or geom.height < 100:
                        continue
                    
                    # Get window title
                    try:
                        title_prop = window.get_full_property(
                            self.display.intern_atom('_NET_WM_NAME'), 
                            self.display.intern_atom('UTF8_STRING')
                        )
                        if title_prop:
                            title = title_prop.value.decode('utf-8')
                        else:
                            title_prop = window.get_full_property(
                                self.display.intern_atom('WM_NAME'), 
                                X.AnyPropertyType
                            )
                            title = title_prop.value.decode('utf-8') if title_prop else "Unknown"
                    except:
                        title = "Unknown"
                    
                    if not title.strip():
                        continue
                    
                    # Get absolute position
                    translated = window.translate_coords(self.root, 0, 0)
                    x, y = translated.x, translated.y
                    
                    windows.append({
                        'title': title.strip(),
                        'handle': window_id,
                        'rect': (x, y, x + geom.width, y + geom.height),
                        'width': geom.width,
                        'height': geom.height,
                        'platform_obj': window
                    })
                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            logging.error(f"Error getting Linux windows: {e}")
        
        return windows
    
    def get_active_window(self) -> Optional[int]:
        """Get currently active window handle."""
        if self.platform == "Windows":
            try:
                active_win = gw.getActiveWindow()
                return active_win._hWnd if active_win else None
            except:
                return None
        elif self.platform == "Linux":
            try:
                active_prop = self.root.get_full_property(
                    self.display.intern_atom('_NET_ACTIVE_WINDOW'), 
                    X.AnyPropertyType
                )
                return active_prop.value[0] if active_prop else None
            except:
                return None
        return None
    
    def take_window_screenshot(self, rect: Tuple[int, int, int, int]) -> Optional[Image.Image]:
        """Take screenshot of specific window area."""
        try:
            if self.platform == "Windows":
                return ImageGrab.grab(bbox=rect)
            elif self.platform == "Linux":
                return ImageGrab_Linux.grab(bbox=rect)
        except Exception as e:
            logging.error(f"Error taking screenshot: {e}")
            return None

class WindowMonitor:
    def __init__(self):
        self.SAVE_DIR = Path("screenshots")
        self.GIF_DIR = Path("gifs")
        self.LOG_FILE = Path("command_log.txt")
        self.CONFIG_FILE = Path("config.json")
        
        # Create directories
        self.SAVE_DIR.mkdir(exist_ok=True)
        self.GIF_DIR.mkdir(exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('monitor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize platform-specific window manager
        try:
            self.wm = CrossPlatformWindowManager()
        except Exception as e:
            self.logger.error(f"Failed to initialize window manager: {e}")
            sys.exit(1)
        
        # State variables
        self.typed_buffer = []
        self.selected_window = None
        self.target_rect = None
        self.selected_handle = None
        self.awaiting_next_command = False
        self.saved_screenshots = []
        self.gif_frame_count = 10
        self.is_monitoring = False
        self.screenshot_lock = threading.Lock()
        
        # Platform info
        self.platform = platform.system()
        self.logger.info(f"Running on {self.platform}")
        
        # Load configuration
        self.load_config()
    
    def load_config(self):
        """Load configuration from file if it exists."""
        try:
            if self.CONFIG_FILE.exists():
                with open(self.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    self.gif_frame_count = config.get('gif_frame_count', 10)
                    self.logger.info(f"Loaded config: GIF frame count = {self.gif_frame_count}")
        except Exception as e:
            self.logger.warning(f"Could not load config: {e}")
    
    def save_config(self):
        """Save current configuration to file."""
        try:
            config = {
                'gif_frame_count': self.gif_frame_count,
                'platform': self.platform,
                'last_updated': datetime.datetime.now().isoformat()
            }
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            self.logger.warning(f"Could not save config: {e}")
    
    def select_window(self) -> bool:
        """Select a window to monitor with cross-platform support."""
        windows = self.wm.get_windows()
        
        if not windows:
            print("No suitable windows found!")
            return False
        
        print(f"\n{'='*70}")
        print(f"Available windows on {self.platform}:")
        print(f"{'='*70}")
        
        for i, win in enumerate(windows):
            print(f"[{i:2d}] {win['title'][:50]:<50} ({win['width']}x{win['height']})")
        
        print(f"{'='*70}")
        
        while True:
            try:
                user_input = input("\nSelect window number to monitor (or 'q' to quit): ").strip()
                
                if user_input.lower() == 'q':
                    return False
                
                idx = int(user_input)
                if 0 <= idx < len(windows):
                    self.selected_window = windows[idx]
                    self.target_rect = self.selected_window['rect']
                    self.selected_handle = self.selected_window['handle']
                    
                    print(f"\n✓ Selected: {self.selected_window['title']}")
                    print(f"  Size: {self.selected_window['width']}x{self.selected_window['height']}")
                    print(f"  Position: ({self.target_rect[0]}, {self.target_rect[1]})")
                    return True
                else:
                    print("Invalid selection. Please try again.")
                    
            except ValueError:
                print("Please enter a valid number or 'q' to quit.")
            except Exception as e:
                self.logger.error(f"Error selecting window: {e}")
                print("An error occurred. Please try again.")
    
    def take_screenshot(self, tag: str = "") -> Optional[str]:
        """Take screenshot with cross-platform support."""
        try:
            with self.screenshot_lock:
                if not self.target_rect:
                    return None
                
                img = self.wm.take_window_screenshot(self.target_rect)
                if not img:
                    return None
                
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                filename = self.SAVE_DIR / f"{timestamp}{tag}.png"
                
                # Optimize image before saving
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                img.save(filename, optimize=True)
                self.saved_screenshots.append(str(filename))
                
                self.logger.info(f"Screenshot saved: {filename.name}")
                
                # Clean up old screenshots
                if len(self.saved_screenshots) > self.gif_frame_count * 3:
                    self.saved_screenshots = self.saved_screenshots[-self.gif_frame_count * 2:]
                
                # Create GIF if we have enough frames
                if len(self.saved_screenshots) >= self.gif_frame_count:
                    threading.Thread(
                        target=self.make_gif, 
                        args=(self.saved_screenshots[-self.gif_frame_count:],),
                        daemon=True
                    ).start()
                
                return str(filename)
                
        except Exception as e:
            self.logger.error(f"Error taking screenshot: {e}")
            return None
    
    def make_gif(self, frame_paths: List[str]):
        """Create GIF with optimization."""
        try:
            if not frame_paths:
                return
            
            frames = []
            for path in frame_paths:
                try:
                    if os.path.exists(path):
                        img = Image.open(path)
                        # Resize if too large
                        if img.width > 800 or img.height > 600:
                            img.thumbnail((800, 600), Image.Resampling.LANCZOS)
                        frames.append(img.convert("RGB"))
                except Exception as e:
                    self.logger.warning(f"Could not load frame {path}: {e}")
            
            if not frames:
                return
            
            gif_name = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.gif"
            gif_path = self.GIF_DIR / gif_name
            
            frames[0].save(
                gif_path,
                save_all=True,
                append_images=frames[1:],
                duration=500,
                loop=0,
                optimize=True
            )
            
            size_mb = gif_path.stat().st_size / (1024 * 1024)
            self.logger.info(f"🎞️  GIF created: {gif_name} ({size_mb:.1f}MB)")
            
        except Exception as e:
            self.logger.error(f"Error creating GIF: {e}")
    
    def log_command(self, command: str):
        """Log command with timestamp."""
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] {command}\n"
            
            with open(self.LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_entry)
                
            self.logger.info(f"Command logged: {command}")
            
        except Exception as e:
            self.logger.error(f"Error logging command: {e}")
    
    def on_key(self, event):
        """Cross-platform key event handler."""
        try:
            if not self.is_monitoring:
                return
            
            # Check if target window is active
            active_handle = self.wm.get_active_window()
            if not active_handle or active_handle != self.selected_handle:
                return
            
            if event.name == 'enter':
                command = ''.join(self.typed_buffer).strip()
                if command:
                    self.log_command(command)
                
                self.typed_buffer = []
                self.take_screenshot("_before_output")
                self.awaiting_next_command = True
            
            elif event.name == 'backspace':
                if self.typed_buffer:
                    self.typed_buffer.pop()
            
            elif event.name == 'space':
                self.typed_buffer.append(' ')
                if self.awaiting_next_command:
                    threading.Timer(0.5, lambda: self.take_screenshot("_after_output")).start()
                    self.awaiting_next_command = False
            
            elif len(event.name) == 1 and event.name.isprintable():
                self.typed_buffer.append(event.name)
                if self.awaiting_next_command:
                    threading.Timer(0.5, lambda: self.take_screenshot("_after_output")).start()
                    self.awaiting_next_command = False
            
        except Exception as e:
            self.logger.error(f"Error in key handler: {e}")
    
    def configure_settings(self):
        """Interactive configuration setup."""
        print(f"\n{'='*50}")
        print("Configuration Settings")
        print(f"{'='*50}")
        
        while True:
            try:
                user_input = input(f"GIF frame count (current: {self.gif_frame_count}): ").strip()
                if not user_input:
                    break
                
                frame_count = int(user_input)
                if 1 <= frame_count <= 50:
                    self.gif_frame_count = frame_count
                    break
                else:
                    print("Please enter a number between 1 and 50.")
            except ValueError:
                print("Please enter a valid number.")
        
        self.save_config()
        print(f"✓ Configuration saved. GIF will be created every {self.gif_frame_count} screenshots.")
    
    def display_status(self):
        """Display current monitoring status."""
        print(f"\n{'='*70}")
        print("CROSS-PLATFORM WINDOW MONITOR STATUS")
        print(f"{'='*70}")
        print(f"Platform: {self.platform}")
        print(f"Target Window: {self.selected_window['title'] if self.selected_window else 'None'}")
        print(f"Screenshots Taken: {len(self.saved_screenshots)}")
        print(f"GIF Frame Count: {self.gif_frame_count}")
        print(f"Monitoring: {'Active' if self.is_monitoring else 'Inactive'}")
        print(f"{'='*70}")
        print("Commands:")
        print("  ESC - Stop monitoring and exit")
        print("  F1  - Show this status")
        print("  F2  - Take manual screenshot")
        print(f"{'='*70}")
    
    def check_dependencies(self):
        """Check platform-specific dependencies."""
        missing = []
        
        if self.platform == "Linux":
            try:
                import pyscreenshot
                import Xlib
                import psutil
            except ImportError as e:
                missing.append("Linux: pip install pyscreenshot python-xlib psutil")
        
        elif self.platform == "Windows":
            try:
                import pywinauto
                import pygetwindow
            except ImportError as e:
                missing.append("Windows: pip install pywinauto pygetwindow")
        
        if missing:
            print("Missing dependencies:")
            for dep in missing:
                print(f"  - {dep}")
            return False
        return True
    
    def run(self):
        """Main execution loop with cross-platform support."""
        print("🔍 Cross-Platform Window Monitor v3.0")
        print(f"Running on {self.platform}")
        print("Captures screenshots and creates GIFs based on keyboard activity")
        
        # Check dependencies
        if not self.check_dependencies():
            sys.exit(1)
        
        try:
            # Window selection
            if not self.select_window():
                print("Exiting...")
                return
            
            # Configuration
            self.configure_settings()
            
            # Display status
            self.display_status()
            
            # Set up event handlers
            self.is_monitoring = True
            keyboard.on_press(self.on_key)
            
            # Additional hotkeys
            keyboard.add_hotkey('f1', self.display_status)
            keyboard.add_hotkey('f2', lambda: self.take_screenshot("_manual"))
            
            print(f"\n🚀 Monitoring started! Focus on '{self.selected_window['title']}' and start typing.")
            print("Press ESC to stop monitoring...")
            
            # Wait for ESC key
            keyboard.wait('esc')
            
        except KeyboardInterrupt:
            print("\n\nMonitoring interrupted by user.")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
        finally:
            self.is_monitoring = False
            print(f"\n✅ Monitoring stopped.")
            print(f"📁 Screenshots saved in: {self.SAVE_DIR.absolute()}")
            print(f"🎞️  GIFs saved in: {self.GIF_DIR.absolute()}")
            print(f"📝 Commands logged in: {self.LOG_FILE.absolute()}")

if __name__ == "__main__":
    monitor = WindowMonitor()
    monitor.run()
