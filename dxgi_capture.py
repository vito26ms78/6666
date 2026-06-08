import dxcam

class DXGICapture:

    def __init__(self, monitor_index=0):
        self.monitor_index = monitor_index
        self.camera = None

    def initialize(self):

        self.camera = dxcam.create(
            output_idx=self.monitor_index
        )

        try:
            self.camera.start(
                target_fps=10
            )
        except Exception:
            pass

        return True

    def capture(self, region=None):

        if self.camera is None:
            return None

        try:
            frame = self.camera.get_latest_frame()

            if frame is not None:
                return frame

            return self.camera.grab(
                region=region
            )

        except Exception:
            return None
