from . import OrmModel
from typing import List, Optional
from pydantic import Field


class Contact(OrmModel):
    id:                   Optional[int]
    firstname:            Optional[str]
    lastname:             Optional[str]
    street:               Optional[str]
    street2:              Optional[str] = Field(alias='additional_street')
    zip:                  Optional[str]
    city:                 Optional[str]
    state:                Optional[str]
    country:              Optional[str]
    email:                Optional[str]
    phone:                Optional[str]
    mobile:               Optional[str]
    alias:                Optional[str]
    vat:                  Optional[str]
    gender_partner:       Optional[str] = Field(alias='gender')
    birthday:             Optional[str]
    participation_reason: Optional[str]
    about_us:             Optional[str]
    comment:              Optional[str]
    is_chalet:            Optional[bool]
    personal_data_policy: Optional[bool]
    promotions:           Optional[bool]
    message_notes:        Optional[str]  # Notes
    tags:                 Optional[List[str]]
    minor:                Optional[bool] = Field(alias='is_minor') 
    tutor:                Optional[int]
