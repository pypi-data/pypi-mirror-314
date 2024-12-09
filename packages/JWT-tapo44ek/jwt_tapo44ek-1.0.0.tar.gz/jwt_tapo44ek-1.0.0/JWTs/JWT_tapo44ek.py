import jwt
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, Request, Depends 
import logging


logger = logging.getLogger(__name__)


def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token not provided")
    return token


async def create_jwt_token(user_data, secret, algorythm):
    """
    Create jwt 
    """
    if user_data:

        logger.info(f"Генерация JWT с данными {user_data}")

        payload = user_data
        payload["exp"] = datetime.now(timezone.utc) + timedelta(hours=1)

        return jwt.encode(payload, secret, algorythm)
    
    else:
        raise HTTPException(status_code=401, detail="No user data")


def decode_jwt(token: str = Depends(get_token), secret, algorythm):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")

    try:
        payload = jwt.decode(
            token, secret, algorithms=[algorythm]
        )
        
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
