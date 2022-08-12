import asyncio
import atexit

f = open('file', 'a')

class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        self.transport = transport

    def data_received(self, data):
        global f
        message = data.decode()
        f.write(message + '\n')
        print(message)
        self.transport.write(b'')
        self.transport.close()
    



async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: EchoServerProtocol(),
        '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()
        
def close_file_discriptor():
    global f
    f.close()
    print('Closed File descriptor')

atexit.register(close_file_discriptor)
asyncio.run(main())