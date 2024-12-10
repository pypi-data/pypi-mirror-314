#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from socket import socket
from queue import Queue
from threading import Thread
from asyncio import sleep
from paramiko import Transport, SSHException, SFTPClient

from . import resolve

class ClientParamiko():
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.transport = None

    async def create(self):
        kwargs = self.kwargs
        sock = socket()
        sock.connect((resolve(kwargs.get('host', '192.168.1.200')), kwargs.get('port', 22)))
        transport = Transport(sock)
        transport.start_client()
        try:
            if not kwargs.get('password'):
                raise SSHException
            transport.auth_password(kwargs.get('username', 'root'), kwargs.get('password', 'elite2014'))
        except SSHException:
            transport.auth_none(kwargs.get('username', 'root'))
        self.transport = transport

    async def putfo(self, files):
        client = SFTPClient.from_transport(self.transport)
        for (path, content) in files:
            try:
                client.chdir(str(path.parent))
            except IOError:
                client.mkdir(str(path.parent))
            queue = Queue(maxsize=1)
            job_done = object()
            def callback(transferred, total):
                queue.put('{0:.3f}\n'.format(transferred / total, 2).encode())
            def task():
                client.putfo(content, str(path), content.getbuffer().nbytes, callback)
                queue.put(job_done)
            thread = Thread(target=task)
            thread.start()
            while True:
                chunk = queue.get()
                if chunk is job_done:
                    break
                yield chunk
            thread.join()

    async def exec_command(self, commands):
        for command in commands:
            try:
                yield command
                await sleep(1)
                channel = self.transport.open_session()
                channel.set_combine_stderr(True)
                channel.exec_command(command.decode())
                line = b''
                while True:
                    self.transport.send_ignore()
                    if channel.recv_ready():
                        char = channel.recv(1)
                        line += char
                        if char == b'\n':
                            yield line
                            line = b''
                    if channel.exit_status_ready():
                        break
                channel.close()
            except EOFError:
                pass

    async def exit(self):
        yield b'end\n'
