from fastapi import FastAPI, HTTPException
from uvicorn import run
from models import models
from extentions.year_age import check_age

profiles = {}


app = FastAPI(title="Jobs, not Steve")

@app.get("/")
def root():
    return {"key" : "value"}


#POST
@app.post("/profile")
def create_profile(profile: models.Profile):
    if profile.login is None or profile.password is None \
        or profile.name is None or profile.surname is None \
            or profile.patronym is None or profile.birthday is None \
                or profile.email is None or profile.experience is None:
        raise HTTPException(status_code=400, detail=f"Not enough information")
    if profile.id is None:
        profile.id = len(profiles.keys()) + 1
    profile.age = check_age(profile.birthday)
    profiles[profile.id] = profile
    return profile


#GET
@app.get("/profile/{id}", response_model=models.Profile)
def get_profile(id: int) -> models.Profile:
    if id <= len(profiles.keys()):
        return profiles[id]
    else:
        raise HTTPException(status_code=404, detail=f"User {id} not found")


#PATCH
@app.patch("/profile/{id}", response_model=models.Profile)
def update_profile(id: int, profile: models.Profile):
    if id <= len(profiles.keys()) and profile.id is not None:
        print(profiles)
        if profile.login is not None:
            profiles[id].login = profile.login
        if profile.password is not None:
            profiles[id].password = profile.password
        if profile.name is not None:
            profiles[id].name = profile.name
        if profile.surname is not None:
            profiles[id].surname = profile.surname
        if profile.patronym is not None:
            profiles[id].patronym = profile.patronym
        if profile.email is not None:
            profiles[id].email = profile.email
        if profile.birthday is not None:
            profiles[id].birthday = profile.birthday
            profile.age = check_age(profile.birthday)
        if profile.experience is not None:
            profiles[id].experience = profile.experience
        return profile
    else:
        raise HTTPException(status_code=404, detail=f"User {id} not found")


#PUT
@app.put("/profile/{id}", response_model=models.Profile)
def update_profile(id: int, profile: models.Profile):
    if id <= len(profiles.keys()):
        if profile.login is None or profile.password is None \
            or profile.name is None or profile.surname is None \
            or profile.patronym is None or profile.birthday is None \
                or profile.email is None or profile.experience is None:
            raise HTTPException(status_code=400, detail=f"Not enough information")
        if profile.id is None:
            profile.id = id
        profile.age = check_age(profile.birthday)
        profiles[str(id)] = profile
        return profile
    else:
        raise HTTPException(status_code=404, detail=f"User {id} not found")


#DELETE
@app.delete("/profile/{id}")
def delete_profile(id: int):
    if id <= len(profiles.keys()):
        profiles.pop(id)
        return {"message": "Profile deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"User {id} not found")


if __name__ == "__main__":
    run("main:app", port=8000, host="0.0.0.0", reload=True)