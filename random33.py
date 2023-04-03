import random
import string

upc = random.choices(string.ascii_uppercase + string.digits, k=12)
print(upc)
