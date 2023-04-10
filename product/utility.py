import random
import string


def generate_upc(self) -> str:
    """Generate a random 12-character string of uppercase letters and digits"""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
