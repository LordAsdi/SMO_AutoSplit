# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
                ('models', 'models'),
                ('ui/resources', 'ui/resources'),
                ('.version', '.'),
                ('defaults.json', '.')
              ]

a = Analysis(['SMO_AutoSplit.py'],
             pathex=['.'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=['venv/lib/site-packages/pyupdater/hooks'],
             hooksconfig={},
             runtime_hooks=['scripts/add_lib.py'],
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
          name='win',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          embed_manifest=False,
          icon='ui/resources/icons/icon.ico')
          
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='win')
