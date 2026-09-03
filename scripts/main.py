"""main.py

The brain of the operation - solves the puzzle
"""

# imports
import dxcam
import cv2
import numpy as np
from pathlib import Path

class PuzzleSolver:

    camera = None
    captured_frame = None
    resolution : dict[str,str] = None
    ratios : dict[str,str] = None
    script_file_path: Path = None
    script_dir_path: Path = None

    """A class that solves the puzzle when initiated

    Attributes:
        camera: a dxcam camera
        captured_frame: a frame captured by the camera
        ratios: a dict containing relative ratios, 
        the script requires them to work in different resolutions
        resolution: stores resolution found by camera
        script_file_path: the absolute path of this file
        script_dir_path: the absolute path of this file's directory
    """
    def __init__(self):

        self.camera = dxcam.create(output_color="GRAY")
        self.resolution = {
            "width": self.camera.width, 
            "height": self.camera.height
        }
        self.ratios = {
            "left" : 920/3840,
            "right" : 2800/3840,
            "top" : 460/2160,
            "bot": 1770/2160
        }

        self.script_file_path = Path(__file__).resolve()
        self.script_dir_path = self.script_file_path.parent

    def __del__(self):

        self.camera.release()

    """Captures a frame of the whole screen 
    and saves it to the self.captured_frame variable
    """
    def screen_capture(self):

        self.captured_frame = self.camera.grab_view()

    """Captures a frame of provided region 
    and saves it to the self.captured_frame variable

    Parameters:
        region: a dict containing the relative ratios
        of the screen part that we want to capture
        values inside could be understood as percent of max x/y of the rezolution
    """
    def cropped_capture(self, ratios : dict[str,str]):

        region = self.get_region(self.ratios) 

        self.captured_frame = self.camera.grab_view(region)

    """Calculates the region to crop based on ratios and resolution
    region format: (x1,y1,x2,y2)
    """
    def get_region(self, ratios: dict[str,str], resolution: dict[str,str]):
        # calculate the raw pixel values
        top_left_point = (int(ratios["left"] * resolution["width"]), int(ratios["top"] * resolution["height"]))
        bot_right_point = (int(ratios["right"] * resolution["width"]), int(ratios["bot"] * resolution["height"]))

        region = (top_left_point[0], top_left_point[1], bot_right_point[0], bot_right_point[1])

        return region

    """Converts a captured frame into binary image
    """
    def frame_to_binary_image(self):

        is_grayscale = self.captured_frame.ndim == 2

        # if grayscale convert immediatley, else convert to grayscale first
        if not is_grayscale:
            self.captured_frame = cv2.cvtColor(self.captured_frame, cv2.COLOR_RGB2GRAY)

        self.captured_frame  = cv2.threshold(self.captured_frame,0,255,cv2.THRESH_BINARY)[1]


    """Testing function - displays the captured frame stored in the self.captured_frame variable
    """
    def display_captured_frame(self):

        if self.captured_frame is not None:

            cv2.imshow("Frame",self.captured_frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    """Testing function - loads an image from specified path to self.frame
    """
    def load_image_from_disk(self, path : Path, ratios: dict[str,str] | None = None, grayscale : bool = True):

        image = None

        if grayscale:
            image = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
        else:
            image = cv2.imread(path)

        if ratios is not None:

            height = None
            width = None
            channels = None

            if grayscale:
                height, width = image.shape
            else:
                height, width, channels = image.shape

            loaded_image_resolution  = {
                "width": width, 
                "height": height
            }

            region = self.get_region(ratios, loaded_image_resolution)

            x_start = region[0]
            y_start = region[1]
            x_end = region[2]
            y_end = region[3]

            image = image[y_start:y_end, x_start:x_end]

        self.captured_frame = np.array(image)

    """Testing function - saves the image to specified path from self.frame
    """
    def save_image_to_disk(self, path : Path):

        cv2.imwrite(path, self.captured_frame)
        

p = PuzzleSolver()
p.load_image_from_disk(p.script_dir_path.parent / "gfx" / "puzzle" / "1.png",p.ratios,False)
p.frame_to_binary_image()
p.save_image_to_disk(p.script_dir_path.parent / "gfx" / "testing" / "1.png")
p.display_captured_frame()