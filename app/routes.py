from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.db import SessionLocal, Base, engine
from app.models import GeographicalAddress, Country, GeographicLocation, GeographicSubAddress
from app.schemas import GeographicalAddressCreate, GeographicalAddressUpdate, GeographicalAddressResponse
import json

app = FastAPI()

router = APIRouter()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create tables
# Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)


@router.post("/addresses/", response_model=GeographicalAddressResponse)
def create_address(
        address_data: GeographicalAddressCreate,
        db: Session = Depends(get_db)
):
    # Convert related objects to JSON serializable data
    country_codes = [country.dict() for country in address_data.country_code]
    geographic_locations = [location.dict() for location in address_data.geographic_location]
    geographic_sub_addresses = [sub_address.dict() for sub_address in address_data.geographic_sub_address]

    address_dict = address_data.dict()
    address_dict.pop("country_code")
    address_dict.pop("geographic_location")
    address_dict.pop("geographic_sub_address")

    print(country_codes)
    address_db = GeographicalAddress(
        **address_data.dict(),
        country_code=country_codes,
        geographic_location=geographic_locations,
        geographic_sub_address=geographic_sub_addresses
    )
    country_code_instances = []
    for country_code in country_codes:
        country_db = Country(**country_code)
        country_code_instances.append(country_db)
        db.add(country_db)

    geographic_location_instances = []

    for geographic_location in geographic_locations:
        geographic_location_db = GeographicLocation(**geographic_location)
        geographic_location_instances.append(geographic_location_db)
        db.add(geographic_location_db)

    geographic_sub_address_instances = []
    for geographic_sub_address in geographic_sub_addresses:
        geographic_sub_address_db = GeographicSubAddress(**geographic_sub_address)
        geographic_sub_address_instances.append(geographic_sub_address_db)
        db.add(geographic_sub_address_db)

    print(country_code_instances)
    address_db.country_code = country_code_instances
    address_db.geographic_location = geographic_location_instances
    address_db.geographic_sub_address = geographic_sub_address_instances
    db.add(address_db)
    db.commit()
    db.refresh(address_db)
    return address_db


@router.get("/addresses/", response_model=list[GeographicalAddressResponse])
def read_address(db: Session = Depends(get_db)):
    addresses = db.query(GeographicalAddress).all()
    return addresses


@router.patch("/addresses/{address_id}", response_model=GeographicalAddressResponse)
def update_address(address_id: str, updated_data: GeographicalAddressUpdate, db: Session = Depends(get_db)):
    address = db.query(GeographicalAddress).filter(GeographicalAddress.id == address_id).first()
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")

    for key, value in updated_data.dict().items():
        setattr(address, key, value)

    db.commit()
    db.refresh(address)
    return address
