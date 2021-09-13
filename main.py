import uvicorn
import os

from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from fastapi import FastAPI, Request
from tortoise import Tortoise

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

from routers import parents, children, users, perms, students, courses
from config.parameters import (
    ALLOWED_HOSTS, 
    ORIGINS, 
    MODEL_PATHS, 
    KEY_FILE, 
    CERT_FILE, 
    PORT, 
    HOST_IP, 
    ALLOWED_METHODS, 
    ALLOWED_HOSTS,
    DB_URL
)


app = FastAPI()


"""
# Database Initialisation
"""
Tortoise.init_models(MODEL_PATHS, 'models')
register_tortoise(
    app,
    db_url=DB_URL,
    modules={"models": MODEL_PATHS},
    generate_schemas=True,
    add_exception_handlers=True,
)


"""
# API & Routers Initialisation
"""
app.include_router(parents.router)
app.include_router(children.router)
app.include_router(users.router)
app.include_router(perms.router)
app.include_router(students.router)
app.include_router(courses.router)

add_pagination(app)


@app.get("/")
def root():
    return {"Welcome": 
            "You can access API documentation through /docs"}


"""
# Middleware Initialisation
"""
app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=ALLOWED_HOSTS,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=ALLOWED_METHODS,
    allow_headers=["*"],
)


@app.middleware("http")
async def request_validator(request: Request, call_next):
    # We can filter either request or response 
    # before there are processed by the routers
    response = await call_next(request)
    return response


"""
# Main
"""
if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST_IP, 
                            port=PORT, 
                            reload=True,
                            ssl_keyfile= KEY_FILE,
                            ssl_certfile= CERT_FILE)
