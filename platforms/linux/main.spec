# -*- mode: python ; coding: utf-8 -*-

import os
from kivymd.tools.packaging.pyinstaller import hooks_path as kivymd_hooks_path

#path = os.path.abspath(".")

a = Analysis(
    ['../../src/main.py'],
    pathex=['../../src'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'gui.user_info_screen',
        'gui.screen_manager',
        'gui.screen_hotreload_tester',
        'services.utils',
        'services.crypto_utils',
        'models.secure_file_handler',
        'models.user_transaction',
        'models.key',
        'models.minuto_voucher',
        'models.person',
        'models.voucher_transaction',
        'models.user_profile'
    ],
    hookspath=[kivymd_hooks_path],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    debug=False,
    strip=False,
    upx=True,
    name="app_name",
    console=True
)
