def get_token() -> str:
    with open("data/TOKEN.env", "r") as tf:
        return tf.read()