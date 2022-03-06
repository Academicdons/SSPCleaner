# -*- mode: python ; coding: utf-8 -*-
added_files = [
("scripts/whatbot.py","scripts"),
("resources/DataBase/AllWhatsAppURLSDB.txt","resources/DataBase"),
("resources/DataBase/new.txt","resources/DataBase"),
("resources/whatsAppUrls.txt","resources"),
("resources/workinglinks.txt","resources"),
("UIFiles/runbot.ui","UIFiles"),
("UIFiles/WelcomePage.ui","UIFiles"),
("resources/chromedriver.exe", "resources")
]

block_cipher = None


a = Analysis(['main.py'],
             pathex=[],
             binaries=[ ( 'resources/chromedriver.exe', 'resources' ) ],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='Gee Bot',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
