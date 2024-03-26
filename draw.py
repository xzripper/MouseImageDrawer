from imgui_standalone import ImGuiStandaloneUtilities

from cv2 import Canny, Laplacian, imread, resize, cvtColor, COLOR_BGR2GRAY, CV_64F

from mouse import move, click

from keyboard import is_pressed

from time import sleep


def draw_more_black_r_white(image_path: str, area: tuple, threshold: int, inversed: bool, delay: float, _utils: ImGuiStandaloneUtilities) -> None:
    image = imread(image_path)

    image = resize(image, (area[0], area[1]))

    pixels_drawn = 0

    for y in range(area[1]):
        for x in range(area[0]):
            if _utils.get_value('request_stop') or is_pressed('F5'): break
    
            b, g, r = image[y, x]

            if pixels_drawn == _utils.get_value('skip_after'):
                pixels_drawn = 0

            else:
                if (not (((b + g + r) // 3) < threshold)) if inversed else ((b + g + r) // 3) < threshold:
                    pixels_drawn += 1

                    move(area[2] + x, area[3] + y); click()

                    sleep(delay)

def draw_brightness_threshold(image_path: str, area: tuple, threshold: int, inversed: bool, delay: float, _utils: ImGuiStandaloneUtilities) -> None:
    image = imread(image_path)

    image = resize(image, (area[0], area[1]))

    grey_image = cvtColor(image, COLOR_BGR2GRAY)

    pixels_drawn = 0

    for y in range(area[1]):
        for x in range(area[0]):
            if _utils.get_value('request_stop') or is_pressed('F5'): break

            if pixels_drawn == _utils.get_value('skip_after'):
                pixels_drawn = 0

            else:
                if (not (grey_image[y, x] > threshold)) if inversed else grey_image[y, x] > threshold:
                    pixels_drawn += 1

                    move(area[2] + x, area[3] + y); click()

                    sleep(delay)

def draw_edge(image_path: str, area: tuple, threshold: list, inversed: bool, delay: float, _utils: ImGuiStandaloneUtilities) -> None:
    image = imread(image_path)

    image = resize(image, (area[0], area[1]))

    edges = Canny(image, threshold[0], threshold[1])

    pixels_drawn = 0

    for y in range(area[1]):
        for x in range(area[0]):
            if _utils.get_value('request_stop') or is_pressed('F5'): break

            if pixels_drawn == _utils.get_value('skip_after'):
                pixels_drawn = 0

            else:
                if (not (edges[y, x] > 0)) if inversed else edges[y, x] > 0:
                    pixels_drawn += 1

                    move(area[2] + x, area[3] + y); click()

                    sleep(delay)

def draw_laplacian(image_path: str, area: tuple, threshold: int, inversed: bool, delay: float, _utils: ImGuiStandaloneUtilities) -> None:
    if threshold > 31:
        threshold = 31

    if threshold > 1 and threshold % 2 == 0:
        threshold += 1

    image = imread(image_path)

    image = resize(image, (area[0], area[1]))

    edges = Laplacian(cvtColor(image, COLOR_BGR2GRAY), CV_64F, ksize=threshold)

    pixels_drawn = 0

    for y in range(area[1]):
        for x in range(area[0]):
            if _utils.get_value('request_stop') or is_pressed('F5'): break

            if pixels_drawn == _utils.get_value('skip_after'):
                pixels_drawn = 0

            else:
                if (not (edges[y, x] > 0)) if inversed else edges[y, x] > 0:
                    pixels_drawn += 1

                    move(area[2] + x, area[3] + y); click()

                    sleep(delay)
