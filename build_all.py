import os
import sys
import subprocess
from PIL import Image

def build():
    # 1. Paths
    root = os.path.abspath(".")
    icon_png = r"C:\Users\Musharab Ali\.gemini\antigravity\brain\7a669fe7-93c6-4a56-8201-6bdc01aa4377\eye_tracking_logo_1781464752097.png"
    icon_ico = os.path.join(root, "app_icon.ico")
    
    print("--- CONVERTING LOGO ---")
    img = Image.open(icon_png)
    img.save(icon_ico, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32)])
    
    print("--- RUNNING PYINSTALLER ---")
    pyinstaller_path = os.path.join(root, ".venv", "Scripts", "pyinstaller.exe")
    
    separator = ";" # Windows separator
    cmd = [
        pyinstaller_path,
        "--noconsole",
        "--onefile",
        f"--icon={icon_ico}",
        f"--add-data=tracking/face_landmarker.task{separator}tracking",
        "--name=Eye Tracking Mouse System",
        "main.py"
    ]
    
    subprocess.run(cmd, check=True)
    
    print("--- CREATING DESKTOP SHORTCUT ---")
    exe_path = os.path.join(root, "dist", "Eye Tracking Mouse System.exe")
    
    # Get official Desktop path via PowerShell
    res = subprocess.run(["powershell", "-Command", "[Environment]::GetFolderPath('Desktop')"], capture_output=True, text=True)
    desktop = res.stdout.strip()
    if not desktop:
        desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
        
    shortcut_path = os.path.join(desktop, "Eye Tracking Mouse System.lnk")
    
    # Use escaped double quotes for paths with spaces
    powershell_cmd = f"$s=New-Object -ComObject WScript.Shell; $lnk=$s.CreateShortcut(\"{shortcut_path}\"); $lnk.TargetPath=\"{exe_path}\"; $lnk.IconLocation=\"{exe_path}\"; $lnk.Save()"
    subprocess.run(["powershell", "-Command", powershell_cmd], check=True)
    
    print(f"\n✅ SUCCESS! The application has been compiled to 'dist/'.")
    print(f"✅ Shortcut created on your Desktop.")

if __name__ == "__main__":
    build()
