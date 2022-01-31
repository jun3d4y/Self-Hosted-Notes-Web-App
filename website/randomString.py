import random
import string

def get_random_string(length=30) :
    letters_pool = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_pool) for i in range(length))
