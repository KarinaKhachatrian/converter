import os
from pathlib import Path

import img2pdf
from natsort import natsorted

from src.pdf_processor.processor import Processor


class ImagesConverter(Processor):
    def __init__(self, images_dir: Path, output_path: Path):
        self.images_dir = images_dir
        self.output_path = output_path

    @staticmethod
    def write_binary(filepath: Path, content: bytes):
        with open(filepath, 'wb') as f:
            f.write(content)

    def process(self) -> None:
        image_files = []
        for filename in natsorted(os.listdir(self.images_dir)):
            if filename.lower().endswith('.png'):
                full_path = os.path.join(self.images_dir, filename)
                print(f'Обработка файла {full_path}...')
                image_files.append(full_path)

        pdf_data = img2pdf.convert(image_files)
        self.write_binary(self.output_path, pdf_data)