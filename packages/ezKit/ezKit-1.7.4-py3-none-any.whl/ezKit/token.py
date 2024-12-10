import json

from .cipher import AESCipher
from .utils import datetime_now, datetime_offset, datetime_string_to_datetime, datetime_to_string, v_true


def generate_token(key: str = 'Fc0zXCmGKd7tPu6W', timeout: int = 3600, data: any = None) -> None | str:
    try:
        source = json.dumps(
            obj={
                'datetime': datetime_to_string(datetime_offset(datetime_now(), seconds=+timeout)),
                'data': data
            },
            default=str
        )
        cipher = AESCipher(key=key, algorithm='sha256')
        return cipher.encrypt(source)
    except:
        return None


def parsing_token(token_string: str, key: str = 'Fc0zXCmGKd7tPu6W') -> None | dict:
    try:
        if v_true(token_string, str):
            cipher = AESCipher(key=key, algorithm='sha256')
            source: dict = json.loads(cipher.decrypt(token_string))
            source['datetime'] = datetime_string_to_datetime(source['datetime'])
            return source
        else:
            return None
    except:
        return None


def certify_token(token_string: str, key: str = 'Fc0zXCmGKd7tPu6W') -> bool:
    try:
        result = parsing_token(token_string, key)
        if not v_true(result, dict):
            return False
        if result.get('datetime') < datetime_now():
            return False
        return True
    except:
        return False
