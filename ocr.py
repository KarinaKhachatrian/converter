from pathlib import Path
import subprocess

from src.pdf_processor.processor import Processor
from src.pdf_processor.get_base_path import get_base_path

class OCRProcessor(Processor):
    def __init__(self, pdf_path: Path,
                 docx_dir: Path,
                 ocr_engine_path: Path = None):
        self.pdf_filepath = pdf_path
        self.docx_dir = docx_dir
        self.base_path = get_base_path()

        if ocr_engine_path is None:
            self.ocr_engine_path = Path(self.base_path) / Path('ocr_engine') / Path('finereaderocr.exe')
        else:
            ocr_path = Path(ocr_engine_path)
            if ocr_path.is_absolute():
                self.ocr_engine_path = ocr_path
            else:
                self.ocr_engine_path = self.base_path / ocr_path

        self.docx_path = docx_dir / f'{pdf_path.stem}.docx'
        self.docx_dir.mkdir(exist_ok=True)

    def process(self) -> None:
        cmd = [
            self.ocr_engine_path,
            self.pdf_filepath,
            "/lang", "Russian", "English",
            "/out", self.docx_path
        ]
        subprocess.run(cmd)

