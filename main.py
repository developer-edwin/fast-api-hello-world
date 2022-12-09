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
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path
from fastapi import Form
from fastapi import Header, Cookie
from fastapi import File, UploadFile

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


class PersonBase(BaseModel): # We create this clss to implement inheritance with Person and PersonOUT classes
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


class Person(PersonBase):
    password: str = Field(
        ...,
        min_length=8
    )


class PersonOut(PersonBase):
    pass


class LoginOut(BaseModel):
    username: str = Field(
        ...,
        max_length=20,
        example="username2022"
    )
    message: str = Field(default="Login Succesfully!")

@app.get(
    path="/",
    status_code=status.HTTP_200_OK
    )
def home():
    return {"Hello": "world"}

# Request and Response Body


@app.post(
    path="/person/new",
    status_code=status.HTTP_201_CREATED,
    response_model=PersonOut) # This is the response_model
def create_person(person: Person = Body(...)):
    return person

# Validations: Query parameters
## Query and path parameters can set authomatic examples with key example in pydantic Field


@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK
    )
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

persons = [1, 2, 3, 4, 5]

@app.get(
    path="/person/detail{person_id}",
    status_code=status.HTTP_200_OK
    )
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="This is the person ID and it's required",
        example=5
        )
):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person doesn't exists!"
        )
    return {person_id: "It exists!"}

# Validations: Request Body


@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK
    )
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

@app.put(
    path="/person/location/{person_id}",
    status_code=status.HTTP_200_OK
    )
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

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(
    username: str = Form(...),
    password: str = Form(...)
    ):
    return LoginOut(
        username=username
        ) # We need to instance the LoginOut CLASS method to return the response

# Cookies and headers parameters


@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length= 20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent


@app.post(
    path="/post-image"
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }