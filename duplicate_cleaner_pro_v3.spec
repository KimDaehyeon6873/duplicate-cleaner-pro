# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['duplicate_cleaner_pro_v3.py'],
    pathex=[],
    binaries=[],
    datas=[],
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
    name='duplicate_cleaner_pro_v3',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # 변경: True로 설정하여 심볼 스트립
    upx=False,   # 변경: False로 설정하여 UPX 압축 비활성화
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, # GUI 애플리케이션이므로 False 유지
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None, # 코드 서명이 필요하다면 여기에 ID 설정
    entitlements_file=None,
    icon=['duplicate_cleaner.ico'], # 아이콘 파일 지정
)
