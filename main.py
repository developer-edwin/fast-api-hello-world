# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr
from pydantic import HttpUrl

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models


class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Campeche"
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Campeche"
    )
    country: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Mexico"
    )


class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    age: int = Field(
        ...,
        gt=18,
        le=115
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    email: EmailStr = Field(
        ...
    )
    personal_site: Optional[HttpUrl] = Field(default=None)
    password: str = Field(
        ...,
        min_length=8
    )
    
    ## We could do this or we can enter an extra field in each parameter as "example" as we can see in Location class

    class Config:
        schema_extra = {
            "example": { ## This key shold be always named "example"
                "first_name": "Azkur",
                "last_name": "Dev",
                "age": 38,
                "hair_color": HairColor.brown,
                "is_married": True,
                "email": "azkur.zone@gmail.com",
                "personal_site": "https://www.azkur.com",
                "password": "123454678"
            }
        }


class PersonOut(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    age: int = Field(
        ...,
        gt=18,
        le=115
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    email: EmailStr = Field(
        ...
    )
    personal_site: Optional[HttpUrl] = Field(default=None)


@app.get("/")
def home():
    return {"Hello": "world"}

# Request and Response Body


@app.post("/person/new", response_model=PersonOut) # This is the response_model
def create_person(person: Person = Body(...)):
    return person

# Validations: Query parameters
## Query and path parameters can set authomatic examples with key example in pydantic Field


@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters long",
        example="John"
        ),
    age: int = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required",
        example="30"
        )
):
    return {name: age}

# Validations: Path Parameters


@app.get("/person/detail{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="This is the person ID and it's required",
        example=123
        )
):
    return {person_id: "It exists!"}

# Validations: Request Body


@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
            ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=321
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results

@app.put("/person/location/{person_id}")
def updat_location(
    person_id: int = Path(
        ...,
        titel="Person ID",
        description="This is the person ID",
        gt=0,
        example=333
    ),
    location: Location = Body(...)
):
    return location
