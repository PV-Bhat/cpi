
import random
import string

def generate_session_id(length=10):
    characters = string.ascii_letters + string.digits
    session_id = ''.join(random.choice(characters) for i in range(length))
    return session_id

if __name__ == "__main__":
    print(generate_session_id())
