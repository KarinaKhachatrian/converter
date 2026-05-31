# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\khach\\PycharmProjects\\diploma\\src\\app.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\khach\\PycharmProjects\\diploma\\src\\fonts', 'src/fonts/'), ('C:\\Users\\khach\\PycharmProjects\\diploma\\src\\icons', 'src/icons/'), ('C:\\Users\\khach\\PycharmProjects\\diploma\\src\\styles', 'src/styles/'), ('C:\\Users\\khach\\PycharmProjects\\diploma\\src\\ocr_engine', 'src/ocr_engine/')],
    hiddenimports=['src.account.account_window', 'src.auth.auth_methods', 'src.auth.hash_password', 'src.auth.login', 'src.auth.regex', 'src.auth.register', 'src.db.database', 'src.db.exec_select', 'src.db.init_db', 'src.get_base_path', 'src.interfaces', 'src.pdf_processor.document_processor', 'src.pdf_processor.headers', 'src.pdf_processor.html_converter', 'src.pdf_processor.html_processor', 'src.pdf_processor.images_converter', 'src.pdf_processor.ocr', 'src.pdf_processor.pdf_converter', 'src.pdf_processor.pdf_processor_window', 'src.pdf_processor.processor', 'src.pdf_processor.stamps_extractor', 'src.pdf_processor.tables_fixer', 'src.pdf_processor.wrapper', 'src.read.read_window', 'src.structurer.structurer', 'src.structurer.structurer_window', 'src.window_methods', 'PySide6', 'abc', 'ast', 'bs4', 'concurrent', 'cv2', 'docx', 'dotenv', 'hashlib', 'img2pdf', 'multiprocessing', 'natsort', 'numpy', 'os', 'pathlib', 'psycopg2', 'pymupdf', 're', 'shutil', 'string', 'subprocess', 'sys', 'time', 'traceback', 'typing', 'ultralytics'],
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
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='app',
)
