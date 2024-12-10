#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import stdout
from io import FileIO, BytesIO
from pathlib import PurePosixPath
from urllib.request import urlopen
from urllib.parse import urlencode, urlunparse
from logging import getLogger
from os import environ
from os.path import basename
from queue import Queue
from ipaddress import ip_address
from random import choice
from datetime import datetime
from tarfile import open
from asyncssh import create_connection, SSHClient, SSHClientSession
from aiodav import Client
from git.cmd import Git
from aiostream.stream import chain
from dns.resolver import Resolver
from httpx import AsyncClient
from humanize import naturalsize, naturaldelta
from aiofile import async_open


logger = getLogger()


remote = {
    'jenkins': {
        'location': 'http://192.168.21.1:5080/',
        'pathname': 'app/develop/develop/update/industry/crab/crab/',
    },
    'live': {
        'location': 'https://webdav.overforge.com/',
        'pathname': 'project/crab/'
    },
}


source = environ.get('SOURCE', 'live')


def resolve(host):
    try:
        return str(ip_address(host))
    except ValueError:
        return choice(Resolver().resolve(host)).to_text()


class Src():
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        kwargs = self.kwargs
        if kwargs.get('firmware'):
            location = kwargs.get('firmware')
            async def io():
                async with AsyncClient().stream(
                    method='get',
                    url=location,
                ) as response:
                    async for chunk in response.aiter_raw():
                        yield chunk
        elif source != 'local' and kwargs.get('version'):
            version = kwargs.get('version')
            location = f'''{remote.get(source).get('location')}{remote.get(source).get('pathname')}dists/crab-{version}.tar.xz'''
            async def io():
                async with AsyncClient().stream(
                    method='get',
                    url=location,
                ) as response:
                    async for chunk in response.aiter_raw():
                        yield chunk
        elif source != 'local' and kwargs.get('branch'):
            version = BytesIO(urlopen(f'''{remote.get(source).get('location')}{remote.get(source).get('pathname')}heads/{kwargs.get('branch')}.txt''').read()).read().decode()
            location = f'''{remote.get(source).get('location')}{remote.get(source).get('pathname')}dists/crab-{version}.tar.xz'''
            async def io():
                async with AsyncClient().stream(
                    method='get',
                    url=location,
                ) as response:
                    async for chunk in response.aiter_raw():
                        yield chunk
        else:
            location = f'''var/crab-{Git().describe(tags=True, abbrev=True, always=True, long=True, dirty=True)}.tar.xz'''
            async def io():
                async with async_open(location, mode='rb') as response:
                    async for chunk in response.iter_chunked(0x10000):
                        yield chunk
        self.location = location
        self.io = io

    def __iter__(self):
        yield (PurePosixPath('/tmp/firmware.bin'), self.io)

    async def dump(self):
        async for chunk in self.io():
            stdout.buffer.write(chunk)

    async def download(self):
        with FileIO(basename(self.location), 'wb') as file:
            async for chunk in self.io():
                file.write(chunk)
        logger.info(self.kwargs)
        logger.info(basename(self.location))


class Archive():
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __iter__(self):
        kwargs = self.kwargs
        tar = open(mode='r:xz', fileobj=Src(**kwargs).io)
        for tarinfo in tar.getmembers():
            file = tar.extractfile(tarinfo)
            if file:
                yield (PurePosixPath(f'''/usr/local/crab/{tarinfo.name}'''), file)
        tar.close()


class ClientAiodav():
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    async def create(self):
        pass

    async def putfo(self, files):
        kwargs = self.kwargs
        async with Client(urlunparse(('https', f'''{kwargs.get('host', '192.168.1.200')}:{kwargs.get('port', 6680)}''', '/', None, urlencode({}), None)), login=kwargs.get('username', 'admin'), password=kwargs.get('password', 'elite2014')) as client:
            for (path, content) in files:
                yield f'{path}\n'.encode()
                await client.upload_to(path=str(path), buffer=content())

    async def exec_command(self, commands):
        for command in commands:
            yield command

    async def exit(self):
        yield b'end\n'


