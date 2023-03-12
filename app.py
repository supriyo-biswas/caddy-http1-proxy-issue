#!/usr/bin/env python3

import random
import argparse
import asyncio
import uvloop

from aiohttp import web

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
routes = web.RouteTableDef()


async def send_dummy_data(response):
    for _ in range(20):
        await asyncio.sleep(2.5)
        await response.write(b'@')


@routes.post('/run/{param}')
async def run_language(request):
    try:
        param = request.match_info['param']
        data = (await request.post())['id']
    except KeyError:
        raise web.HTTPBadRequest()

    response = web.StreamResponse(status=200)
    await response.prepare(request)
    keepalive = asyncio.ensure_future(send_dummy_data(response))

    timeout = random.randint(1, 5)
    await asyncio.sleep(timeout)

    keepalive.cancel()
    await response.write(f'#done.{param}.{data}'.encode('utf-8'))

    return response


app = web.Application(client_max_size=144 * 1024)
app.add_routes(routes)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=2000, help='port to listen on')
    parser.add_argument('--host', default='127.0.0.1', help='address to listen on')
    parser.add_argument('--sock', help='unix socket to listen on')
    args = parser.parse_args()
    web.run_app(app, host=args.host, port=args.port)


if __name__ == '__main__':
    main()
