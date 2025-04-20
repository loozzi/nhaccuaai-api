import random
import string


def gen_permalink(num: int = 22) -> str:
    """
    Generate a permalink based on the given number.
    """
    s = ""
    _ = string.ascii_letters + string.digits
    for i in range(1, num + 1):
        s += random.choice(_)

    return s
