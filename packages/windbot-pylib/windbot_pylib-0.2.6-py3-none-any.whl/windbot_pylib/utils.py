import os


def get_env_secret(key: str, default: str | int = None, required: bool = True) -> str:
    """Pulls a secret out of an environment variable. If the secret value is a file path that starts with "/run/secrets/", it will read the secret from the file.

    Args:
        key (str): Environment variable name

    Returns:
        str: secret
    """
    secret = os.getenv(key)
    if secret and secret.startswith("/run/secrets/"):
        with open(secret, "r") as secret_file:
            secret = secret_file.readline()

    if not secret and default:
        secret = default
    elif not secret and required:
        raise Exception(f"Missing required env secret '{key}'!")

    return secret
