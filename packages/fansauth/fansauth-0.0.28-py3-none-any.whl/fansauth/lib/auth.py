import time
import inspect
from typing import Annotated, Callable

import jwt
import requests
from fastapi import FastAPI, APIRouter, HTTPException, Response
from fastapi import Depends, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


_globals = {'public_key': None}


class User:

    def __init__(self, data):
        self.data = data
        self.username = data['username']

    def is_admin(self) -> bool:
        return self.data['admin']


class CheckMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, check_func):
        super().__init__(app)

        if inspect.iscoroutinefunction(check_func):
            self.check_func = check_func
        else:
            self.check_func = _wrap_as_async(check_func)

    async def dispatch(self, req, call_next):
        req.state.get_user = lambda: _get_user(req)
        try:
            check_result = await self.check_func(req)
        except HTTPException as exc:
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
        except Exception as exc:
            return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
        else:
            if check_result is False:
                raise HTTPException(403)
            return await call_next(req)


def auth(
        app,
        provider: str = 'https://auth.fans656.me',
        login: bool = False,
        admin: bool = False,
        check: Callable[[Request], bool] = None,
):
    """
    Add authorization to a FastAPI app.

    Params:

        app - A FastAPI app

        provider: str - Authorization server URL, defaults to "https://auth.fans656.me"

        login: bool - if True then requires login for all endpoint by default

        admin: bool - if True then requires admin login for all endpoint by default

        check: Callable[[Request], bool] - Custom authorization check function

            Check function takes a FastAPI Request object as solely argument,
            and has `request.state.get_user()` function to retrieve a optional `User` object.

                def check_func(request: Request):
                    user = request.state.get_user()
                    if not user:
                        if request.url.path.startswith('/api/public/'):
                            return True
                        else:
                            raise HTTPException(401)

            You can return False in check function to indicate HTTP 403 Forbidden response,
            or raise custom HTTPException directly.
            Note `None` return value will pass the authorization check.

    Returns:

        The FastAPI app
    """
    if isinstance(app, FastAPI):
        app.post('/api/grant')(api_grant)

        n_retries = 10
        for i_retry in range(n_retries):
            try:
                res = requests.get(f'{provider}/public-key')
                if res.status_code != 200:
                    raise RuntimeError(f'failed to retrieve public key from auth provider')
                _globals['public_key'] = res.text
                break
            except Exception:
                if i_retry + 1 == n_retries:
                    raise
                else:
                    time.sleep(0.1)
    else:
        raise TypeError(f'unsupported app type {type(app)}')

    if check:
        check_func = check
    elif admin:
        check_func = _check_admin_login
    elif login:
        check_func = _check_user_login
    else:
        check_func = None

    if check_func:
        app.add_middleware(CheckMiddleware, check_func=check_func)

    return app


def api_grant(req: dict, response: Response):
    auth_server = req['auth_server']

    url = f'{auth_server}/api/token'
    json = {
        'grant_type': 'authorization_code',
        'code': req['grant'],
    }
    res = requests.post(url, json=json)

    if res.status_code != 200:
        raise HTTPException(400, 'Failed to get token')

    token = res.json()['token']
    response.set_cookie(
        key='token',
        value=token,
        # TODO: set expire
        # max_age=token.expire_seconds,
    )
    return {'token': token}


def dep_User(req: Request):
    user = _get_user(req)
    if not user:
        raise HTTPException(401)
    return user


auth.User = Annotated[User, Depends(dep_User)]


def dep_Admin(user: auth.User):
    if not user.is_admin():
        raise HTTPException(403)
    return user


auth.Admin = Annotated[User, Depends(dep_Admin)]


def auth_check(check_func):
    pass


auth.check = auth_check


def _get_user(req):
    token = req.cookies.get('token')
    try:
        data = jwt.decode(token, _globals['public_key'], algorithms=['RS256'])
        return User(data)
    except Exception:
        return None


def _wrap_as_async(func):
    async def wrapped(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapped


def _check_user_login(req):
    user = _get_user(req)
    if not user:
        raise HTTPException(401)
    return user


def _check_admin_login(req):
    user = _check_user_login(req)
    if not user.is_admin():
        raise HTTPException(403)
