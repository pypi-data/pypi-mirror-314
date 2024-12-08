from typing import List, TypedDict

from fastapi import FastAPI

from .main import compare_async, init_web_view

app = FastAPI()


class User(TypedDict):
    public_id: str
    name: str
    age: int


class UsersResponse(TypedDict):
    users: List[User]


init_web_view(app=app, security_token="1234")


# example of a use case current in production
async def currentUseCase() -> UsersResponse:
    users = [
        User(public_id="1", name="John", age=30),
        User(public_id="2", name="Ane", age=20),
        User(public_id="3", name="Brook", age=38),
    ]
    return {"users": users}


# example of a refactored use case with a different response
async def newUseCase() -> UsersResponse:
    users = [
        User(public_id="1", name="John", age=30),
        User(public_id="2", name="Ane", age=20),
        User(public_id="3", name="Brooksss", age=28),
    ]
    return {"users": users}


@app.get("/users", response_model=UsersResponse)
async def get_users() -> UsersResponse:
    current_fn = lambda: currentUseCase()
    new_fn = lambda: newUseCase()

    result = await compare_async(
        current_fn=current_fn,
        new_fn=new_fn,
        percentage=80,  # percentage of requests to compare, good to control expensive endpoints
    )

    return result
