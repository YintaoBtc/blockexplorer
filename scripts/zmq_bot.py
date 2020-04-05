import binascii
import asyncio
import zmq
import zmq.asyncio
import signal
import struct
import sys

port = 28332


class ZMQHandler():
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.zmqContext = zmq.asyncio.Context()

        self.zmqSubSocket = self.zmqContext.socket(zmq.SUB)
        self.zmqSubSocket.setsockopt(zmq.RCVHWM, 0)
        self.zmqSubSocket.setsockopt_string(zmq.SUBSCRIBE, "hashblock")
        self.zmqSubSocket.setsockopt_string(zmq.SUBSCRIBE, "hashtx")
        self.zmqSubSocket.setsockopt_string(zmq.SUBSCRIBE, "rawblock")
        self.zmqSubSocket.setsockopt_string(zmq.SUBSCRIBE, "rawtx")
        self.zmqSubSocket.connect("tcp://127.0.0.1:%i" % port)

    async def handle(self) :
        msg = await self.zmqSubSocket.recv_multipart()
        topic = msg[0]
        body = msg[1]
        sequence = "Unknown"
        if len(msg[-1]) == 4:
          msgSequence = struct.unpack('<I', msg[-1])[-1]
          sequence = str(msgSequence)
        if topic == b"hashblock":
            print('- HASH BLOCK ('+sequence+') -')
            print(binascii.hexlify(body))

            ##########################################################
            #           CONNECT RPC FOR INFO FROM HASH               #
            ##########################################################

            from connect_rpc import instruct_wallet


            body_hash = binascii.hexlify(body)
            hash_block = body_hash.decode('ascii')
            print(hash_block)

            x = instruct_wallet("getblock", [hash_block])["result"]
            confirmations = x["confirmations"]
            size = x["size"]
            height = x["height"]
            merkleroot = x["merkleroot"]
            datetime = x["time"]
            bits = x["bits"]
            difficulty = x["difficulty"]
            number_txs = x["nTx"]
            nonce = x["nonce"]

            print(f"Confirmations: {confirmations}\nSize: {size}\nHeight: {height}\nDifficulty: {difficulty}\nDatetime: {datetime}\nNumber of txs: {number_txs}")


        elif topic == b"hashtx":
            print('- HASH TX  ('+sequence+') -')
            print(binascii.hexlify(body))
        # schedule ourselves to receive the next message
        asyncio.ensure_future(self.handle())

    def start(self):
        self.loop.add_signal_handler(signal.SIGINT, self.stop)
        self.loop.create_task(self.handle())
        self.loop.run_forever()

    def stop(self):
        self.loop.stop()
        self.zmqContext.destroy()

daemon = ZMQHandler()
print("ZMQ daemon starting ...")
daemon.start()




