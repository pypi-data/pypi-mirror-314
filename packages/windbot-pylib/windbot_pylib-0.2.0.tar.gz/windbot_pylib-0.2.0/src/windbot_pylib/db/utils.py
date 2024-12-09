from utils import get_env_secret
from db.models import DBStationModel

# from clients.synoptic.models import SynopticStation


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


def synoptic_station_to_db_station(station) -> DBStationModel:
    """Converts a synoptic station model to a db model

    Args:
        station (SynopticStation): station model

    Returns:
        DBStationModel: database station model
    """
    return DBStationModel(
        coordinates=f"POINT({station.latitude} {station.longitude})",
        elev_dem=station.elev_dem,
        elevation=station.elevation,
        mnet_id=station.mnet_id,
        name=station.name,
        state=station.state,
        status=station.status,
        timezone=station.timezone,
        stid=station.stid,
    )
