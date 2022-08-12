import time
import asyncio
from uuid import uuid4


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message):
        self.message = message

    def connection_made(self, transport):
        transport.write(self.message.encode())
        # print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        pass
        # print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        # print('The server closed the connection')
        pass


async def main(message):
    # Get a reference to the event loop as we plan to use
    # low-level APIs.

    loop = asyncio.get_running_loop()
    # start = time.time()
    # total = 0

    # for i in range(1, 1_000_000+1):
    #     if i%50000 == 0:
    #         total += 50000
    #         print(f"time taken for {total} records is {timme.time()-start} seconds")
        # on_con_lost = loop.create_future()

        # message = f"{i}    {uuid4()}"
    transport, protocol = await loop.create_connection(
        lambda: EchoClientProtocol(message),
        '127.0.0.1', 8888)

    # Wait until the protocol signals that the connection
    # is lost and close the transport.
    transport.close()

# asyncio.run(main())