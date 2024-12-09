import click
import uvicorn
from fans.ports import ports

from fansauth import cons
from fansauth.server.env import env
from fansauth.server.app import app


@click.group()
def cli():
    pass


@cli.command()
@click.option('-d', '--data', default=None)
def serve(data):
    env.setup(data or cons.root_dir / 'data')
    uvicorn.run(app, host='0.0.0.0', port=ports.auth_back)


if __name__ == '__main__':
    cli()
