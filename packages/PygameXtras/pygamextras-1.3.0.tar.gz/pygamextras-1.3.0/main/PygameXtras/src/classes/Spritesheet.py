import pygame
import os
import json

class Spritesheet:
    def __init__(self, path_to_folder: str, images_facing: str = "right"):
        """
        <name> must be the path to the folder containing the files listed below \n
        every file inside that folder must have the same name as the folder itself (ignoring endings) \n

        use self.get_frames to get images from the spritesheet (not self.__get_frame__ !)

        files necessary:
            - <name>.png
            - <name>.json (containing metadata)

        (works only with aseprite, best with horizontal strip)

        the json file has to have the following structure (the names
        of the frames have to be called just by their number):
        {
            "frames": {
                1: {
                    "frame": {
                        "x": ...,
                        "y": ...,
                        "w": ...,
                        "h": ...
                    }
                }
            }
        }
        """
        foldername = path_to_folder.split(os.sep)[-1]
        png_file = os.path.join(os.path.abspath(path_to_folder), (foldername + ".png"))
        json_file = os.path.join(os.path.abspath(path_to_folder), (foldername + ".json"))
        if not os.path.exists(png_file):
            raise FileNotFoundError(f"Could not find file {png_file}")
        elif not os.path.exists(json_file):
            raise FileNotFoundError(f"Could not find file {json_file}")

        self.base_image = pygame.image.load(png_file)
        with open(json_file) as f:
            self.metadata = json.load(f)

        assert images_facing in ["left", "right"], "invalid direction"
        self.images_facing = images_facing

    def __get_frame__(
            self, frame_number: int, colorkey: tuple[int, int, int] = (0, 0, 0),
            resize_factor: int = 1) -> dict:
        """returns a dict with images (left, right, flipped_left, flipped_right)"""

        assert self.metadata["frames"][str(frame_number)], f"no frame with number '{frame_number}' found"
        assert resize_factor > 0, "resize factor must be above 0"

        x = self.metadata["frames"][str(frame_number)]["frame"]["x"]
        y = self.metadata["frames"][str(frame_number)]["frame"]["y"]
        width = self.metadata["frames"][str(frame_number)]["frame"]["w"]
        height = self.metadata["frames"][str(frame_number)]["frame"]["h"]
        base_surface = pygame.Surface((width, height))
        base_surface.set_colorkey(colorkey)
        base_surface.blit(self.base_image, (0, 0), (x, y, width, height))

        if resize_factor != 1:
            new_width, new_height = int(width*resize_factor), int(height*resize_factor)
            base_surface = pygame.transform.scale(base_surface, (new_width, new_height))

        if self.images_facing == "right":
            img_dict = {
                "right": base_surface,
                "left": pygame.transform.flip(base_surface, True, False),
                "flipped_right": pygame.transform.flip(base_surface, False, True),
                "flipped_left": pygame.transform.flip(base_surface, False, True)
            }
        elif self.images_facing == "left":
            img_dict = {
                "right": pygame.transform.flip(base_surface, True, False),
                "left": base_surface,
                "flipped_right": pygame.transform.flip(base_surface, True, True),
                "flipped_left": pygame.transform.flip(base_surface, False, True)
            }

        return img_dict

    def get_frames(self, first_frame_number: int, last_frame_number: int,
                   colorkey: tuple[int, int, int] = (0, 0, 0),
                   resize_factor: int = 1) -> list[dict]:
        """ returns a list of the requested frames \n
        first_frame_number and last_frame_number are inclusive """
        try:
            return [self.__get_frame__(i, colorkey, resize_factor) for i in range(first_frame_number, last_frame_number + 1)]
        except KeyError:
            raise KeyError(
                f"key not found. you probably requested more frames than there are pictures in this spritesheet")

    def get_size(self, frame_number=0):
        width = self.metadata["frames"][str(frame_number)]["frame"]["w"]
        height = self.metadata["frames"][str(frame_number)]["frame"]["h"]
        return [width, height]
