"""
TODO:
- register new user
    * consider handle of resource consumption attack, i.e. some one register a lot accounts
"""
import os
import json

from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import PlainTextResponse, FileResponse, RedirectResponse
from pydantic import BaseModel, Field
from fans.logger import get_logger

from fansauth import cons
from fansauth.server import deps
from fansauth.server.env import env
from fansauth.server.utils import add_query_param


logger = get_logger(__name__)
app = FastAPI()


@app.on_event('startup')
async def startup():
    logger.info(f'workdir: {env.workdir}')


class LoginReq(BaseModel):

    username: str = Field(..., max_length=100)
    password: str = Field(..., max_length=100)
    response_type: str = Field(default='code')
    redirect_uri: str = Field(default='')


@app.post('/api/login')
async def api_login(req: LoginReq, response: Response):
    user = env.get_user(req.username)

    if not user or not user.verify_password(req.password):
        raise HTTPException(400, 'Wrong username or password')

    token = user.generate_access_token()

    match req.response_type:
        case 'code':
            response.set_cookie(
                key='token',
                value=token.raw,
                max_age=token.expire_seconds,
            )
            return {'token': token.raw}
        case 'grant':
            grant = env.make_grant(token)
            if req.redirect_uri:
                return RedirectResponse(url=add_query_param(req.redirect_uri, 'grant', grant))
            else:
                return {'grant': grant}
        case _:
            raise HTTPException(400, f'invalid response_type "{req.response_type}"')


class TokenReq(BaseModel):

    grant_type: str = Field(default='authorization_code')
    code: str = Field()


@app.post('/api/token')
async def api_token(req: TokenReq):
    match req.grant_type:
        case 'authorization_code':
            token = env.use_grant(req.code)
            if not token:
                raise HTTPException(400, f'invalid code')
            return {'token': token.raw}
        case _:
            raise HTTPException(400, f'invalid grant_type "{req.grant_type}"')


@app.get('/api/users')
async def api_users(user: deps.Admin, paginated: deps.Paginated):
    query = env.get_users()
    return {
        'users': [{
            'username': d.username,
            'meta': json.loads(d.meta),
            'extra': json.loads(d.extra),
            'ctime': d.ctime,
        } for d in paginated(query)],
        'n_users': query.count(),
    }


@app.get('/api/user')
async def api_user(username: str, user: deps.Admin):
    user = env.get_user(username)
    if not user:
        raise HTTPException(404, f'user "{username}" not found')
    return {
        'username': user.username,
        'meta': user.meta,
        'extra': user.extra,
    }


class CreateUserReq(BaseModel):

    username: str
    password: str
    meta: dict = {}
    extra: dict = {}


@app.post('/api/create-user')
async def api_create_user(req: CreateUserReq, user: deps.Admin):
    if env.get_user(req.username):
        raise HTTPException(409)

    env.create_user(
        username=req.username,
        password=req.password,
        meta=req.meta,
        extra=req.extra,
    )


class DeleteUserReq(BaseModel):

    username: str


@app.post('/api/delete-user')
async def api_delete_user(req: DeleteUserReq, user: deps.Admin):
    if req.username == user.username:
        raise HTTPException(400, 'Cannot delete self')

    env.delete_user(req.username)


class EditUserReq(BaseModel):

    username: str
    meta: dict
    extra: dict


@app.post('/api/edit-user')
async def api_edit_user(req: EditUserReq, user: deps.Admin):
    if req.username == user.username and not (req.meta or {}).get('admin'):
        raise HTTPException(400, 'Cannot remove admin role of self')

    env.edit_user(req.username, req.meta, req.extra)


class ChangePasswordReq(BaseModel):

    old_password: str
    new_password: str


@app.post('/api/change-password')
async def api_change_password(req: ChangePasswordReq, user: deps.User):
    if not user.verify_password(req.old_password):
        raise HTTPException(400)

    env.change_password(user.username, req.new_password)


@app.get('/public-key', response_class=PlainTextResponse)
async def public_key():
    return env.public_key


@app.get('/favicon.ico')
async def favicon():
    return FileResponse(cons.root_dir / 'web/dist/favicon.ico')


@app.get('/assets/{path:path}')
async def assets(path):
    return FileResponse(cons.root_dir / 'web/dist/assets' / path)


@app.get('/{path:path}')
async def index():
    return FileResponse(cons.root_dir / 'web/dist/index.html')
