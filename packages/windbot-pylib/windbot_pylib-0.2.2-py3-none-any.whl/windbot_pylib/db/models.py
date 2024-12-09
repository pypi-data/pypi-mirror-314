from geoalchemy2 import Geometry
from sqlalchemy import ForeignKey, Integer, TIMESTAMP, DECIMAL, VARCHAR, DATETIME, BOOLEAN
from sqlalchemy.dialects.mysql import MEDIUMINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy.sql import func
from typing import List


DBBase = declarative_base()


class DBStationModel(DBBase):
    __tablename__ = "synoptic_station"

    id = mapped_column(Integer, primary_key=True)
    coordinates = mapped_column(Geometry("POINT"), nullable=False)
    date_added = mapped_column(TIMESTAMP, nullable=False, default=func.now())
    elev_dem = mapped_column(DECIMAL(7, 2))
    elevation = mapped_column(DECIMAL(5, 2))
    mnet_id = mapped_column(VARCHAR(8))
    name = mapped_column(VARCHAR(64), nullable=False)
    state = mapped_column(VARCHAR(32), nullable=False)
    status = mapped_column(VARCHAR(32))
    ts_interval = mapped_column(MEDIUMINT)
    timezone = mapped_column(VARCHAR(32))
    stid = mapped_column(VARCHAR(16))
    observations: Mapped[List["DBStationObservationModel"]] = relationship(back_populates="station")
    # observations_precip = Mapped[List["DBStationObservationPrecip"]] = relationship(back_populates="station")


class DBStationObservationModel(DBBase):
    __tablename__ = "synoptic_station_observation"

    id = mapped_column(Integer, primary_key=True)
    date_added = mapped_column(TIMESTAMP, nullable=False, default=func.now())
    date_modified = mapped_column(TIMESTAMP, nullable=False, default=func.now())

    air_temp = mapped_column(DECIMAL(6, 3))
    air_temp_d = mapped_column(BOOLEAN, default=False)

    altimeter = mapped_column(DECIMAL(9, 3))
    altimeter_d = mapped_column(BOOLEAN, default=False)

    date_time = mapped_column(DATETIME, nullable=False)  # observation datetime

    dew_point_temp = mapped_column(DECIMAL(6, 3))
    dew_point_temp_d = mapped_column(BOOLEAN, default=False)

    pressure = mapped_column(DECIMAL(8, 2))
    pressure_d = mapped_column(BOOLEAN, default=False)

    relative_humidity = mapped_column(DECIMAL(5, 2))
    relative_humidity_d = mapped_column(BOOLEAN, default=False)

    station_id = mapped_column(ForeignKey("synoptic_station.id"))
    station: Mapped["DBStationModel"] = relationship(back_populates="observations")

    wind_dir = mapped_column(DECIMAL(4, 1))
    wind_dir_d = mapped_column(BOOLEAN)

    wind_gust = mapped_column(DECIMAL(4, 1))
    wind_gust_d = mapped_column(BOOLEAN, default=False)

    wind_speed = mapped_column(DECIMAL(6, 3))
    wind_speed_d = mapped_column(BOOLEAN, default=False)


class DBSynopticVarModel(DBBase):
    __tablename__ = "synoptic_var"

    id = mapped_column(Integer, primary_key=True)
    date_added = mapped_column(TIMESTAMP, nullable=False, default=func.now())
    date_modified = mapped_column(TIMESTAMP, nullable=False, default=func.now())

    long_name = mapped_column(VARCHAR(128), index=True, unique=True)
    unit = mapped_column(VARCHAR(32))
    name = mapped_column(VARCHAR(64), nullable=False, unique=True)


class DBUserModel(DBBase):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(VARCHAR(64), unique=True, index=True)
    email = mapped_column(VARCHAR(320), unique=True, index=True)
    pass_hash = mapped_column(VARCHAR(512), nullable=False)
    first_name = mapped_column(VARCHAR(32), nullable=True)
    last_name = mapped_column(VARCHAR(32), nullable=True)
    role_id = mapped_column(Integer, ForeignKey("user_role.id"), index=True)
    role = relationship("DBUserRoleModel", foreign_keys=[role_id])
    date_added = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())
    date_modified = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())


class DBUserRoleModel(DBBase):
    __tablename__ = "user_role"

    id = mapped_column(Integer, primary_key=True)
    role = mapped_column(VARCHAR(64), unique=True, nullable=False)
