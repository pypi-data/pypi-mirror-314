from yta_general_utils.programming.parameter_validator import PythonValidator
from yta_general_utils.color.regex import ColorRegularExpression
from yta_general_utils.color.enums import ColorString
from colorsys import rgb_to_hsv as _rgb_to_hsv, hsv_to_rgb as _hsv_to_rgb
from typing import Union


def is_hexadecimal_color(color):
    """
    Check that the 'color' parameter is an hexadecimal
    color.
    """
    return ColorRegularExpression.HEX.parse(color)

def is_string_color(color):
    """
    Check that the 'color' parameter is an string 
    color accepted by our system, whose value is an
    hexadecimal value.
    """
    return ColorString.is_valid(color)

def is_array_or_tuple_without_alpha_normalized(color):
    """
    Check that the 'color' parameter is an array or a
    tuple of 3 elements that are float values between
    0 and 1 (normalized value).
    """
    return (
        is_array_or_tuple_without_alpha and
        all(
            PythonValidator.is_instance(c, float) and
            0 <= c <= 1
            for c in color
        )
    )

def is_array_or_tuple_with_alpha_normalized(color):
    """
    Check that the 'color' parameter is an array or a
    tuple of 4 elements that are float values between
    0 and 1 (normalized value).
    """
    return (
        is_array_or_tuple_with_alpha and
        all(
            PythonValidator.is_instance(c, float) and 
            0 <= c <= 1
            for c in color
        )
    )

def is_array_or_tuple_without_alpha(color):
    """
    Check that the 'color' parameter is an array or a
    tuple of 3 elements that are int values between 0
    and 255.
    """
    return (
        PythonValidator.is_instance(color, [tuple, list]) and
        len(color) == 3 and
        all(
            PythonValidator.is_instance(c, int) and
            0 <= c <= 255
            for c in color
        )
    )

def is_array_or_tuple_with_alpha(color):
    """
    Check that the 'color' parameter is an array or a
    tuple of 4 elements that are int values between 0
    and 255.
    """
    return (
        PythonValidator.is_instance(color, [tuple, list]) and
        len(color) == 4 and
        all(
            PythonValidator.is_instance(c, int) and
            0 <= c <= 255
            for c in color
        )
    )

def parse_rgb_color(color):
    """
    Parse the provided 'color' as RGB and returns it as
    r,g,b values.
    """
    if is_array_or_tuple_without_alpha_normalized(color):
        return color[0] * 255, color[1] * 255, color[2] * 255
    elif is_array_or_tuple_without_alpha(color):
        return color[0], color[1], color[2]
    else:
        raise Exception(f'The provided "color" parameter is not an RGB color.')

def parse_rgba_color(color):
    """
    Parse the provided 'color' as RGBA and returns it as
    r,g,b,a values.
    """
    if is_array_or_tuple_with_alpha_normalized(color):
        return color[0] * 255, color[1] * 255, color[2] * 255, color[3] * 255
    elif is_array_or_tuple_with_alpha(color):
        return color[0], color[1], color[2], color[3]
    else:
        raise Exception(f'The provided "color" parameter is not an RGBA color.')
    


def parse_color(color: Union[str, list, tuple]):
    """
    Tries to parse the provided 'color' and returns it
    as an RGBA if parseable, or None if not.
    """
    # As string color
    string_color = None
    try:
        string_color = ColorString.to_enum(color)
    except:
        pass

    color_array = None
    if string_color is not None:
        color_array = hex_to_rgba(string_color.value)
    # A hexadecimal string
    elif PythonValidator.is_string(color) and is_hexadecimal_color(color):
        color_array = hex_to_rgba(color)
    else:
        # RGBA color
        try:
            color_array = parse_rgba_color(color)
        except:
            pass

        # RGB color
        try:
            color_array = *parse_rgb_color(color), 0
        except:
            pass

    # TODO: What about HSL, CYMK, etc. (?)

    return color_array
    
