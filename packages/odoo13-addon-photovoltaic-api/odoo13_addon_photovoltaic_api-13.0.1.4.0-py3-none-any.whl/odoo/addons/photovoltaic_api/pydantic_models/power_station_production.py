from datetime import date

from . import OrmModel


class PowerStationProduction(OrmModel):
    date: date
    energy_generated: float