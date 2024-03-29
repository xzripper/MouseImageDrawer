"""Standalone ImGui window."""

from imgui.integrations.pygame import PygameRenderer

from OpenGL.GL import glClearColor, glClear, GL_COLOR_BUFFER_BIT

from pygame import Rect, OPENGL, DOUBLEBUF, NOFRAME, QUIT, MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION, SHOWN, HIDDEN

from pygame.display import set_mode, set_caption, set_icon, flip

from pygame.event import get as pg_events

from pygame.key import get_pressed, key_code

from pygame.mouse import get_pos

from pygame.image import load

from imgui import (create_context as imgui_create_ctx,

                   get_io as imgui_io,

                   new_frame,

                   begin,
                   end,

                   set_window_size,
                   set_window_position,

                   render as imgui_render,

                   get_draw_data)

from imgui import WINDOW_NO_COLLAPSE, WINDOW_NO_MOVE, WINDOW_NO_RESIZE

from keyboard import is_pressed

from pywinctl import getActiveWindow

from time import sleep

from sys import exit as sys_exit

from typing import Callable, Any


DEFAULT_SHOW_HIDE_KEY: str = 'insert'

IMGUI_STANDALONE_VERSION: str = '1.1.0-alpha'

class ImGuiStandalone:
    """ImGuiStandalone class."""

    def __init__(self,
                 title: str,

                 width: int,
                 height: int,

                 always_on_top: bool=False,

                 show_hide_key: int=DEFAULT_SHOW_HIDE_KEY,

                 background_color: tuple[int, int, int]=(0, 0, 0),

                 imgui_flags: Any=None) -> None:
        """Initialize standalone window."""
        set_mode((1, 1), NOFRAME); imgui_create_ctx()

        self._pg_window = set_mode((width, height), DOUBLEBUF | OPENGL | NOFRAME)

        set_caption(title)

        window = getActiveWindow(); (
            window.move(-width // 2, -height // 2),

            window.alwaysOnTop(always_on_top)); del window

        self._pg_render = PygameRenderer()

        self._imgui_io = imgui_io()

        self._imgui_io.display_size = (width, height)

        self.hidden = False

        self.title = title

        self.show_hide_key = show_hide_key

        self.background_color = background_color

        self.imgui_flags = imgui_flags

        self._window_header_rect = Rect(0, 0, self._imgui_io.display_size[0], 20)

    def set_icon(self, icon: str) -> None:
        """Set window icon."""
        set_icon(load(icon))

    def loop(self, main_func: Callable, on_close: Callable=None) -> None:
        """Main loop."""
        moving = False

        while True:
            for event in pg_events():
                if event.type == QUIT:
                    self.close()

                if event.type == MOUSEBUTTONDOWN:
                    moving = True

                elif event.type == MOUSEMOTION:
                    mx, my = get_pos()

                    if moving and Rect(mx, my, 16, 16).colliderect(self._window_header_rect):
                        getActiveWindow().move(mx - 10, my - 5)

                elif event.type == MOUSEBUTTONUP:
                    moving = False

                self._pg_render.process_event(event)

            self._pg_render.process_inputs()

            if self.show_hide_key != None:
                if self.hidden and ImGuiStandaloneUtilities.pressed_global(self.show_hide_key):
                    self.show()

                    sleep(.2)

                elif not self.hidden and ImGuiStandaloneUtilities.pressed_global(self.show_hide_key):
                    self.hide()

                    sleep(.2)

            new_frame()

            flags = WINDOW_NO_RESIZE | WINDOW_NO_MOVE | WINDOW_NO_COLLAPSE

            if self.imgui_flags:
                flags |= self.imgui_flags

            _, stay_open = begin(self.title, True, flags)

            if not stay_open:
                if on_close:
                    on_close()

                self.close()

            set_window_size(*self._imgui_io.display_size)

            set_window_position(0, 0)

            main_func()

            end()

            glClearColor(*self.background_color, 1)

            glClear(GL_COLOR_BUFFER_BIT)

            imgui_render()

            self._pg_render.render(get_draw_data())

            flip()

    def show(self) -> None:
        """Show window."""
        self._pg_window = set_mode(self._imgui_io.display_size, DOUBLEBUF | OPENGL | NOFRAME | SHOWN)

        self.hidden = False

    def hide(self) -> None:
        """Hide window."""
        self._pg_window = set_mode(self._imgui_io.display_size, DOUBLEBUF | OPENGL | NOFRAME | HIDDEN)

        self.hidden = True

    def close(self) -> None:
        """Close window."""
        sys_exit(0)

class ImGuiStandaloneUtilities:
    """Utilities."""

    values = {}

    @staticmethod
    def set_value(key: str, value: Any) -> None:
        """Save value."""
        ImGuiStandaloneUtilities.values[key] = value

    @staticmethod
    def get_value(key: str) -> Any:
        """Get value."""
        if key not in ImGuiStandaloneUtilities.values:
            return None

        return ImGuiStandaloneUtilities.values[key]

    @staticmethod
    def pressed(key: str) -> bool:
        """Is key pressed."""
        return get_pressed()[key_code(key)]

    @staticmethod
    def pressed_global(key: str) -> bool:
        """Is key pressed globally."""
        return is_pressed(key)
