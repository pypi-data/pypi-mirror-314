from typing import Annotated

import jwt
from fastapi import Depends, Request, HTTPException

from fansauth.server.env import env
from fansauth.server.user import User as _User


def dep_User(req: Request):
    token = req.cookies.get('token')

    try:
        data = jwt.decode(token, env.public_key, algorithms=['RS256'])
        return env.get_user(data['username'])
    except Exception:
        raise HTTPException(401)


User = Annotated[_User, Depends(dep_User)]


def dep_Admin(user: User):
    if not user:
        raise HTTPException(401, 'Login required')
    if not (user and user.is_admin()):
        raise HTTPException(403, 'Admin required')
    return user


Admin = Annotated[_User, Depends(dep_Admin)]


def dep_Paginated(offset: int = 0, limit: int = 0):
    def func(query):
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        return query
    return func


Paginated = Annotated[callable, Depends(dep_Paginated)]
