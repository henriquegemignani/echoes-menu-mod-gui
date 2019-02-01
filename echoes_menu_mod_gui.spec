# -*- mode: python -*-

block_cipher = None
icon_path = "echoes_menu_mod_gui/data/icons/sky_temple_key_NqN_icon.ico"

a = Analysis(['echoes_menu_mod_gui/__main__.py', 'echoes_menu_mod_gui/cli/__init__.py'],
             pathex=[],
             binaries=[],
             datas=[
                 ("echoes_menu_mod_gui/data/icons", "data/icons"),
                 ("echoes_menu_mod_gui/data/ClarisEchoesMenu", "data/ClarisEchoesMenu"),
             ],
             hiddenimports=[
                "unittest.mock",
             ],
             hookspath=[],
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
          [],
          exclude_binaries=True,
          name='echoes_menu_mod_gui',
          debug=False,
          strip=False,
          upx=False,
          icon=icon_path,
          console=True)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='echoes_menu_mod_gui')
