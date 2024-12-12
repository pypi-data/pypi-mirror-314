# JWTs
A simple library for JWT management in FastAPI projects.

## Features
- Generate JWT tokens
- Decode JWT tokens
- Simple integration with FastAPI

## Installation
```bash
pip install JWT_tapo44ek
```
## How to use?

the current version is compatible with .env.
The file must contain two variables:

ALGORITHM = os.environ["ALGORITHM"]

SECRET_KEY = os.environ["SECRET_KEY"]

Where ALGORITHM = your encryption algorithm. For example, "HS256".

And SECRET_KEY is a unique "salt" example ->

3d7c8e5e7342064cb8b7abe038786b48740acd737bd725ce3037263cf619f145384ed6cf33385e62910b7190ada0b1d0370e53bad1055c86bacd6f27fe811a2a57205446f8d575

To form a jwt, a dictionary with data is passed -> expire is substituted automatically for an hour. To change -> go to the library code and change the timedelta.

To decode a token, you must have the ['exp'] parameter in the pydantic scheme.

Example:

class UserJWT(BaseModel):
 user_id:str
 exp : int 

Usage example:

Creating an instance of the class 
get_user = DecodeJWT(UserJWT)

And now we can use it in fastapi application ->

@router.get("/test", summary="JWT test")
async def test(user=Depends(get_user)):
 """
 JWT test
 """
 return {"user_data": user}

 




