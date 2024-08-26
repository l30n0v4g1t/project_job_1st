from fastapi import FastAPI, HTTPException, Request, exceptions
from fastapi.responses import JSONResponse
from uvicorn import run
from models import models
from uuid import uuid1, UUID
from extentions.year_age import check_age

profiles = {}


app = FastAPI(title="Jobs, not Steve")

@app.exception_handler(HTTPException)
def handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.get("/")
def root():
    try:
        return JSONResponse(status_code=200, content={"message" : "Everything is fine"})
    except HTTPException as httpexc:
        raise httpexc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


#POST
@app.post("/profile")
def create_profile(profile: models.Profile):
    if profile.id is None:
        profile.id = uuid1()
    profiles[profile.id] = profile
    return profiles[profile.id], check_age(profile.birthday)


#GET
@app.get("/profile/{id}", response_model=models.Profile)
def get_profile(id: UUID) -> models.Profile:
    if id in profiles.keys():
        return profiles[id]
    else:
        raise HTTPException(status_code=404, detail=f"User {id} not found")


#PATCH
@app.patch("/profile/{id}", response_model=models.Profile)
def update_profile(id: UUID, profile: models.Profile):
    if id in profiles.keys() and profile.id is not None:
        profiles[id].login = profile.login
        profiles[id].password = profile.password
        profiles[id].name = profile.name
        profiles[id].surname = profile.surname
        profiles[id].patronym = profile.patronym
        profiles[id].email = profile.email
        profiles[id].birthday = profile.birthday
        profiles[id].experience = profile.experience
        return profiles[id]
    else:
        raise HTTPException(status_code=404, detail=f"User {id} not found")


#PUT
@app.put("/profile/{id}", response_model=models.Profile)
def put_profile(id: UUID, profile: models.Profile):
    if profile.id is None:
        profile.id = uuid1()
    elif id in profiles.keys():
        profiles[id] = profile
        return profiles[id]
    else:
        raise HTTPException(status_code=404, detail=f"User {id} not found")


#DELETE
@app.delete("/profile/{id}")
def delete_profile(id: UUID):
    if id in profiles.keys():
        profiles.pop(id)
        return {"message": "Profile {id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"User {id} not found")


if __name__ == "__main__":
    run("main:app", port=8000, host="0.0.0.0", reload=True)