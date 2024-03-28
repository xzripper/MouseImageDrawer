from imgui_standalone import ImGuiStandalone, ImGuiStandaloneUtilities, IMGUI_STANDALONE_VERSION

from imgui import text, text_disabled, button, radio_button, checkbox, input_int, input_int2, input_float, same_line

from ui_utils import error, ask_image, ask_area

from draw import draw_more_black_r_white, draw_brightness_threshold, draw_edge, draw_laplacian

from time import perf_counter

from loguru import logger


MID_VERSION: str = 'v1.1.1-alpha'

DEFAULT_THRESHOLD_EDGE: list = [25, 25]

ImGuiStandaloneUtilities.set_value('image', None)

ImGuiStandaloneUtilities.set_value('draw_area', None)

ImGuiStandaloneUtilities.set_value('drawing_method', None)

ImGuiStandaloneUtilities.set_value('delay', 0.001)

ImGuiStandaloneUtilities.set_value('inversed', False)

ImGuiStandaloneUtilities.set_value('skip_after', -1)

ImGuiStandaloneUtilities.set_value('drawing', False)

ImGuiStandaloneUtilities.set_value('request_stop', False)

ImGuiStandaloneUtilities.set_value('_EDGE', True)

ImGuiStandaloneUtilities.set_value('_threshold', DEFAULT_THRESHOLD_EDGE)

logger.info(f'Registered {", ".join(ImGuiStandaloneUtilities.values.keys())}.')

def _format_img_path(path: str) -> str:
    return path.split('/')[-1][:16] + f'... ({path.split(".")[-1].upper()})' if path else None

def _format_area(area: tuple) -> str:
    return f'W{area[0]}H:{area[1]}-X{area[2]}:Y{area[3]}' if area else None

