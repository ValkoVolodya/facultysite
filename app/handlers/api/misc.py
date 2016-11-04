# coding: utf-8
import logging
import bson

from aiohttp.web import json_response
from aiohttp_jinja2 import template

from app.lib.json import dumps

log = logging.getLogger(__name__)


async def create(request):
    data = await request.json()
    id_ = await request.app.db.misc.insert(data)
    return json_response({
        'status': 'ok',
        'result': {
            'id_': id_,
        }
    }, dumps=dumps)


async def get(request):
    id_ = bson.ObjectId(request.match_info['id'])
    data = await request.app.db.misc.find_one({
        '_id': id_
    })
    return json_response({
        'status': 'ok',
        'result': data,
    }, dumps=dumps)
