"""
EyeMouse AI Ultra – One-Click Build Script
==========================================
Run this script ONCE to compile the entire project into a single .exe file.

Usage:
    python build_exe.py

Requirements (already in your venv):
    pip install pyinstaller
"""

import subprocess
import sys
import os
import shutil

# ── Configuration ─────────────────────────────────────────────────────────────
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SPEC_FILE   = os.path.join(PROJECT_DIR, "EyeMouse AI Ultra.spec")
DIST_DIR    = os.path.join(PROJECT_DIR, "dist")
BUILD_DIR   = os.path.join(PROJECT_DIR, "build")
EXE_NAME    = "EyeMouse AI Ultra"
ICON_FILE   = os.path.join(PROJECT_DIR, "app_icon.ico")

def banner(msg):
    print("\n" + "=" * 60)
    print(f"  {msg}")
    print("=" * 60)

def check_pyinstaller():
    banner("Checking PyInstaller")
    result = subprocess.run(
        [sys.executable, "-m", "PyInstaller", "--version"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    else:
        print(f"PyInstaller {result.stdout.strip()} found [OK]")

def clean_old_build():
    banner("Cleaning Previous Build")
    for folder in [DIST_DIR, BUILD_DIR]:
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
            print(f"Cleaned: {folder}")
    print("Clean done [OK]")

def run_build():
    banner("Building .exe (this may take 3-8 minutes)")
    print(f"Spec file: {SPEC_FILE}\n")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        SPEC_FILE,
    ]

    result = subprocess.run(cmd, cwd=PROJECT_DIR)

    if result.returncode != 0:
        print("[!] BUILD FAILED. Check the output above for errors.")
        sys.exit(1)

def create_desktop_shortcut():
    banner("Creating Desktop Shortcut")
    exe_path = os.path.join(DIST_DIR, EXE_NAME + ".exe")

    if not os.path.exists(exe_path):
        print(f"[!] EXE not found at: {exe_path}")
        return

    # --- Use PowerShell to get the true Desktop path (works with OneDrive) ---
    try:
        res = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "[Environment]::GetFolderPath('Desktop')"],
            capture_output=True, text=True, timeout=10
        )
        desktop = res.stdout.strip()
        if not desktop or not os.path.isdir(desktop):
            raise ValueError(f"Invalid desktop path: '{desktop}'")
    except Exception as e:
        print(f"[!] Could not determine Desktop path: {e}")
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        print(f"    Falling back to: {desktop}")

    lnk_path = os.path.join(desktop, EXE_NAME + ".lnk")

    ps_script = f"""
$ws  = New-Object -ComObject WScript.Shell
$lnk = $ws.CreateShortcut('{lnk_path}')
$lnk.TargetPath       = '{exe_path}'
$lnk.WorkingDirectory = '{DIST_DIR}'
$lnk.IconLocation     = '{exe_path},0'
$lnk.Description      = 'Eye Tracking Mouse System - AI Powered'
$lnk.WindowStyle      = 1
$lnk.Save()
Write-Output 'OK'
"""
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
             "-Command", ps_script],
            check=True, capture_output=True, text=True, timeout=15
        )
        if "OK" in result.stdout:
            print(f"Desktop shortcut created: {lnk_path} [OK]")
        else:
            print(f"[!] Unexpected output: {result.stdout}")
    except Exception as e:
        print(f"[!] Could not create shortcut automatically: {e}")
        print(f"    Manually copy the shortcut to Desktop from: {exe_path}")


def print_summary():
    banner("Build Complete!")
    exe_path = os.path.join(DIST_DIR, EXE_NAME + ".exe")
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"[OK]  EXE Location : {exe_path}")
        print(f"[OK]  File Size    : {size_mb:.1f} MB")
        print(f"[OK]  Icon         : Embedded")
        print(f"[OK]  Console      : Hidden (no black window)")
        print(f"[OK]  Auto-start   : Ready for desktop shortcut")
        print()
        print("HOW TO USE:")
        print("  1. Double-click the .exe or the Desktop shortcut")
        print("  2. Auth window opens -> login / register")
        print("  3. Eye tracking starts AUTOMATICALLY after auth")
        print("  4. Logs saved to: %APPDATA%\\EyeMouseUltra\\system_log.txt")
    else:
        print("[FAIL] EXE was not found after build!")

if __name__ == "__main__":
    os.chdir(PROJECT_DIR)
    check_pyinstaller()
    clean_old_build()
    run_build()
    create_desktop_shortcut()
    print_summary()
