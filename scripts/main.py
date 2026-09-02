"""main.py

The brain of the operation - solves the puzzle
"""

# imports
import dxcam
import cv2


class PuzzleSolver:

    camera = None
    captured_frame = None

    """A class that solves the puzzle when initiated

    Attributes:
        camera: a dxcam camera
        captured_frame: a frame captured by the camera
    """
    def __init__(self):

        self.camera = dxcam.create(output_color="GRAY")

    def __del__(self):

        self.camera.release()

    """Captures a frame and saves it to the self.captured_frame variable
    """
    def screen_capture(self):

        self.captured_frame = self.camera.grab_view()
        print(self.captured_frame)

    """Testing function - displays the captured frame stored in the self.captured_frame variable
    """
    def display_captured_frame(self):

        if self.captured_frame is not None:

            cv2.imshow("Frame",self.captured_frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

p = PuzzleSolver()
p.screen_capture()
p.display_captured_frame()