class ClientAsyncssh():
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.connnection = None

    async def create(self):
        kwargs = self.kwargs
        connnection, client = await create_connection(SSHClient, resolve(kwargs.get('host', '192.168.1.200')), port=kwargs.get('port', 22), username=kwargs.get('username', 'root'), password=kwargs.get('password', 'elite2014'), known_hosts=None)
        self.connnection = connnection

    async def putfo(self, files):
        connnection = self.connnection
        async with connnection.start_sftp_client() as sftp:
            for (path, content) in files:
                yield f'{path}\n'.encode()
                try:
                    await sftp.chdir(str(path.parent))
                except IOError:
                    await sftp.mkdir(str(path.parent))
                async with sftp.open(str(path), 'wb+') as file:
                    size = 0
                    start = datetime.now()
                    async for chunk in content():
                        await file.write(chunk)
                        difference = datetime.now() - start
                        yield f'''{naturalsize(size, binary=True, format='%f')} {naturalsize(size / difference.total_seconds(), binary=True, format='%f')}/s {naturaldelta(difference)}\r'''.encode()
                        size = size + len(chunk)
                    yield b'\n'
    async def exec_command(self, commands):
        connnection = self.connnection
        for command in commands:
            yield command
            queue = Queue()
            job_done = object()
            class MySSHClientSession(SSHClientSession):
                def connection_lost(self, exc):
                    queue.put(f'{exc}\n'.encode())
                    queue.put(job_done)
                def data_received(self, data, datatype):
                    if isinstance(data, (bytes)):
                        queue.put(data)
                    elif isinstance(data, (str)):
                        queue.put(f'{data}\n'.encode())
                def eof_received(self):
                    queue.put(job_done)
                def exit_status_received(self, status):
                    queue.put(f'exit_status_received {status}\n'.encode())
                def __aiter__(self):
                    return self
                async def __anext__(self):
                    chunk = queue.get()
                    if chunk is job_done:
                        raise StopAsyncIteration
                    return chunk
            channel, session = await connnection.create_session(MySSHClientSession, command)
            await channel.wait_closed()
            async for item in session:
                yield item

    async def exit(self):
        yield b'end\n'


class Protocol():
    def __init__(self, *args, protocol='sftp', **kwargs):
        if protocol == 'webdav':
            self.client = ClientAiodav(*args, **kwargs)
        if protocol == 'sftp':
            self.client = ClientAsyncssh(*args, **kwargs)


class Distcrab():
    def __init__(self, host='192.168.1.200', port=22, username='root', password=None, download=False, dump=False, firmware=None, version=None, branch=None):
        self.client = Protocol(host=host, port=port, username=username, password=password).client
        self.download = download
        self.dump = dump
        self.firmware = firmware
        self.version = version
        self.branch = branch

    async def __aiter__(self):
        client = self.client
        download = self.download
        dump = self.dump
        firmware = self.firmware
        version = self.version
        branch = self.branch
        src = Src(firmware=firmware, version=version, branch=branch)
        if download:
            await src.download()
        elif dump:
            await src.dump()
        elif firmware:
            await client.create()
            async with chain(client.putfo(src), client.exec_command([
                b'/bin/mount -o rw,remount /\n',
                b'/bin/sync\n',
                b'/rbctrl/prepare-update.sh /tmp\n',
                b'/etc/init.d/rbctrl.sh stop\n',
                b'PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin /var/volatile/update/chrt-sqfs.sh /update/updater /mnt/tmp/update-final.sh\n'
            ]), client.exit()).stream() as stream:
                async for item in stream:
                    yield item
        else:
            await client.create()
            async with chain(client.exec_command([
                b'/usr/local/bin/elite_local_stop.sh\n',
            ]), client.putfo(src), client.exec_command([
                b'/bin/rm -rf /usr/local/crab/\n',
                b'/bin/mkdir -p /usr/local/crab/\n',
                b'/bin/sync\n',
                b'/bin/tar -xJf /tmp/firmware.bin -C /usr/local/crab/\n',
                b'/bin/rm -rf /tmp/firmware.bin\n',
                b'/bin/sync\n',
                b'/usr/local/bin/elite_local_start.sh\n',
            ]), client.exit()).stream() as stream:
                async for item in stream:
                    yield item
