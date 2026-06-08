from PyQt6.QtWidgets import QApplication

from capture.dxgi_capture import DXGICapture
from ocr.easyocr_engine import EasyOCREngine
from translator.translator_engine import TranslatorEngine
from overlay.overlay_window import OverlayWindow
from core.translation_loop import TranslationLoop


APP_NAME = "Anber Translator V1.6 Realtime"


def main():

    print(APP_NAME)

    app = QApplication([])

    capture = DXGICapture()
    ocr = EasyOCREngine()
    translator = TranslatorEngine()
    overlay = OverlayWindow()

    if not capture.initialize():
        return

    if not ocr.initialize():
        return

    loop = TranslationLoop(
        capture=capture,
        ocr=ocr,
        translator=translator,
        overlay=overlay,
        interval=0.5
    )

    loop.start()

    overlay.show()

    app.exec()


if __name__ == "__main__":
    main()
