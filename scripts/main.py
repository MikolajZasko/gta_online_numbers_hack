"""main.py

The brain of the operation - solves the puzzle
"""

# imports
import dxcam
import cv2


class PuzzleSolver:

    camera = None
    captured_frame = None
    resolution : dict[str,str] = None
    ratios : dict[str,str] = None

    """A class that solves the puzzle when initiated

    Attributes:
        camera: a dxcam camera
        captured_frame: a frame captured by the camera
        ratios: a dict containing relative ratios, 
        the script requires them to work in different resolutions
        resolution: stores resolution found by camera
    """
    def __init__(self):

        self.camera = dxcam.create(output_color="GRAY")
        self.resolution = {
            "width": self.camera.width, 
            "height": self.camera.height
        }
        self.ratios = {
            "left" : 900/3840,
            "right" : 2800/3840,
            "top" : 460/2160,
            "bot": 1770/2160
        }

    def __del__(self):

        self.camera.release()

    """Captures a frame of the whole screen 
    and saves it to the self.captured_frame variable
    """
    def screen_capture(self):

        self.captured_frame = self.camera.grab_view()
        print(self.captured_frame)

    """Captures a frame of provided region 
    and saves it to the self.captured_frame variable

    Parameters:
        region: a dict containing the relative ratios
        of the screen part that we want to capture
        values inside could be understood as percent of max x/y of the rezolution
    """
    def cropped_capture(self, ratios):

        # calculate the raw pixel values
        top_left_point = (int(ratios["left"] * self.resolution["width"]), int(ratios["top"] * self.resolution["height"]))
        bot_right_point = (int(ratios["right"] * self.resolution["width"]), int(ratios["bot"] * self.resolution["height"]))

        region = (top_left_point[0], top_left_point[1], bot_right_point[0], bot_right_point[1])

        self.captured_frame = self.camera.grab_view(region)


    """Testing function - displays the captured frame stored in the self.captured_frame variable
    """
    def display_captured_frame(self):

        if self.captured_frame is not None:

            cv2.imshow("Frame",self.captured_frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

p = PuzzleSolver()
print(p.ratios)
p.cropped_capture(p.ratios)
p.display_captured_frame()