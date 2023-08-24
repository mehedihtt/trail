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

    # Create instances of related models and add them to the session
    country_code_instances = [Country(**country) for country in country_codes]
    geographic_location_instances = [GeographicLocation(**location) for location in geographic_locations]
    geographic_sub_address_instances = [GeographicSubAddress(**sub_address) for sub_address in geographic_sub_addresses]

    for country_instance in country_code_instances:
        db.add(country_instance)

    for location_instance in geographic_location_instances:
        db.add(location_instance)

    for sub_address_instance in geographic_sub_address_instances:
        db.add(sub_address_instance)

    # db.commit()  # Commit related instances before creating the address

    # Create GeographicalAddress instance and associate foreign keys
    address_dict = address_data.dict()
    address_dict.pop("country_code")
    address_dict.pop("geographic_location")
    address_dict.pop("geographic_sub_address")

    # Create GeographicalAddress instance and associate foreign keys
    address_db = GeographicalAddress(**address_dict)
    db.add(address_db)
    db.commit()
    address_db.country_code = [country_instance.id for country_instance in country_code_instances]
    address_db.geographic_location = [location_instance.id for location_instance in geographic_location_instances]
    address_db.geographic_sub_address = [sub_address_instance.id for sub_address_instance in geographic_sub_address_instances]

    # for country_code in country_code_instances:
    #     # country_db = Country(**country_code)
    #     print(country_code)
    #     address_db.country_code = country_code.id
    #     # db.add(country_db)

    # for geographic_location in geographic_location_instances:
    #     # geographic_location_db = Country(**geographic_location)
    #     address_db.geographic_location.append(geographic_location)
    #     # db.add(geographic_location_db)
    #
    #
    # for geographic_sub_address in geographic_sub_address_instances:
    #     geographic_sub_address_db = Country(**geographic_sub_address)
    #     address_db.geographic_sub_address.append(geographic_sub_address_db)
    #     db.add(geographic_sub_address_db)
    # for geographic_location in country_codes:
    #     country_db = Country(**country_code)
    #     address_db.country_code.append(country_db)
    #     db.add(country_db)

    # db.add(address_db)
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
