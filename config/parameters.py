from fastapi.security import OAuth2PasswordBearer


"""
# API & HTTPS Parameters
"""
HOST_IP = "127.0.0.1"
PORT = 8000
KEY_FILE = "config/key.pem"
CERT_FILE = "config/cert.pem"


"""
# Database Parameters
"""
DB_URL = "sqlite://database/db.sqlite3"
MODEL_PATHS = ['database.models.manytomany', 
               'database.models.user', 
               'database.models.onetomany']


"""
# Regex Policies
"""
PASSWORD_POLICY = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{12,}$'
EMAIL_POLICY = r'^.+\@.+\..+$'
PHONE_POLICY = r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$'


"""
# JWT Parameters
"""
ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10
PRIV_KEY = open('config/priv_key.pem', 'r').read()
PUB_KEY = open('config/pub_key.pub', 'r').read()


"""
# OAuth2 Initialisation, Permissions
"""
OAUTH2_SCHEME = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.",
            "admin": "Allow critical methods"
            }
)


"""
# CORS & Middleware Parameters
"""
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
ALLOWED_METHODS = ["GET", "PUT", "POST", "DELETE"]
ORIGINS = [
    "https://127.0.0.1:8000",
    "https://localhost:8000"
]
