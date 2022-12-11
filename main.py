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
    status_code=status.HTTP_200_OK,
    tags=["Home"]
    )
def home():
    """
    # home

    ## Returns:
        Body(): Return a response body with a greeting message.
    """
    return {"Hello": "world"}

# Request and Response Body


@app.post(
    path="/person/new",
    status_code=status.HTTP_201_CREATED,
    response_model=PersonOut,
    tags=["Person"],
    summary="Create person in the app"
    ) # This is the response_model
def create_person(person: Person = Body(...)):
    """
    # create_person
    
    This path operation function creates a person in the app and save the information in the database.

    ## Args:
    
        -person (Person): Person model.
            - first_name (str): User first name.
            - last_name (str): User last name.
            - age (int): User age.
            - hair_color (HairColor, optional): User hair color. Defaults to None.
            - is_married (bool, optional): User married status. Defaults to None.
            - email (EmailStr): User email.


    ## Returns:
    
        Body(): Person model.
    """
    return person

# Validations: Query parameters
## Query and path parameters can set authomatic examples with key example in pydantic Field


@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Person"],
    summary="Get Person detail",
    deprecated=True
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
    """
    # show_person
    
    This endpoint recives query parameters and returns a respose body with the person id seted.

    ## Args:
    
        - name (Optional[str], optional): Person name.
        - age (int): Person age. 

    ## Returns:
    
        Body: Return a response body with user name as key and age as value.
    """
    return {name: age}

# Validations: Path Parameters

persons = [1, 2, 3, 4, 5]

@app.get(
    path="/person/detail{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Person"],
    summary="Get person detail"
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
    """
    # show_person
    
    

    ## Args:
    
        - person_id (int): Person ID.

    ## Raises:
    
        HTTPException: If the ID doesn't exists, return a persolalized error exception message.

    ##Returns:
    
        Body(): Return a response body with a value informs that ID exists.
    """
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person doesn't exists!"
        )
    return {person_id: "It exists!"}

# Validations: Request Body


@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Person"],
    summary="Update person data"
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
    """
    # update_person
    
    This path operation updates information from person model and location model.

    ## Args:
    
        - person_id (int): Person ID.
        - person (Person): Person model.
            - first_name (str): User first name.
            - last_name (str): User last name.
            - age (int): User age.
            - hair_color (HairColor, optional): User hair color. Defaults to None.
            - is_married (bool, optional): User married status. Defaults to None.
            - email (EmailStr): User email.
        - location (Location): Location model.
            - city (str): Person City.
            - state (str): Person State.
            - country (str): Person Country.

    ## Returns:
    
        Body(): Person model.
        Body(): Location model.
    """
    results = person.dict()
    results.update(location.dict())
    return results

@app.put(
    path="/person/location/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Person"],
    summary="Update persn location data"
    )
def updat_location(
    person_id: int = Path(
        ...,
        titel="Person ID",
        description="This is the person ID",
        gt=0,
        example=333,
        deprecated=True
    ),
    location: Location = Body(...)
):
    """
    # updat_location
    
    This path operation recives a Person ID and updates de location model.

    ## Args:

        - person_id (int): Person ID.
        - location (Location): Location model.
            - city (str): Person City.
            - state (str): Person State.
            - country (str): Person Country.

    ## Returns:
    
        Body(): Location model.
    """
    return location

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["Person"],
    summary="Login area"
)
def login(
    username: str = Form(...),
    password: str = Form(...)
    ):
    """
    # login
    
    This form allows to login using username and password.

    ## Args:
        username (str): Person username.
        password (str): Person password.

    ## Returns:
    
        Body(): Return a response body with de username and a message of succesfuly login.
    """
    return LoginOut(
        username=username
        ) # We need to instance the LoginOut CLASS method to return the response

# Cookies and headers parameters


@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Form"],
    summary="Contact area"
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
    """
    # contact
    
    

    ## Args:
    
        - first_name (str): Person name.
        - last_name (str): Person last name.
        - email (EmailStr): Person email.
        - message (str): Message to be send.
        - user_agent (Optional[str], optional): Web browser data. Defaults to Header(default=None).
        - ads (Optional[str], optional): Web browser cookies. Defaults to Cookie(default=None).

    ## Returns:
    
        Body(): Returns the Web browser data.
    """
    return user_agent


@app.post(
    path="/post-image",
    tags=["Upload"],
    summary="Image upload"
)
def post_image(
    image: UploadFile = File(...)
):
    """
    # post_image
    
    This form recives an image file and return its technical data.

    ## Args:
    
        image (UploadFile): Image file.

    ## Returns:
    
        Body(): Return a ressponse body with the technical data about the image.
    """
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }