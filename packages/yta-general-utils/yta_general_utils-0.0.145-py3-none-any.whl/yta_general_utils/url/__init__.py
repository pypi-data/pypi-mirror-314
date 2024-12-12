from urllib import parse as url_parse


def encode_url_parameter(parameter: str):
    """
    Encode the provided 'parameter' to be able to send
    it throught as a url query parameter.

    This method will turn 'example message' to
    'example%20message'.
    """
    return url_parse.quote(parameter)