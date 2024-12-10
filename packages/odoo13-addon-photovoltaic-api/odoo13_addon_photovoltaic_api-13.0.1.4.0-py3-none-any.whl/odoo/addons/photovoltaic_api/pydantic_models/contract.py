from typing import Optional
from datetime import date
from . import OrmModel
from .power_station import PowerStationShort


class Contract(OrmModel):
    id: int
    name: str
    date: date
    power_plant: PowerStationShort
    peak_power: float
    stage: str
    generated_power: float
    tn_co2_avoided: float
    eq_family_consumption: float
    sent_state: Optional[str]
    product_mode: str
    payment_period: Optional[str]
    investment: float
    bank_account: str
    percentage_invested: float
    crece_solar_activated: bool


class ContractIn(OrmModel):
    investment: float
    power_plant: int
    product_mode: str