def main() -> None:
    text(f'Image: {_format_img_path(ImGuiStandaloneUtilities.get_value("image"))}.'); same_line()

    if button('Select image.'):
        logger.info('User tries to select image : ask_image()')

        image = ask_image()

        if image:
            ImGuiStandaloneUtilities.set_value('image', image)

            logger.info(f'Image updated: `{image}`.')

        else:
            logger.warning('Image selection canceled.')

    text(f'Area: {_format_area(ImGuiStandaloneUtilities.get_value("draw_area"))}.'); same_line()

    if button('Select area.'):
        logger.info('User tries to select area : ask_area()')

        area = ask_area(ImGuiStandaloneUtilities.get_value('draw_area'))

        if area:
            ImGuiStandaloneUtilities.set_value('draw_area', area)

            logger.info(f'Area specified: `{area}`.')

        else:
            logger.warning('Area selection canceled.')

    delay = input_float('Delay.', ImGuiStandaloneUtilities.get_value('delay'), 0.001, 0.0001, '%.4f')[1]

    if delay < 0:
        delay = 0

    elif delay > 0.1:
        delay = 0.1

    ImGuiStandaloneUtilities.set_value('delay', delay)

    if not ImGuiStandaloneUtilities.get_value('_EDGE'):
        if not isinstance(ImGuiStandaloneUtilities.get_value('_threshold'), int):
            logger.info('Casting _threshold to INT...')

            ImGuiStandaloneUtilities.set_value('_threshold', ImGuiStandaloneUtilities.get_value('_threshold')[0])

        ImGuiStandaloneUtilities.set_value('_threshold', 255 if ImGuiStandaloneUtilities.get_value('_threshold') > 255 else \
            (0 if (_t := input_int('Threshold.', ImGuiStandaloneUtilities.get_value('_threshold'))[1]) < 0 else _t))

    else:
        if not isinstance(ImGuiStandaloneUtilities.get_value('_threshold'), list):
            logger.info('Casting _threshold to LIST...')

            ImGuiStandaloneUtilities.set_value('_threshold', DEFAULT_THRESHOLD_EDGE)

        _threshold = input_int2('Threshold.', *ImGuiStandaloneUtilities.get_value('_threshold'))[1]

        if _threshold[0] < 0: _threshold[0] = 0
        elif _threshold[0] > 255: _threshold[0] = 255

        if _threshold[1] < 0: _threshold[1] = 0
        elif _threshold[1] > 255: _threshold[1] = 255

        ImGuiStandaloneUtilities.set_value('_threshold', _threshold)

    ImGuiStandaloneUtilities.set_value('skip_after', -1 if (_s := input_int('Skip each:...', ImGuiStandaloneUtilities.get_value('skip_after'))[1]) < -1 else _s)

    if radio_button('MORE_BLACK_R_WHITE', ImGuiStandaloneUtilities.get_value('_MORE_BLACK_R_WHITE')):
        ImGuiStandaloneUtilities.set_value('_BRIGHTNESS_THRESHOLDING', False)
        ImGuiStandaloneUtilities.set_value('_EDGE', False)
        ImGuiStandaloneUtilities.set_value('_LAPLACIAN', False)

        ImGuiStandaloneUtilities.set_value('_MORE_BLACK_R_WHITE', not ImGuiStandaloneUtilities.get_value('_MORE_BLACK_R_WHITE'))

        logger.info('Mode: MORE_BLACK_R_WHITE.')

    same_line()

    if radio_button('BRIGHTNESS_THRESHOLDING', ImGuiStandaloneUtilities.get_value('_BRIGHTNESS_THRESHOLDING')):
        ImGuiStandaloneUtilities.set_value('_MORE_BLACK_R_WHITE', False)
        ImGuiStandaloneUtilities.set_value('_EDGE', False)
        ImGuiStandaloneUtilities.set_value('_LAPLACIAN', False)

        ImGuiStandaloneUtilities.set_value('_BRIGHTNESS_THRESHOLDING', not ImGuiStandaloneUtilities.get_value('_BRIGHTNESS_THRESHOLDING'))

        logger.info('Mode: BRIGHTNESS_THRESHOLDING.')

    if radio_button('EDGE_CANNY', ImGuiStandaloneUtilities.get_value('_EDGE')):
        ImGuiStandaloneUtilities.set_value('_MORE_BLACK_R_WHITE', False)
        ImGuiStandaloneUtilities.set_value('_BRIGHTNESS_THRESHOLDING', False)
        ImGuiStandaloneUtilities.set_value('_LAPLACIAN', False)

        ImGuiStandaloneUtilities.set_value('_EDGE', not ImGuiStandaloneUtilities.get_value('_EDGE'))

        logger.info('Mode: EDGE.')

    same_line()

    if radio_button('LAPLACIAN', ImGuiStandaloneUtilities.get_value('_LAPLACIAN')):
        ImGuiStandaloneUtilities.set_value('_MORE_BLACK_R_WHITE', False)
        ImGuiStandaloneUtilities.set_value('_BRIGHTNESS_THRESHOLDING', False)
        ImGuiStandaloneUtilities.set_value('_EDGE', False)

        ImGuiStandaloneUtilities.set_value('_LAPLACIAN', not ImGuiStandaloneUtilities.get_value('_LAPLACIAN'))

        logger.info('Mode: LAPLACIAN.')

    same_line()

    ImGuiStandaloneUtilities.set_value('inversed', checkbox('Inverse.', ImGuiStandaloneUtilities.get_value('inversed'))[1])

    same_line()

    if ImGuiStandaloneUtilities.get_value('_drawing_took'):
        text(f'[Took {ImGuiStandaloneUtilities.get_value("_drawing_took"):.1f}s].')

    else:
        text('[Took: XXXs].')

    if not ImGuiStandaloneUtilities.get_value('drawing'):
        if button('Draw.'):
            if not ImGuiStandaloneUtilities.get_value('image'):
                error('Missing image.', 'Please specify image.')

                return

            if not ImGuiStandaloneUtilities.get_value('draw_area'):
                error('Missing area.', 'Please specify area.')

                return

            before_drawing = perf_counter()

            if ImGuiStandaloneUtilities.get_value('_MORE_BLACK_R_WHITE'):
                logger.info('Starting drawing with mode MORE_BLACK_R_WHITE.')

                draw_more_black_r_white(
                    ImGuiStandaloneUtilities.get_value('image'),

                    ImGuiStandaloneUtilities.get_value('draw_area'),

                    ImGuiStandaloneUtilities.get_value('_threshold'),

                    ImGuiStandaloneUtilities.get_value('inversed'),

                    ImGuiStandaloneUtilities.get_value('delay'), ImGuiStandaloneUtilities)

            elif ImGuiStandaloneUtilities.get_value('_BRIGHTNESS_THRESHOLDING'):
                logger.info('Starting drawing with mode BRIGHTNESS_THRESHOLDING.')

                draw_brightness_threshold(
                    ImGuiStandaloneUtilities.get_value('image'),

                    ImGuiStandaloneUtilities.get_value('draw_area'),

                    ImGuiStandaloneUtilities.get_value('_threshold'),

                    ImGuiStandaloneUtilities.get_value('inversed'),

                    ImGuiStandaloneUtilities.get_value('delay'), ImGuiStandaloneUtilities)

            elif ImGuiStandaloneUtilities.get_value('_EDGE'):
                logger.info('Starting drawing with mode EDGE.')

                draw_edge(
                    ImGuiStandaloneUtilities.get_value('image'),

                    ImGuiStandaloneUtilities.get_value('draw_area'),

                    ImGuiStandaloneUtilities.get_value('_threshold'),

                    ImGuiStandaloneUtilities.get_value('inversed'),

                    ImGuiStandaloneUtilities.get_value('delay'), ImGuiStandaloneUtilities)

            elif ImGuiStandaloneUtilities.get_value('_LAPLACIAN'):
                logger.info('Starting drawing with mode LAPLACIAN.')

                draw_laplacian(
                    ImGuiStandaloneUtilities.get_value('image'),

                    ImGuiStandaloneUtilities.get_value('draw_area'),

                    ImGuiStandaloneUtilities.get_value('_threshold'),

                    ImGuiStandaloneUtilities.get_value('inversed'),

                    ImGuiStandaloneUtilities.get_value('delay'), ImGuiStandaloneUtilities)

            ImGuiStandaloneUtilities.set_value('_drawing_took', perf_counter() - before_drawing)

            logger.info(f'Drawing took: {ImGuiStandaloneUtilities.get_value("_drawing_took"):.2f}s.')

    else: text_disabled('Draw.')

    same_line()

    if ImGuiStandaloneUtilities.get_value('drawing'):
        if button('Stop. (F5).'):
            logger.info('Requesting stop...')

            ImGuiStandaloneUtilities.set_value('request_stop', True)

            ImGuiStandaloneUtilities.set_value('drawing', False)

    else: text_disabled('Stop. (F5).')

    same_line(); text(f'MID {MID_VERSION}'); same_line(); text(F'imgui-s {IMGUI_STANDALONE_VERSION}')

logger.info('Initializing window...')

ImGuiStandalone('Mouse Image Drawer.', 405, 215, False, None, (0, 0, 0), None).loop(main, lambda: logger.info('Window closed.'))
