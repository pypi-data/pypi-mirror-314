from yta_general_utils.web.tiktok.url_parser import parse_tiktok_url
from yta_general_utils.downloader import Downloader
from yta_general_utils.file.writer import FileWriter
from yta_general_utils.programming.parameter_validator import PythonValidator
from typing import Union


DOWNLOAD_CDN_URL = 'https://tikcdn.io/ssstik/' # + video_id to download

# TODO: Make this work also with video_id (?)
def get_tiktok_video(url: str, output_filename: Union[str, None] = None):
    """
    Obtains the Tiktok video from the provided 'url' if 
    valid and stores it locally if 'output_filename' is
    provided, or returns it if not.
    """
    if not PythonValidator.is_string(url):
        raise Exception('The provided "url" parameter is not a string.')

    tiktok_video_info = parse_tiktok_url(url)

    download_url = DOWNLOAD_CDN_URL + tiktok_video_info['video_id']

    video_content = Downloader.download_video(download_url)

    if output_filename:
        FileWriter.write_binary_file(video_content, output_filename)

    return video_content

# TODO: Make this work also with video_id (?)
def download_tiktok_video(url: str, output_filename: str):
    """
    Obtains the Tiktok video from the provided 'url' if 
    valid and stores it locally as 'output_filename'.
    """
    if not PythonValidator.is_string(url):
        raise Exception('The provided "url" parameter is not a string.')
    
    if not output_filename:
        raise Exception('No "output_filename" provided to save the file.')
    
    return get_tiktok_video(url, output_filename)