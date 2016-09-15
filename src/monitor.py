import asyncio
import aiohttp
import json
from docker import Client
from aiohttp import web


async def handle_data(request):
    containers = await get_containers()
    networks = await get_networks()
    json_string = json.dumps({'containers': containers, 'networks': networks})
    return web.Response(body=json_string.encode('utf-8'))


async def handle_containers(request):
    json_string = json.dumps(await get_containers())
    return web.Response(body=json_string.encode('utf-8'))


async def handle_networks(request):
    json_string = json.dumps(await get_networks())
    return web.Response(body=json_string.encode('utf-8'))


async def handle_statistics(request):
    json_string = json.dumps(await get_statistics())
    return web.Response(body=json_string.encode('utf-8'))


async def get_containers():
    api = Client(base_url='tcp://172.17.0.1:4242')
    containers = api.containers()
    return containers


async def get_networks():
    api = Client(base_url='tcp://172.17.0.1:4242')
    networks = api.networks()
    return networks


async def get_statistics():
    api = Client(base_url='tcp://172.17.0.1:4242')
    statistics = api.stats('')
    return statistics


def main():
    app = web.Application()
    app.router.add_route('GET', '/data', handle_data)
    app.router.add_route('GET', '/containers', handle_containers)
    app.router.add_route('GET', '/networks', handle_networks)
    app.router.add_route('GET', '/statistics', handle_statistics)
    app.router.add_static('/', 'static')
    web.run_app(app)

if __name__ == '__main__':
    main()