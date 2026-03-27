# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path


project_root = Path.cwd()
resources_tessdata = project_root / "resources" / "tessdata"
portable_tesseract_dir = Path(
    os.getenv("PDF_READER_TESSERACT_DIR", str(project_root / "vendor" / "tesseract"))
)

datas = []
if resources_tessdata.exists():
    datas.append((str(resources_tessdata), "resources/tessdata"))

if portable_tesseract_dir.exists():
    for file_path in portable_tesseract_dir.rglob("*"):
        if file_path.is_file():
            relative_parent = Path("vendor") / "tesseract" / file_path.relative_to(portable_tesseract_dir).parent
            datas.append((str(file_path), str(relative_parent)))

excludes = [
    "IPython",
    "PyQt5",
    "PyQt6",
    "jedi",
    "matplotlib",
    "pytest",
    "scipy",
    "sqlalchemy",
    "tkinter",
    "_tkinter",
]


block_cipher = None


a = Analysis(
    [str(project_root / "src" / "app" / "main.py")],
    pathex=[str(project_root), str(project_root / "src")],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="pdf-reader",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="pdf-reader",
)