# These methods below are just actioners, they don't
# check anything as they will be used by a class that
# validates everything before using these methods.
def hex_to_rgba(hex_color: str):
    # Hex can start with '0x', '0X' or '#'
    hex = hex_color.lstrip('#').lstrip('0x').lstrip('0X')
    if len(hex) == 8:
        # hex with alpha
        r, g, b, a = (int(hex[i:i+2], 16) for i in (0, 2, 4, 6))
    elif len(hex) == 6:
        # hex without alpha
        r, g, b, a = *(int(hex[i:i+2], 16) for i in (0, 2, 4)), 0
    
    return r, g, b, a

def hex_to_rgb(hex_color: str):
    r, g, b, _ = hex_to_rgba(hex_color)

    return r, g, b

def rgb_to_hex(rgb_color: list, do_include_alpha: bool = False):
    r, g, b = parse_rgb_color(rgb_color)

    return rgba_to_hex([r, g, b, 255], do_include_alpha)

def rgba_to_hex(rgba_color: list, do_include_alpha: bool = False):
    r, g, b, a = parse_rgba_color(rgba_color)

    hex = "#{:02x}{:02x}{:02x}".format(r, g, b)
    if do_include_alpha:
        hex = "#{:02x}{:02x}{:02x}{:02x}".format(r, g, b, a)

    return hex

def rgba_to_hsl(rgba_color: list):
    r, g, b, _ = parse_rgba_color(rgba_color)

    return rgb_to_hsl([r, g, b])

def rgb_to_hsl(rgb_color: list):
    r, g, b = parse_rgb_color(rgb_color)

    # Values normalization
    r /= 255.0
    g /= 255.0
    b /= 255.0
    
    # Max and minimum values for RGB
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    delta = cmax - cmin

    # Tone (H)
    if delta == 0:
        h = 0  # No difference => undefined (gray) tone
    elif cmax == r:
        h = (60 * ((g - b) / delta) + 360) % 360
    elif cmax == g:
        h = (60 * ((b - r) / delta) + 120) % 360
    else:  # cmax == b
        h = (60 * ((r - g) / delta) + 240) % 360
    
    # Luminosity (L)
    l = (cmax + cmin) / 2
    
    # Saturation (S)
    if delta == 0:
        s = 0  # No difference => saturation is 0
    else:
        s = delta / (1 - abs(2 * l - 1)) if l != 0 and l != 1 else delta / (2 - (cmax + cmin))

    # TODO: I saw in some online solutions that they offer
    # the results without decimal figures
    return round(h, 2), round(s * 100, 2), round(l * 100, 2)

# TODO: Add 'hsl_to_rgb'
# TODO: Add 'hsl_to_rgba'

def rgb_to_cymk(rgb_color: list):
    r, g, b = parse_rgb_color(rgb_color)

    r, g, b = r / 255.0, g / 255.0, b / 255.0

    k = 1 - max(r, g, b)

    if k == 1:
        c = m = y = 0
    else:
        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)

    # TODO: I saw in some online solutions that they offer
    # the results without decimal figures
    return round(c * 100, 2), round(m * 100, 2), round(y * 100, 2), round(k * 100, 2)

def rgb_to_hsv(rgb_color):
    r, g, b = parse_rgb_color(rgb_color)

    # TODO: Assume this is not normalized
    return _rgb_to_hsv(r, g, b)

def rgba_to_hsv(rgba_color):
    r, g, b, _ = parse_rgba_color(rgba_color)
    
    # TODO: Assume this is not normalized
    return _rgb_to_hsv(r, g, b)

def hsv_to_rgb(h, s, v):
    # TODO: Assume this is not normalized
    return _hsv_to_rgb(h, s, v)

def hsv_to_rgba(h, s, v):
    # TODO: Assume this is not normalized
    return *hsv_to_rgb(h, s, v), 255


