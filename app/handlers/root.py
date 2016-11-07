# coding: utf-8
import logging

from aiohttp_jinja2 import template


log = logging.getLogger(__name__)


@template('index.html')
async def index(request):
    data = await request.app.db.misc.find().to_list(length=10)
    return {
        'status': 'OK',
        'data': data,
    }


@template('about.html')
async def about(request):
    return {}
