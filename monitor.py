import asyncio
import aiohttp
import json
from docker import Client
from aiohttp import web


async def handle_containers(request):
    json_string = json.dumps(get_containers())
    return web.Response(body=json_string.encode('utf-8'))


async def handle_networks(request):
    json_string = json.dumps(get_networks())
    return web.Response(body=json_string.encode('utf-8'))


def get_containers():
    api = Client(base_url='tcp://127.0.0.1:2375')
    containers = api.containers()
    return containers


def get_networks():
    api = Client(base_url='tcp://127.0.0.1:2375')
    networks = api.networks()
    return networks


def main():
    app = web.Application()
    app.router.add_route('GET', '/containers', handle_containers)
    app.router.add_route('GET', '/networks', handle_networks)
    app.router.add_static('/', 'static')
    web.run_app(app)

if __name__ == '__main__':
    main()