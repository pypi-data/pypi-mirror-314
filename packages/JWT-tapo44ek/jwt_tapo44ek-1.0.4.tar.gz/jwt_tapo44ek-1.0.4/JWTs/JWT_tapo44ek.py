import jwt
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, Request, Depends
import logging
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

ALGORITHM = os.environ["ALGORITHM"]
SECRET_KEY = os.environ["SECRET_KEY"]

logger = logging.getLogger(__name__)


def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token not provided")
    return token


async def create_jwt_token(user_data):
    """
    Create jwt
    """
    if user_data:
        logger.info(f"Generate JWT with user_data:  {user_data}")

        payload = user_data
        payload["exp"] = datetime.now(timezone.utc) + timedelta(hours=1)

        return jwt.encode(payload, SECRET_KEY, ALGORITHM)

    else:
        raise HTTPException(status_code=401, detail="No user data")


class DecodeJWT:
    def __init__(self, pydantic_response_model=None):
        if pydantic_response_model is None:
            raise HTTPException(status_code=400, detail="Model must be provided")

        if not isinstance(pydantic_response_model, type) or not issubclass(
            pydantic_response_model, BaseModel
        ):
            raise HTTPException(
                status_code=400, detail="Provided model is not a Pydantic BaseModel"
            )

        self.pydantic_response_model = pydantic_response_model

    def __call__(self, token: str = Depends(get_token)):
        return self.decode_jwt(token)

    def _jwt(self, token: str = Depends(get_token)):
        if not token:
            raise HTTPException(status_code=401, detail="Token is missing")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            return self.pydantic_response_model(**payload)

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))
