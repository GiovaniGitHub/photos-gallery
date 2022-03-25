import os
import re

from project.utils.const import PHOTOS_EXTENSIONS, email_regex

def check_file_as_format_valid(filename):
    return filename.lower().endswith(PHOTOS_EXTENSIONS)


def check_email(email):
    if(re.fullmatch(email_regex, email)):
        return True
    return False


def get_extension(filename):
    _, extension = os.path.splitext(filename)
    return extension
