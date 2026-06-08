import time
import traceback


class MainLoop:

    def __init__(self, capture, detector, translator):
        self.capture = capture
        self.detector = detector
        self.translator = translator
        self.running = False

    def run_once(self):

        frame = self.capture.get_frame()

        if frame is None:
            return []

        try:

            results = self.detector.detect(frame)

        except Exception:
            traceback.print_exc()
            return []

        output = []

        for item in results:

            try:

                text = item[1]

                translated = self.translator.translate(text)

                output.append(
                    {
                        "text": translated,
                        "x": 100,
                        "y": 100
                    }
                )

            except Exception:
                traceback.print_exc()

        return output

    def run_forever(self):

        self.running = True

        while self.running:

            try:
                self.run_once()

            except Exception:
                traceback.print_exc()

            time.sleep(0.1)

    def stop(self):
        self.running = False