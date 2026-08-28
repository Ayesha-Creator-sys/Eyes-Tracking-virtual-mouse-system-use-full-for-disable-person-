"""
EyeMouse AI Ultra - Main Entry Point
Designed to run as a standalone Windows .exe with no console.
Double-click to launch -> Auth -> Eye Tracking starts automatically.
"""
import sys
import os
import logging

# ── Redirect stdout/stderr in frozen mode (no console window) ────────────────
if getattr(sys, 'frozen', False):
    # Running as a PyInstaller bundle — redirect logs to a file
    app_data = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'EyeMouseUltra')
    os.makedirs(app_data, exist_ok=True)
    log_path = os.path.join(app_data, 'system_log.txt')
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )
    # Suppress any print() calls from crashing the no-console exe
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
else:
    # Development mode — log to both file and console
    logging.basicConfig(
        filename='system_log.txt',
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )

# ── Fix working directory for PyInstaller ───────────────────────────────────
if getattr(sys, 'frozen', False):
    # When frozen, _MEIPASS is the temp folder. We keep cwd as the exe dir.
    os.chdir(os.path.dirname(sys.executable))

# ── Add project root to path ─────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Prevent duplicate instances ──────────────────────────────────────────────
import threading
from utilities.auto_shortcut import ensure_shortcut_on_startup

_LOCK_FILE = os.path.join(
    os.environ.get('APPDATA', os.path.expanduser('~')),
    'EyeMouseUltra', 'app.lock'
)

def _acquire_lock():
    """Returns True if this is the first instance. False if already running."""
    try:
        import msvcrt, atexit
        lock_dir = os.path.dirname(_LOCK_FILE)
        os.makedirs(lock_dir, exist_ok=True)
        _lf = open(_LOCK_FILE, 'w')
        msvcrt.locking(_lf.fileno(), msvcrt.LK_NBLCK, 1)
        atexit.register(lambda: _lf.close())
        return True
    except Exception:
        return False

# ── Main Launch ──────────────────────────────────────────────────────────────
def launch_main_app():
    """Called after successful authentication — opens the main tracking window."""
    try:
        from gui.app import VirtualMouseApp
        app = VirtualMouseApp()
        app.mainloop()
    except Exception as e:
        logging.critical(f"Main App crashed: {e}", exc_info=True)


def main():
    # Check for duplicate instance
    if not _acquire_lock():
        # Bring existing window to front instead of opening a second one
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(
                0,
                "EyeMouse AI is already running.\nCheck your system tray.",
                "EyeMouse AI",
                0x40  # MB_ICONINFORMATION
            )
        except Exception:
            pass
        return

    # ── Auto-create desktop shortcut on first launch ──────────────────────────
    ensure_shortcut_on_startup()

    try:
        from gui.auth_window import AuthWindow
        from security.auth_manager import AuthenticationManager

        # Pre-initialise the auth manager (creates DB/key if first run)
        AuthenticationManager()

        # Open the secure gatekeeper window
        gatekeeper = AuthWindow(launch_main_app)
        gatekeeper.mainloop()

    except Exception as e:
        logging.critical(f"Startup failed: {e}", exc_info=True)
        # Show a user-friendly error if something goes wrong
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(
                0,
                f"EyeMouse AI failed to start.\n\nError: {e}\n\nCheck system_log.txt for details.",
                "EyeMouse AI - Startup Error",
                0x10  # MB_ICONERROR
            )
        except Exception:
            pass


if __name__ == "__main__":
    main()
