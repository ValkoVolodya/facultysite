import logging

import jinja2
from aiohttp.web import Application
from aiohttp_jinja2 import setup as setup_jinja2
from motor.motor_asyncio import AsyncIOMotorClient

import app.handlers.root as root_handler
import app.handlers.api.misc as api_misc_handler

from app.lib.logging import configure_logging
from app.lib.config import read_config


log = logging.getLogger(__name__)


async def init_app(loop, config_filename):
    config = read_config(config_filename)
    host = config['app']['host']
    port = config['app']['port']

    configure_logging()
    
    # Set up database
    client = AsyncIOMotorClient(
        config['mongo']['host'],
        config['mongo']['port'],
    )
    mongo_db_name = config['mongo']['db']
    db = client[mongo_db_name]

    app = Application(loop=loop)
    app.db = db
    # FIXME: find a better way to configure templates folder
    setup_jinja2(app, loader=jinja2.FileSystemLoader('app/templates'))

    # Setup views
    app.router.add_route('GET', '/', root_handler.index)
    app.router.add_route('GET', '/about', root_handler.about)
    app.router.add_route('GET', '/api/misc/{id}', api_misc_handler.get)
    app.router.add_route('POST', '/api/misc/', api_misc_handler.create)
    app.router.add_static('/static', config['app']['static-dir'])

    handler = app.make_handler()

    srv = await loop.create_server(handler, host, port)

    log.info(
        'App started at http://%(host)s:%(port)s',
        {'host': host, 'port': port}
    )
    return srv, handler
