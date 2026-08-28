# -*- mode: python ; coding: utf-8 -*-
# ============================================================
# EyeMouse AI Ultra – PyInstaller Spec (One-File Build)
# Run:  pyinstaller "EyeMouse AI Ultra.spec"
# ============================================================

import sys, os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs

block_cipher = None

# ── Collect all sub-modules that PyInstaller misses ───────────────────────────
hidden = []

# mediapipe (large package with many lazy-loaded sub-packages)
hidden += collect_submodules('mediapipe')

# customtkinter (loads .json themes at runtime)
hidden += collect_submodules('customtkinter')

# cv2 / OpenCV
hidden += collect_submodules('cv2')

# speech_recognition
hidden += collect_submodules('speech_recognition')

# pyautogui
hidden += collect_submodules('pyautogui')

# pyttsx3 — Windows voice engine
hidden += collect_submodules('pyttsx3')
hidden += ['pyttsx3.drivers', 'pyttsx3.drivers.sapi5']

# win32 extensions
hidden += [
    'win32gui', 'win32con', 'win32com', 'win32com.client',
    'win32api', 'pywintypes',
]

# scipy / numpy
hidden += collect_submodules('scipy')
hidden += collect_submodules('numpy')

# cryptography / bcrypt
hidden += ['cryptography', 'cryptography.fernet', 'bcrypt']

# PIL / Pillow
hidden += collect_submodules('PIL')

# pyperclip
hidden += ['pyperclip']

# sqlite3 is stdlib but include explicitly
hidden += ['sqlite3', '_sqlite3']

# Our app utilities (auto-shortcut, etc.)
hidden += ['utilities', 'utilities.auto_shortcut']

# json, threading, queue are stdlib — always available

# matplotlib is needed by mediapipe drawing_utils
hidden += ['matplotlib', 'matplotlib.pyplot']

# Additional scipy submodules often missed
hidden += ['scipy.spatial.transform._rotation_groups', 'scipy.special._cdflib']

# ── Collect data files (non-Python resources) ─────────────────────────────────
datas = []

# 1. MediaPipe model files (the .task / .tflite files)
datas += collect_data_files('mediapipe')

# 2. CustomTkinter themes
datas += collect_data_files('customtkinter')

# 3. Our own tracking model
datas += [('tracking/face_landmarker.task', 'tracking')]

# 4. App icon (needed at runtime for title-bar icon)
datas += [('app_icon.ico', '.')]

# ── Collect dynamic libraries that the above packages need ────────────────────
binaries = []
binaries += collect_dynamic_libs('mediapipe')
binaries += collect_dynamic_libs('cv2')

# ── Analysis ──────────────────────────────────────────────────────────────────
a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # ONLY exclude packages we are 100% sure are not used anywhere
        # DO NOT exclude stdlib modules like unittest/email/html/http/xml
        # — mediapipe, speech_recognition, scipy all use them internally
        'notebook',
        'IPython',
        'docutils',
        # 'torch',        # Keep these commented out if you use mediapipe tasks
        # 'tensorflow',   # as some models might trigger imports
        # 'jax',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# ── ONE-FILE exe ──────────────────────────────────────────────────────────────
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='EyeMouse AI Ultra',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[
        # Don't UPX these — they're already compressed or UPX breaks them
        'vcruntime140.dll', 'python*.dll', '_mediapipe*', 'libopencv*',
    ],
    runtime_tmpdir=None,   # Extract to a fixed temp dir on first run (faster second launch)
    console=False,         # ← NO black console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico',
    version=None,
)
