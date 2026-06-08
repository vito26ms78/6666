import threading

import easyocr
import torch


class EasyOCRDetector:

    def __init__(
        self,
        languages=None,
        confidence_threshold=0.30
    ):

        if languages is None:

            languages = [
                "en",
                "ja",
                "ko",
                "ch_tra"
            ]

        self.languages = languages

        self.confidence_threshold = (
            confidence_threshold
        )

        self.reader = None

        self.lock = threading.RLock()

        self.gpu_enabled = False

    def initialize(self):

        try:

            self.gpu_enabled = (
                torch.cuda.is_available()
            )

            print(
                f"[EasyOCR] GPU={self.gpu_enabled}"
            )

            self.reader = easyocr.Reader(
                self.languages,
                gpu=self.gpu_enabled,
                verbose=False
            )

            return True

        except Exception as e:

            print(
                f"[EasyOCR Init Error] {e}"
            )

            return False

    def detect_text(
        self,
        image
    ):

        if image is None:
            return []

        if self.reader is None:
            return []

        try:

            with self.lock:

                results = self.reader.readtext(
                    image,
                    detail=1,
                    paragraph=False,
                    batch_size=1
                )

            output = []

            for item in results:

                if len(item) < 3:
                    continue

                box = item[0]
                text = item[1]
                confidence = item[2]

                if not text:
                    continue

                if (
                    confidence
                    < self.confidence_threshold
                ):
                    continue

                output.append(
                    {
                        "text": text.strip(),
                        "box": box,
                        "confidence": confidence
                    }
                )

            return output

        except Exception as e:

            print(
                f"[EasyOCR Error] {e}"
            )

            return []

    def shutdown(self):

        self.reader = None

        if self.gpu_enabled:

            try:

                torch.cuda.empty_cache()

            except Exception:
                pass
