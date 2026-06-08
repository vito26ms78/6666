import time
import threading
from queue import Queue, Full, Empty

from window.window_detector import WindowDetector
from core.region_scheduler import RegionScheduler


class TranslationLoop:

    TTL_SECONDS = 5.0
    QUEUE_SIZE = 500

    def __init__(
        self,
        capture,
        ocr,
        translator,
        overlay,
        interval=0.1
    ):

        self.capture = capture
        self.ocr = ocr
        self.translator = translator
        self.overlay = overlay
        self.interval = interval

        self.window_detector = WindowDetector()
        self.region_scheduler = RegionScheduler()

        self.translation_queue = Queue(
            maxsize=self.QUEUE_SIZE
        )

        self.active_items = {}
        self.pending_translation = set()

        self.lock = threading.RLock()

        self.running = False

    def start(self):

        if self.running:
            return

        self.running = True

        threading.Thread(
            target=self.translation_worker,
            daemon=True,
            name="TranslationWorker"
        ).start()

        threading.Thread(
            target=self.run,
            daemon=True,
            name="TranslationLoop"
        ).start()

    def stop(self):

        self.running = False

    def translation_worker(self):

        while self.running:

            try:

                key, text = self.translation_queue.get(
                    timeout=0.5
                )

            except Empty:
                continue

            try:

                translated = self.translator.translate(
                    text
                )

            except Exception as e:

                print(
                    f"[TRANSLATOR ERROR] {e}"
                )

                translated = text

            finally:

                with self.lock:

                    if key in self.active_items:

                        self.active_items[key][
                            "translated"
                        ] = translated

                    self.pending_translation.discard(
                        key
                    )

                self.translation_queue.task_done()

    def run(self):

        while self.running:

            try:

                win = self.window_detector.get_foreground_window()

                if not win:

                    time.sleep(self.interval)
                    continue

                frame = self.capture.capture(
                    region=(
                        win["left"],
                        win["top"],
                        win["right"],
                        win["bottom"]
                    )
                )

                if frame is None:

                    time.sleep(self.interval)
                    continue

                h, w = frame.shape[:2]

                rx1, ry1, rx2, ry2 = (
                    self.region_scheduler.next_region(
                        w,
                        h
                    )
                )

                region_frame = frame[
                    ry1:ry2,
                    rx1:rx2
                ]

                now = time.time()

                detected_items = self.ocr.detect_text(
                    region_frame
                )

                for item in detected_items:

                    text = (
                        item.get("text", "")
                        .strip()
                    )

                    if not text:
                        continue

                    key = text.lower()

                    box = [
                        [
                            p[0] + rx1,
                            p[1] + ry1
                        ]
                        for p in item.get(
                            "box",
                            []
                        )
                    ]

                    with self.lock:

                        if key not in self.active_items:

                            self.active_items[key] = {
                                "box": box,
                                "text": text,
                                "translated": "...",
                                "last_seen": now
                            }

                            if (
                                key not in
                                self.pending_translation
                            ):

                                try:

                                    self.translation_queue.put_nowait(
                                        (key, text)
                                    )

                                    self.pending_translation.add(
                                        key
                                    )

                                except Full:

                                    print(
                                        "[QUEUE FULL]"
                                    )

                        else:

                            self.active_items[key][
                                "box"
                            ] = box

                            self.active_items[key][
                                "last_seen"
                            ] = now

                with self.lock:

                    expired = []

                    for k, v in self.active_items.items():

                        if (
                            now - v["last_seen"]
                        ) > self.TTL_SECONDS:

                            expired.append(k)

                    for k in expired:

                        self.active_items.pop(
                            k,
                            None
                        )

                    overlay_items = [

                        {
                            "box": v["box"],
                            "text": v["text"],
                            "translated": v["translated"]
                        }

                        for v in self.active_items.values()
                    ]

                self.overlay.update_items(
                    overlay_items
                )

            except Exception as e:

                print(
                    f"[LOOP ERROR] {e}"
                )

            time.sleep(
                self.interval
            )
