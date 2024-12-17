import random

def generate_otp(length=6):
    """
    Generate a numeric OTP of the specified length.
    Default length is 6.
    """
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])
