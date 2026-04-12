import os
from pathlib import Path

from concurrent.futures import ThreadPoolExecutor
import multiprocessing

import pymupdf

from src.pdf_processor.processor import Processor

class PDFConverter(Processor):
    def __init__(self, pdf_path: Path, output_dir: Path, image_format="png", dpi=400, workers=None):
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        self.image_format = image_format
        self.dpi = dpi
        self.workers = workers or multiprocessing.cpu_count()

    def render_page(self, page_num: int):
        doc = pymupdf.open(self.pdf_path)
        page = doc[page_num]
        pix = page.get_pixmap(dpi=self.dpi)

        output_path = self.output_dir / f"page_{page_num + 1}.{self.image_format}"
        pix.save(str(output_path))

        doc.close()

    def process(self):
        os.makedirs(self.output_dir, exist_ok=True)

        doc = pymupdf.open(self.pdf_path)
        page_count = doc.page_count
        doc.close()

        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            executor.map(self.render_page, range(page_count))

