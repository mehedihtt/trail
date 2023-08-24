from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base
import uuid


class Country(Base):
    __tablename__ = "countries"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    href = Column(String)
    format = Column(String)
    value = Column(String)

class GeographicLocation(Base):
    __tablename__ = "geographic_locations"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    name = Column(String)
    href = Column(String)
    bbox = Column(Integer)

class GeographicSubAddress(Base):
    __tablename__ = "geographic_sub_addresses"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    href = Column(String)
    building_name = Column(String)
    level_number = Column(String)
    level_type = Column(String)
    name = Column(String)
    private_street_name = Column(String)
    private_street_number = Column(String)
    sub_address_type = Column(String)
    sub_unit_number = Column(String)
    sub_unit_type = Column(String)

class GeographicalAddress(Base):
    __tablename__ = "geographical_addresses"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    href = Column(String)
    city = Column(String)
    country = Column(String)
    geographic_address_type = Column(String, name="geographicAddressType")
    locality = Column(String)
    name = Column(String)
    postcode = Column(String)
    state_or_province = Column(String, name="stateOrProvince")
    street_name = Column(String, name="streetName")
    street_nr = Column(String, name="streetNr")
    street_nr_last = Column(String, name="streetNrLast")
    street_nr_last_suffix = Column(String, name="streetNrLastSuffix")
    street_nr_suffix = Column(String, name="streetNrSuffix")
    street_suffix = Column(String, name="streetSuffix")
    street_type = Column(String, name="streetType")
    country_code = Column(String, ForeignKey("countries.id"))
    country = relationship("Country")
    geographic_location_id = Column(String, ForeignKey("geographic_locations.id"))
    geographic_location_rel = relationship("GeographicLocation")
    geographic_sub_address = Column(String, ForeignKey("geographic_sub_addresses.id"))
    geographic_sub_address_rel = relationship("GeographicSubAddress")