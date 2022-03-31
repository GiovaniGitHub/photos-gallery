
from passlib.context import CryptContext

PHOTOS_EXTENSIONS = ("png", "jpg", "jpeg", "gif")

PWD_CONTEXT = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000,
)

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
