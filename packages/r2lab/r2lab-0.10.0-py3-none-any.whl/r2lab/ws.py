import sys
import http.client
import websocket, asyncore

def _onopen():
    print("opened!")

def _onmessage(msg):
    print(("msg: " + str(msg)))

def _onclose():
    print("closed!")


def connect(server, port):

    print(("connecting to: %s:%d" %(server, port)))

    conn  = http.client.HTTPConnection(server + ":" + str(port))
    conn.request('POST','/socket.io/1/')
    resp  = conn.getresponse()
    hskey = resp.read().decode().split(':')[0]
    ws = websocket.WebSocket(
                'ws://'+server+':'+str(port)+'/socket.io/1/websocket/'+hskey,
                onopen   = _onopen,
                onmessage = _onmessage,
                onclose = _onclose)

    return ws

if __name__ == '__main__':

    server = 'r2lab-sidecar.inria.fr'
    port = 443
    server = 'localhost'
    port = 10000

    ws = connect(server, port)

    try:
        asyncore.loop()
    except KeyboardInterrupt:
        ws.close()
