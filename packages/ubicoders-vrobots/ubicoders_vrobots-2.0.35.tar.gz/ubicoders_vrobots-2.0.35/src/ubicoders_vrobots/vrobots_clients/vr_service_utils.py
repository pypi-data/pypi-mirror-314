from websocket import create_connection
import time
import typing


def ws_req_service(req_msg, checker, url="ws://localhost:12740", timeout=3):
    ws = create_connection(url)
    ws.settimeout(timeout)

    keepRunning = True
    result = None
    while keepRunning:
        try:
            print("Sending...")
            ws.send(req_msg, opcode=0x2)
            rec_msg = ws.recv()
            keepRunning = not checker(rec_msg, 0)
            result = rec_msg
            time.sleep(1)
        except Exception as e:
            keepRunning = False
            print("No message received. Timeout.")
        finally:
            pass
    print("Received '%s'" % result)
    ws.close()
    return result


if __name__ == "__main__":

    msg = "hello ping"
    res = ws_req_service(msg, lambda x: True)
    print(res)
