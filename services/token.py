from services.config import Config

class Token:
    @staticmethod
    def get() -> (None | str):
        if path := Config["paths"]["token_file"]:
            with open(path, "r") as tf:
                return tf.read()
        else:
            raise ValueError("paths.token_file is None")

__all__ = (
    "Token"
)
