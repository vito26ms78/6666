
import cv2
import easyocr
import torch

class EasyOCREngine:

    MIN_CONFIDENCE = 0.15

    def __init__(self):
        self.reader = None

    def initialize(self):
        gpu_enabled = torch.cuda.is_available()
        print(f"[OCR] GPU Enabled: {gpu_enabled}")
        self.reader = easyocr.Reader(["en"], gpu=gpu_enabled)
        return True

    def preprocess(self, frame):
        enlarged = cv2.resize(
            frame,
            None,
            fx=1.25,
            fy=1.25,
            interpolation=cv2.INTER_LINEAR
        )

        gray = cv2.cvtColor(enlarged, cv2.COLOR_BGR2GRAY)
        return gray

    def detect_text(self, frame):

        if self.reader is None:
            return []

        processed = self.preprocess(frame)

        results = self.reader.readtext(
            processed,
            paragraph=False,
            low_text=0.15,
            text_threshold=0.40,
            link_threshold=0.30
        )

        parsed = []

        for item in results:

            text = str(item[1]).strip()
            conf = float(item[2])

            if conf < self.MIN_CONFIDENCE:
                continue

            if len(text) <= 1:
                continue

            parsed.append({
                "box": [[p[0]/1.25, p[1]/1.25] for p in item[0]],
                "text": text,
                "confidence": conf
            })

        return parsed
