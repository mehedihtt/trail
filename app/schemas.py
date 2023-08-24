from pydantic import BaseModel
from typing import List


class CountryCreate(BaseModel):
    format: str
    href: str
    value: str


class GeographicLocationCreate(BaseModel):
    name: str
    href: str
    bbox: int


class GeographicSubAddressCreate(BaseModel):
    href: str
    building_name: str
    level_number: str
    level_type: str
    name: str
    private_street_name: str
    private_street_number: str
    sub_address_type: str
    sub_unit_number: str
    sub_unit_type: str


class GeographicalAddressCreate(BaseModel):
    href: str
    city: str
    geographic_address_type: str
    locality: str
    name: str
    postcode: str
    state_or_province: str
    street_name: str
    street_nr: str
    street_nr_last: str
    street_nr_last_suffix: str
    street_nr_suffix: str
    street_suffix: str
    street_type: str
    country_code: List[CountryCreate]
    geographic_location: List[GeographicLocationCreate]
    geographic_sub_address: List[GeographicSubAddressCreate]


class GeographicalAddressUpdate(BaseModel):
    href: str
    city: str
    locality: str
    name: str
    postcode: str
    state_or_province: str
    street_name: str
    street_nr: str
    street_nr_last: str
    street_nr_last_suffix: str
    street_nr_suffix: str
    street_suffix: str
    street_type: str


class CountryResponse(BaseModel):
    id: str
    href: str
    format: str
    value: str


class GeographicLocationResponse(BaseModel):
    id: str
    name: str
    href: str
    bbox: int


class GeographicSubAddressResponse(BaseModel):
    id: str
    href: str
    building_name: str
    level_number: str
    level_type: str
    name: str
    private_street_name: str
    private_street_number: str
    sub_address_type: str
    sub_unit_number: str
    sub_unit_type: str


class GeographicalAddressResponse(BaseModel):
    id: str
    href: str
    city: str
    geographic_address_type: str
    locality: str
    name: str
    postcode: str
    state_or_province: str
    street_name: str
    street_nr: str
    street_nr_last: str
    street_nr_last_suffix: str
    street_nr_suffix: str
    street_suffix: str
    street_type: str
    country_code: List[CountryResponse]
    geographic_location: List[GeographicLocationResponse]
    geographic_sub_address: List[GeographicSubAddressResponse]
