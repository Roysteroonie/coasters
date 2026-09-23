# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
import os

# GitHub Actions sets OPENSCAD_DIR after installing OpenSCAD.
openscad_dir = os.environ.get('OPENSCAD_DIR', r'C:\Program Files\OpenSCAD')
if not Path(openscad_dir).exists():
    raise RuntimeError(f'OpenSCAD directory not found: {openscad_dir}')

# Bundle the entire OpenSCAD runtime so end users do not need to install it.
datas = [(openscad_dir, 'openscad')]

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['matplotlib.backends.backend_agg'],
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
    [],
    exclude_binaries=True,
    name='RLO_Player_Coaster_Generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='RLO_Player_Coaster_Generator',
)
