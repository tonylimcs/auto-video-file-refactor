# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['auto_video_file_refactor.py'],
    pathex=[],
    binaries=[],
    datas=[('auto_video_file_refactor/view/icons', 'auto_video_file_refactor/view/icons'), ('film_roll_icon.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Auto Video File Refactor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['film_roll_icon.ico'],
)
