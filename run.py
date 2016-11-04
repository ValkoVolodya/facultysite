# coding: utf-8
import click
import asyncio
import uvloop

from app.app import init_app


@click.command()
@click.argument('config_file', type=click.File('rb'), required=True)
def run_server(config_file):
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    srv, handler = loop.run_until_complete(init_app(loop, config_file.name))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(handler.finish_connections())


if __name__ == "__main__":
    run_server()
