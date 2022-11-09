
from base64 import b64encode
from tempfile import TemporaryFile

from .captcha import Captcha

def generate_captcha() -> dict:
    """
        Generates a captcha and returns a dictionary with its value and a string in base 64 of the associated image.
    """
    with TemporaryFile() as fp:
        captcha_to_send = Captcha()
        captcha_value = captcha_to_send.get_value()
        captcha_to_send.save(fp)
        fp.seek(0)
        b64_captcha = b64encode(fp.read()).decode(encoding='utf-8')
        src_b64_captcha = f"data:image/jpeg;charset=utf-8;base64,{b64_captcha}"

    return {
        'value' : captcha_value,
        'b64_data' : src_b64_captcha
    }