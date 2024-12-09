from yta_general_utils.programming.regular_expressions import GeneralRegularExpression
from yta_general_utils.programming.parameter_validator import PythonValidator

import requests


# TODO: Refactor this, simplify and create a
# TiktokUrlParser class
def __is_short_tiktok_url(url: str):
    if not PythonValidator.is_string(url):
        raise Exception('The provided "url" parameter is not a string.')
    
    return GeneralRegularExpression.TIKTOK_SHORT_VIDEO_URL.parse(url)

def __is_long_tiktok_url(url: str):
    if not PythonValidator.is_string(url):
        raise Exception('The provided "url" parameter is not a string.')
    
    return GeneralRegularExpression.TIKTOK_LONG_VIDEO_URL.parse(url)

def __short_tiktok_url_to_long_tiktok_url(url: str):
    """
    Transforms the provided short tiktok 'url' to 
    the long format and returns it.
    """
    if not PythonValidator.is_string(url):
        raise Exception('The provided "url" parameter is not a string.')
    
    if not __is_short_tiktok_url(url):
        raise Exception('No "url" provided is not a short tiktok url.')

    return requests.get(url).url

def __clean(url: str):
    """
    Removes any additional parameter that is after a
    question mark sign.
    """
    if not PythonValidator.is_string(url):
        raise Exception('The provided "url" parameter is not a string.')

    if '?' in url:
        url = url.split('?')[0]

    return url

def is_valid_tiktok_url(url: str):
    """
    This method returns True if the provided 'url' is a
    valid long or short tiktok video url or False if not.
    """
    if not PythonValidator.is_string(url):
        raise Exception('The provided "url" parameter is not a string.')
    
    return __is_short_tiktok_url(url) or __is_long_tiktok_url(url)

def parse_tiktok_url(url: str):
    """
    Parses the provided 'url' returning a dict with that
    'url' (long version) and also the 'username' and the
    'video_id' if it is a valid url. It will raise an 
    Exception if not valid 'url' provided.
    """
    if not PythonValidator.is_string(url):
        raise Exception('The provided "url" parameter is not a string.')

    if not is_valid_tiktok_url(url):
        raise Exception('The provided "url" is not a valid tiktok video url.')
    
    url = __clean(url)
    if not __is_long_tiktok_url(url):
        url = __short_tiktok_url_to_long_tiktok_url(url)

    aux = url.split('/')

    data = {
        'username': aux[len(aux) - 3],
        'video_id': aux[len(aux) - 1],
        'url': url,
    }

    return data
    

    