from windbot_pylib.utils import get_env_secret


def mariadb_connector_url() -> str:
    """Returns a mariadb connector URL

    Returns:
        str: mariadb connector url
    """
    return "mariadb+mariadbconnector://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}".format(
        db_user=get_env_secret("DB_USER", "windbot"),
        db_pass=get_env_secret("DB_PASS", "password"),
        db_host=get_env_secret("DB_HOST", "127.0.0.1"),
        db_port=get_env_secret("DB_PORT", 3306),
        db_name=get_env_secret("DB_NAME", "windbot"),
    )
