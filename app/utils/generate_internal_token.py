import os
import jwt
from datetime import datetime, timedelta

JWT_INTERNAL_VALID_TIME_MINUTE = 60


def generate_internal_token():
    expired_at = round(
        (datetime.now() + timedelta(minutes=JWT_INTERNAL_VALID_TIME_MINUTE)).timestamp()
    )
    key = os.getenv("JWT_KEY")
    return jwt.encode(
        payload={
            "exp": expired_at,
            "i_sid": 9,
        },
        key=os.getenv("JWT_KEY"),
        algorithm="HS512",
    )
