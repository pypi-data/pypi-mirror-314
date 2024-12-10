# CONSTANTS #
# Buttons
BUTTON_A = 12
BUTTON_B = 13
BUTTON_C = 14
BUTTON_D = 15
BUTTON_DOWN = 11
BUTTON_E = 11
BUTTON_UP = 15
BUTTON_USER = 23

# Update speeds
UPDATE_NORMAL = 0
UPDATE_MEDIUM = 1
UPDATE_FAST = 2
UPDATE_TURBO = 3

# System speeds
SYSTEM_VERY_SLOW = 0  # 4 MHz if on battery, 48 MHz if connected to USB
SYSTEM_SLOW = 1       # 12 MHz if on battery, 48 MHz if connected to USB
SYSTEM_NORMAL = 2     # 48 MHz
SYSTEM_FAST = 3       # 133 MHz
SYSTEM_TURBO = 4      # 250 MHz

# Screen size
WIDTH = 296
HEIGHT = 128

# E Ink Pins
PIN_CS = 17
PIN_CLK = 18
PIN_MOSI = 19
PIN_DC = 20
PIN_RESET = 21
PIN_BUSY = 26

# Power Pins
PIN_VBUS_DETECT = 24
PIN_VREF_POWER = 27
PIN_1V2_REF = 28
PIN_BATTERY = 29
PIN_ENABLE_3V3 = 10

# LED Pin
PIN_LED = 25


class Badger2040:
    def __init__(self):
        print("Badger2040 Class init NOTICE: This class does not implement functionality, but only serves as a stub for documentation purposes.")
        pass

    @property
    def is_busy(self) -> bool:
        pass

    def set_update_speed(self, speed: int) -> None:
        """
        Badger 2040 is capable of updating the display at multiple different speeds.
        These offer a tradeoff between the quality of the final image and the speed of the update.
        There are currently four constants naming the different update speeds from 0 to 3:

        UPDATE_NORMAL - a normal update, great for display the first screen of your application and ensuring good contrast and no ghosting
        UPDATE_MEDIUM - a good balance of speed and clarity, you probably want this most of the time
        UPDATE_FAST - a fast update, good for stepping through screens such as the pages of a book or the launcher
        UPDATE_TURBO - a super fast update, prone to ghosting, great for making minor changes such as moving a cursor through a menu

        :param speed: one of the update constants
        :type speed: int
        """
        pass

    def update(self) -> None:
        """
        Starts a full update of the screen. Will block until the update has finished.

        Update takes no parameters, but the update time will vary depending on which set_update_speed you've selected.
        """
        pass

    def partial_update(self, x: int, y: int, w: int, h: int) -> None:
        """
        Starts a partial update of the screen. Will block until the update has finished.

        A partial update allows you to update a portion of the screen rather than the whole thing.

        That portion must be a multiple of 8 pixels tall, but can be any number of pixels wide.

        :param x: The x coordinate of the top left corner of the update area.
        :type x: int
        :param y: The y coordinate of the top left corner of the update area. Must be a multiple of 8.
        :type y: int
        :param w: The width of the update area.
        :type w: int
        :param h: The height of the update area. Must be a multiple of 8.
        :type h: int
        """
        pass

    @property
    def woken_by_button(self) -> bool:
        pass

    def halt(self) -> None:
        pass

    def led(self, brightness: int) -> None:
        """
        The white indicator LED can be controlled, with brightness ranging from 0 (off) to 255:
        :param brightness: The brightness of the LED. 0 - 255
        :type brightness: int
        """
        pass

    def set_font(self, font: str) -> None:
        """
        Set the font vector.
        "sans", "gothic", "cursive", "serif", "serif_italic", "bitmap6", "bitmap8", "bitmap14_outline"

        :param font: The font vector to set
        :type font: str
        """
        pass

    def set_pen(self, color: int) -> None:
        """
        Set the pen color. 0 to 15

        :param color: Brightness value, from 0 to 15
        :type color: int
        """
        pass

    def set_thickness(self, thickness: int) -> None:
        """
        Set the pen thickness in pixels.

        :param thickness: Pen thickness in pixels
        :type thickness: int
        """
        pass

    def pressed(self, button: int) -> bool:
        pass

    @property
    def pressed_to_wake(self, button: int) -> bool:
        pass

    def clear(self) -> None:
        """
        Before drawing again it can be useful to clear your display.

        clear fills the drawing buffer with the pen colour, giving you a clean slate.
        """
        pass

    def pixel(self, x: int, y: int) -> None:
        """
        Draw a pixel at the given coordinates.

        :param x: x coordinate to draw at
        :type x: int
        :param y: y coordinate to draw at
        :type y: int
        """
        pass

    def command(self, reg: int, data) -> None:
        pass

    def line(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Draw a line from (x1, y1) to (x2, y2).

        :param x1: x coordinate of start point
        :type x1: int
        :param y1: y coordinate of start point
        :type y1: int
        :param x2: x coordinate of end point
        :type x2: int
        :param y2: y coordinate of end point
        :type y2: int
        """
        pass

    def rectangle(self, x: int, y: int, w: int, h: int) -> None:
        """
        Draw a rectangle at the given coordinates.

        :param x: x coordinate of top left corner
        :type x: int
        :param y: y coordinate of top left corner
        :type y: int
        :param w: width of rectangle
        :type w: int
        :param h: height of rectangle
        :type h: int
        """
        pass

    def text(
        self,
        message: str,
        x: int,
        y: int,
        scale: float = None,
        rotation: float = None,
        letter_spacing: int = 1,
    ) -> None:
        """
        Draw text on the screen.

        :param message: The text to draw
        :type message: str
        :param x: The x coordinate to draw the text at for left middle alignment
        :type x: int
        :param y: The y coordinate to draw the text at for left middle alignment
        :type y: int
        :param scale: size of text
        :type scale: float
        :param rotation: rotation of text in degrees
        :type rotation: float
        :param letter_spacing:
        :type letter_spacing: int
        """
        pass

    def glyph(self, char: str, x: int, y: int, scale: float = None, rotation: float = None) -> None:
        pass

    def measure_text(self, message: str, scale: float = None, letter_spacing: int = 1) -> int:
        """
        Measure the width of a string of text.

        :param message: The text to measure
        :type message: str
        :param scale: The size of the text
        :type scale: float
        :param letter_spacing:
        :type letter_spacing: int
        """
        pass

    def measure_glyph(self, char: str, scale: float = None) -> int:
        pass

    @staticmethod
    def set_system_speed(selected_speed: int) -> None:
        pass

    @staticmethod
    def system_speed(speed) -> None:
        pass

