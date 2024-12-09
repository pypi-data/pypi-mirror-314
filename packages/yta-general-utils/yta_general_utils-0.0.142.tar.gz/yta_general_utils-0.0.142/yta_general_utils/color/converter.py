from yta_general_utils.color.utils import is_hexadecimal_color, parse_rgba_color, rgba_to_hex, hex_to_rgba, rgb_to_hex, rgba_to_hex, rgb_to_hsl, rgb_to_cymk, rgb_to_hsv, hsv_to_rgb, rgba_to_hsv, parse_color, hsv_to_rgba
from yta_general_utils.programming.parameter_validator import PythonValidator
from typing import Union


class ColorConverter:
    """
    Class to simplify and encapsulate the functionality related
    to color conversion.
    """
    @staticmethod
    def rgb_to_hex(red, green, blue):
        """
        Returns the provided RGB color as a hex color. The 'red', 'green' and
        'blue' parameters must be between 0 and 255.
        """
        return rgba_to_hex(red, green, blue)
    
    @staticmethod
    def hex_to_rgb(color: str):
        """
        Parse the provided hexadecimal 'color' parameter and
        turn it into an RGB color (returned as r,g,b) or
        raises an Exception if not.
        """
        r, g, b, _ = ColorConverter.hex_to_rgba(color)

        return r, g, b

    @staticmethod
    def hex_to_rgba(color: str):
        if not is_hexadecimal_color(color):
            raise Exception(f'The provided "color" parameter "{str(color)}" is not an hexadecimal color.')
        
        return hex_to_rgba(color)

    @staticmethod
    def rgb_to_hex(color: Union[tuple, list], do_include_alpha: bool = False):
        """
        Parse the provided RGB 'color' parameter and turn it to
        a hexadecimal color if valid or raises an Exception if
        not. The result will be #RRGGBB if 'do_include_alpha' is
        False, or #RRGGBBAA if 'do_include_alpha' is True.
        """
        validate_color(color)

        return rgb_to_hex(color, do_include_alpha)
        
    @staticmethod
    def rgba_to_hex(color: Union[tuple, list], do_include_alpha: bool = False):
        """
        Parse the provided RGBA 'color' parameter and turn it to
        a hexadecimal color if valid or raises an Exception if
        not. The result will be #RRGGBB if 'do_include_alpha' is
        False, or #RRGGBBAA if 'do_include_alpha' is True.
        """
        validate_color(color)

        return rgba_to_hex(color, do_include_alpha)

    @staticmethod
    def rgba_to_hsl(color: Union[tuple, list]):
        # TODO: Explain
        validate_color(color)

        _, _, _, a = parse_rgba_color(color)
        
        return *ColorConverter.rgb_to_hsl(color), a

    @staticmethod
    def rgb_to_hsl(color: Union[tuple, list]):
        # TODO: Explain
        validate_color(color)
        
        return rgb_to_hsl(color)

    @staticmethod
    def rgba_to_cymk(color: Union[tuple, list]):
        # TODO: Explain
        validate_color(color)

        color = color[:3]

        # TODO: Is there a way to handle alpha transparency
        # with a cymk (?)
        return ColorConverter.rgb_to_cymk(color)

    @staticmethod
    def rgb_to_cymk(color: Union[tuple, list]):
        # TODO: Explain
        # It looks like you need to know the color profile before
        # any conversion from RGB or RGBA
        # https://www.reddit.com/r/AdobeIllustrator/comments/17vpbod/different_cmyk_values_for_same_hex_code_which/?rdt=55781#:~:text=A%20hex%20code%20is%20an,information%2C%20like%20a%20colour%20profile.
        validate_color(color)

        return rgb_to_cymk(color)
    
    @staticmethod
    def rgb_to_hsv(color: Union[tuple, list]):
        """
        Turn the provided RGB 'color' into a HSV color.
        """
        validate_color(color)

        return rgb_to_hsv(color)

    @staticmethod
    def rgba_to_hsv(color: Union[tuple, list]):
        """
        Turn the provided RGBA 'color' into a HSV color.
        The HSV color doesn't pay attention to the alpha
        layer so this method is the same as using the
        'rgb_to_hsv' method for this 'color'.
        """
        validate_color(color)

        return rgba_to_hsv(color)
    
    @staticmethod
    def hsv_to_rgb(color: Union[tuple, list]):
        """
        Turn the provided HSV 'color' into a RGB color.
        """
        validate_color(color)
        
        h, s, v = color

        return hsv_to_rgb(h, s, v)
    
    @staticmethod
    def hsv_to_rgba(color: Union[tuple, list]):
        """
        Turn the provided HSV 'color' into a RGBA color.
        The HSV color doesn't pay attention to the alpha
        layer so it will be always one.
        """
        validate_color(color)

        h, s, v = color

        return hsv_to_rgba(h, s, v)
    
def validate_color(color: Union[tuple, list]):
    """
    Validate the provided 'color' as a tuple or list of 3
    or 4 elements.
    """
    if not PythonValidator.is_instance(color, 'Color') and parse_color(color) is None:
        raise Exception('The provided "color" is not a parsable color.')
    
    return True