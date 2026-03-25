from pathlib import Path

import numpy as np
import cv2
from ultralytics import YOLO

from src.pdf_processor.processor import Processor
from src.pdf_processor.get_base_path import get_base_path


class StampsExtractor(Processor):
    def __init__(self, images_dir: Path,
                 output_dir: Path,
                 weights_path: Path = None
        ):
        self.images_dir = images_dir
        self.output_dir = output_dir
        self.base_path = get_base_path()

        if weights_path is None:
            self.weights_path = Path(self.base_path) / Path('train') / Path('weights') / Path('best.pt')
        else:
            self.weights_path = weights_path

        self.output_dir.mkdir(exist_ok=True)

        self.model = YOLO(self.weights_path)

    def process_image(self, image_path: Path):
        print(f"Обработка изображения {image_path.name}...")

        results = self.model.predict(str(image_path), verbose=False)

        for r in results:
            img = np.copy(r.orig_img)
            result = img.copy()
            img_name = Path(r.path).stem

            for c in r:
                x1, y1, x2, y2 = c.boxes.xyxy.cpu().numpy().squeeze().astype(np.int32)

                h, w = img.shape[:2]
                pad_left, pad_top, pad_right, pad_bottom = 10, 10, 10, 50

                x1p = max(0, x1 - pad_left)
                y1p = max(0, y1 - pad_top)
                x2p = min(w, x2 + pad_right)
                y2p = min(h, y2 + pad_bottom)

                stamp_mask = np.zeros(img.shape[:2], dtype=np.uint8)
                cv2.rectangle(stamp_mask, (x1p, y1p), (x2p, y2p), 255, -1)

                kernel = np.ones((10, 10), np.uint8)
                stamp_mask = cv2.dilate(stamp_mask, kernel, iterations=1)

                result_hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV).astype(np.float32)

                mask = stamp_mask == 255
                result_hsv[..., 1][mask] *= 0.01
                result_hsv[..., 2][mask] = np.clip(result_hsv[..., 2][mask] * 1.15, 0, 255)

                result = cv2.cvtColor(result_hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

            output_path = self.output_dir / f"{img_name}.png"
            cv2.imwrite(str(output_path), result)

    def process(self):
        images = list(self.images_dir.glob("*.png"))

        for image in images:
            self.process_image(image)
