from bcrypt import checkpw
from bcrypt import hashpw
from bcrypt import gensalt


def get_hash(_str):
    pwhash = hashpw(_str.encode('utf-8'), gensalt())
    return pwhash.decode('utf-8')


def check_hash(_ustr, _hstr):
    expected = _hstr.encode('utf-8')
    return checkpw(_ustr.encode('utf-8'), expected)
