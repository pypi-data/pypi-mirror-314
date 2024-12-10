from datetime import date
from typing import List, Optional

from pydantic import BaseModel

from .allocation import AllocationByYear
from . import OrmModel
from .power_station_production import PowerStationProduction


class PowerStation(OrmModel):
    id: int
    name: str
    display_name: Optional[str]
    image: Optional[str] 
    province: str
    city: str
    link_google_maps: str
    peak_power: str
    rated_power: str
    start_date: date
    monit_link: Optional[str]
    monit_user: Optional[str]
    monit_pass: Optional[str]
    tecnical_memory_link: Optional[str]
    annual_report_link: Optional[str]
    energy_generated: float
    tn_co2_avoided: float
    reservation: float
    contracts_count: int
    eq_family_consumption: float
    production: List[PowerStationProduction]
    allocations_by_year: List[AllocationByYear]

class PowerStationPublic(OrmModel):
    id: int
    name: str
    display_name: Optional[str]
    image: Optional[str] 
    province: str
    city: str
    link_google_maps: str
    peak_power: str
    rated_power: str
    start_date: date
    energy_generated: float
    tn_co2_avoided: float
    reservation: float
    contracts_count: int
    eq_family_consumption: float

class PowerStationShort(BaseModel):
    id: int
    name: str
    display_name: Optional[str]
    province: str
    city: str
