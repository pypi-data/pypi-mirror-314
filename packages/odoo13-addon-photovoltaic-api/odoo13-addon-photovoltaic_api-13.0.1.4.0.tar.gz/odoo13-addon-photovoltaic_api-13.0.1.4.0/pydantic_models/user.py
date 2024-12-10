from typing import List, Optional

from pydantic import Field

from .bank_account import BankAccountOut
from .info import Country, State
from . import OrmModel


class UserShort(OrmModel):
    id:        Optional[int]
    firstname: Optional[str]
    lastname:  Optional[str]
    vat:       Optional[str]
    gender:    Optional[str] = Field(alias='gender_partner')
    birthday:  Optional[str]
    alias:     Optional[str]

class UserIn(OrmModel):
    person_type:          Optional[int] = Field(alias='person_type_id')
    firstname:            Optional[str]
    lastname:             Optional[str]
    street:               Optional[str]
    street2:              Optional[str] = Field(alias='additional_street')
    zip:                  Optional[str]
    city:                 Optional[str]
    state_id:             Optional[int]
    country_id:           Optional[int]
    email:                Optional[str]
    phone:                Optional[str]
    mobile:               Optional[str]
    alias:                Optional[str]
    vat:                  Optional[str]
    gender_partner:       Optional[str] = Field(alias='gender')
    birthday:             Optional[str]
    representative:       Optional[UserShort]
    about_us:             Optional[str]
    interests:            Optional[List[str]]

class UserOut(OrmModel):
    id:                int
    person_type:       str
    firstname:         str
    lastname:          str
    street:            str
    additional_street: Optional[str]
    zip:               str
    city:              str
    state:             Optional[State]
    country:           Optional[Country]
    email:             str
    phone:             Optional[str]
    mobile:            Optional[str]
    alias:             Optional[str]
    vat:               str
    gender:            Optional[str]
    birthday:          Optional[str]
    bank_accounts:     List[BankAccountOut]
    representative:    Optional[UserShort]
    about_us:          Optional[str]
    interests:         List[str]
