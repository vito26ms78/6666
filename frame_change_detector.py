import time

import cv2
import numpy as np


class FrameChangeDetector:

    def __init__(
        self,
        hash_size=16,
        hash_threshold=10,
        resize_width=256,
        cooldown_seconds=0.35
    ):

        self.hash_size = hash_size
        self.hash_threshold = hash_threshold
        self.resize_width = resize_width
        self.cooldown_seconds = cooldown_seconds

        self.previous_hash = None
        self.last_trigger_time = 0.0

    def _compute_hash(self, frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        resized = cv2.resize(
            gray,
            (self.hash_size, self.hash_size),
            interpolation=cv2.INTER_AREA
        )

        avg = resized.mean()

        return resized > avg

    def _hash_distance(self, hash_a, hash_b):

        return np.count_nonzero(hash_a != hash_b)

    def changed(self, frame):

        if frame is None:
            return False

        if frame.size == 0:
            return False

        if len(frame.shape) < 2:
            return False

        h, w = frame.shape[:2]

        if h <= 0 or w <= 0:
            return False

        scale = self.resize_width / w

        preview = cv2.resize(
            frame,
            (
                self.resize_width,
                max(1, int(h * scale))
            ),
            interpolation=cv2.INTER_AREA
        )

        current_hash = self._compute_hash(preview)

        if self.previous_hash is None:

            self.previous_hash = current_hash
            self.last_trigger_time = time.time()

            return True

        distance = self._hash_distance(
            self.previous_hash,
            current_hash
        )

        self.previous_hash = current_hash

        if distance < self.hash_threshold:
            return False

        now = time.time()

        if (now - self.last_trigger_time) < self.cooldown_seconds:
            return False

        self.last_trigger_time = now

        return True

    def reset(self):

        self.previous_hash = None
        self.last_trigger_time = 0.0
