from services.config import Config

def get_token() -> str:
    if path := Config["paths"]["token_file"]:
        with open(path, "r") as tf:
            return tf.read()
    else:
        raise TypeError()