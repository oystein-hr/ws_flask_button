from flask import Flask, send_file
import websockets
import webbrowser
import asyncio
import datetime


# Websocket server loop
async def time(websocket, path):    # ws_handler requires 2 arguments, path not used in this code
    while True:
        try:
            # Get current time, isoformat() makes it a string in ISO 8601 format
            now = datetime.datetime.now().time().isoformat(timespec='seconds')

            await websocket.send(now)       # Send current time to GUI
            await asyncio.sleep(1)          # Wait one second before running loop again

        # If GUI is closed, exit the while loop
        except websockets.ConnectionClosed:
            break

    # Stop the asyncio event loop - closing the program
    asyncio.get_event_loop().stop()


def main():
    app = Flask(__name__)

    start_server = websockets.serve(time, "127.0.0.1", 5001)

    # (mac os) Get current path and open the gui in default web browser
    webbrowser.open_new_tab('http://127.0.0.1:5000')

    # Start the websocket server
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_until_complete(app.run())

    # Keep the program running
    asyncio.get_event_loop().run_forever()

    @app.route("/")
    def hello():
        return send_file('front-end/index.html')


if __name__ == '__main__':
    main()
