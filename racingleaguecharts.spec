# -*- mode: python -*-
a = Analysis(['racingleaguecharts.py'],
             pathex=['C:\\Users\\darrylh\\Documents\\GitHub\\F1Telemetry'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='racingleaguecharts.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , version='version_file.txt', icon='rlc.ico')
