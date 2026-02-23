from PySide6.QtGui import QFont, QFontDatabase

def load_font(font_path: str, font_size: int) -> QFont:
    font_id = QFontDatabase.addApplicationFont(font_path)
    font_families = QFontDatabase.applicationFontFamilies(font_id)
    font = QFont(font_families[0], font_size)
    return font